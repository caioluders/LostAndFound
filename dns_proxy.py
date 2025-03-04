#!/usr/bin/env python3

import socket
import threading
import time
import argparse
import logging
import dnslib
import tldextract
import requests
import json
import aiodns
import asyncio
import string
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("dns_proxy.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("DNS-Proxy")

# Global variables
unregistered_domains = set()
forwarded_queries = {}
upstream_dns = "8.8.8.8"  # Default to Google DNS
dns_port = 53
proxy_port = 5333
running = True
verbose = False

class AsyncResolver(object):
    def __init__(self, nameserver=None):
        self.timeout = 0.1
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.resolver = aiodns.DNSResolver(timeout=self.timeout, loop=self.loop)
        self.resolver.nameservers = [nameserver or upstream_dns]

    async def query(self, domain, type):
        return await self.resolver.query(domain, type)

    def query_A(self, domain):
        """query DNS A records.
        Returns data if found, raises aiodns.error.DNSError if not found
        """
        f = self.query(domain, 'A')
        result = self.loop.run_until_complete(f)
        data = list(map(lambda x: x.host, result))
        item = {"domain": domain, "type": "A", "data": data}
        return item

def clean_domain(dirty_domain):
    """Clean and validate domain name"""
    allowed_chars = string.ascii_letters + string.digits + "-."

    for i in range(len(dirty_domain)):
        if dirty_domain[i] not in allowed_chars:
            i -= 1
            break

    domain_ext = tldextract.extract(dirty_domain[:i+1])
    
    # Get the domain and suffix (TLD)
    if not domain_ext.domain or not domain_ext.suffix:
        return False
        
    domain_parts = [domain_ext.domain, domain_ext.suffix]
    if domain_ext.subdomain:
        domain_parts.insert(0, domain_ext.subdomain)
    
    return ".".join(domain_parts)

def is_domain_registered(domain):
    """Check if a domain is registered using DNS query"""
    try:
        # Clean and extract the main domain
        clean_dom = clean_domain(domain)
        if not clean_dom:
            return True  # Assume registered if domain format is invalid
            
        # Extract just the main domain without subdomains for registration check
        ext = tldextract.extract(clean_dom)
        domain_to_check = f"{ext.domain}.{ext.suffix}"
        
        # If we've already checked this domain recently, return cached result
        if domain_to_check in forwarded_queries:
            if time.time() - forwarded_queries[domain_to_check]['time'] < 3600:  # Cache for 1 hour
                return forwarded_queries[domain_to_check]['registered']
        
        # Use aiodns to check if domain is registered
        dns_resolver = AsyncResolver(nameserver=upstream_dns)
        is_registered = True
        
        try:
            dns_resolver.query_A(domain_to_check)
        except aiodns.error.DNSError as error:
            # Error code 4 means domain not found (NXDOMAIN)
            if error.args[0] == 4:
                is_registered = False
            
        # Store result in cache
        forwarded_queries[domain_to_check] = {
            'time': time.time(),
            'registered': is_registered
        }
        
        if verbose:
            status = "REGISTERED" if is_registered else "NOT REGISTERED"
            print(f"[CHECK] Domain {domain_to_check} is {status}")
            
        return is_registered
    except Exception as e:
        logger.error(f"Error checking domain {domain}: {e}")
        return True  # Assume registered in case of error
        
def process_dns_query(data, client_address):
    """Process a DNS query packet"""
    try:
        # Parse the DNS query using dnslib
        request = dnslib.DNSRecord.parse(data)
        qname = str(request.q.qname)
        qtype = dnslib.QTYPE[request.q.qtype]
        
        # Remove trailing dot from domain name
        if qname.endswith('.'):
            qname = qname[:-1]
        
        # Clean domain name
        clean_dom = clean_domain(qname)
        if not clean_dom:
            if verbose:
                print(f"\n[QUERY] {client_address[0]}:{client_address[1]} -> {qname} ({qtype}) - INVALID DOMAIN")
            logger.warning(f"Invalid domain format: {qname}")
        else:
            qname = clean_dom
            
            if verbose:
                print(f"\n[QUERY] {client_address[0]}:{client_address[1]} -> {qname} ({qtype})")
                logger.info(f"Received DNS query for {qname} from {client_address[0]}:{client_address[1]}")
        
            # Check if the domain is registered
            domain_registered = is_domain_registered(qname)
            if not domain_registered:
                unregistered_domains.add(qname)
                warning_msg = f"Domain {qname} appears to be unregistered!"
                logger.warning(warning_msg)
                if verbose:
                    print(f"[WARNING] {warning_msg}")
        
        # Forward the query to the upstream DNS server
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (upstream_dns, dns_port))
        
        # Receive the response from the upstream DNS server
        sock.settimeout(5)  # 5 second timeout
        response_data, _ = sock.recvfrom(4096)
        sock.close()
        
        # Parse and print response if in verbose mode
        if verbose:
            try:
                response = dnslib.DNSRecord.parse(response_data)
                print(f"[RESPONSE] {upstream_dns} -> {qname}")
                for rr in response.rr:
                    print(f"  {rr.rname} {dnslib.QTYPE[rr.rtype]} {rr.rdata}")
            except Exception as e:
                print(f"[ERROR] Failed to parse response: {e}")
        
        return response_data
            
    except Exception as e:
        error_msg = f"Error processing DNS query: {e}"
        logger.error(error_msg)
        if verbose:
            print(f"[ERROR] {error_msg}")
        # In case of error, return an empty response
        return dnslib.DNSRecord(
            header=dnslib.DNSHeader(id=dnslib.DNSRecord.parse(data).header.id, rcode=3),
            q=dnslib.DNSRecord.parse(data).q
        ).pack()

def dns_proxy_server():
    """Run the DNS proxy server"""
    global running
    
    try:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', proxy_port))
        start_msg = f"DNS proxy server started on port {proxy_port}"
        logger.info(start_msg)
        if verbose:
            print(f"[INFO] {start_msg}")
            print(f"[INFO] Using upstream DNS server: {upstream_dns}")
            print(f"[INFO] Verbose mode ON - showing all DNS queries\n")
        
        # Set a timeout to allow checking for the running flag
        sock.settimeout(1)
        
        while running:
            try:
                # Receive data from client
                data, client_address = sock.recvfrom(4096)
                
                # Process the query in a separate thread to avoid blocking
                threading.Thread(
                    target=lambda: client_response(data, client_address, sock)
                ).start()
                
            except socket.timeout:
                continue
            except Exception as e:
                error_msg = f"Error in main DNS proxy loop: {e}"
                logger.error(error_msg)
                if verbose:
                    print(f"[ERROR] {error_msg}")
                
    except Exception as e:
        error_msg = f"Failed to start DNS proxy server: {e}"
        logger.error(error_msg)
        if verbose:
            print(f"[ERROR] {error_msg}")
    finally:
        if sock:
            sock.close()
        stop_msg = "DNS proxy server stopped"
        logger.info(stop_msg)
        if verbose:
            print(f"[INFO] {stop_msg}")

def client_response(data, client_address, sock):
    """Handle processing the DNS query and sending the response back to the client"""
    try:
        response = process_dns_query(data, client_address)
        sock.sendto(response, client_address)
    except Exception as e:
        error_msg = f"Error sending response to client: {e}"
        logger.error(error_msg)
        if verbose:
            print(f"[ERROR] {error_msg}")

def report_unregistered_domains():
    """Generate a report of unregistered domains"""
    if unregistered_domains:
        report_header = "=== UNREGISTERED DOMAINS REPORT ==="
        logger.info(report_header)
        if verbose:
            print(f"\n[REPORT] {report_header}")
            
        for domain in sorted(unregistered_domains):
            domain_msg = f"Unregistered domain: {domain}"
            logger.info(domain_msg)
            if verbose:
                print(f"[REPORT] {domain_msg}")
                
        total_msg = f"Total unregistered domains: {len(unregistered_domains)}"
        logger.info(total_msg)
        if verbose:
            print(f"[REPORT] {total_msg}")
    else:
        no_domains_msg = "No unregistered domains detected"
        logger.info(no_domains_msg)
        if verbose:
            print(f"\n[REPORT] {no_domains_msg}")

def main():
    global upstream_dns, proxy_port, running, verbose
    
    parser = argparse.ArgumentParser(description="DNS Proxy Server for Lost & Found")
    parser.add_argument("--dns", help="Upstream DNS server (default: 8.8.8.8)", default="8.8.8.8")
    parser.add_argument("--port", help="Proxy port to listen on (default: 5333)", type=int, default=5333)
    parser.add_argument("--time", help="Time to run the proxy in seconds (default: 3600)", type=int, default=3600)
    parser.add_argument("--verbose", "-v", help="Enable verbose output", action="store_true")
    args = parser.parse_args()
    
    upstream_dns = args.dns
    proxy_port = args.port
    duration = args.time
    verbose = args.verbose
    
    logger.info(f"Starting DNS proxy with upstream DNS {upstream_dns}, listening on port {proxy_port}")
    logger.info(f"Will run for {duration} seconds")
    
    # Start the DNS proxy server in a separate thread
    proxy_thread = threading.Thread(target=dns_proxy_server)
    proxy_thread.daemon = True
    proxy_thread.start()
    
    try:
        # Run for the specified duration
        time.sleep(duration)
    except KeyboardInterrupt:
        interrupt_msg = "Keyboard interrupt received, stopping DNS proxy"
        logger.info(interrupt_msg)
        if verbose:
            print(f"[INFO] {interrupt_msg}")
    finally:
        running = False
        proxy_thread.join(timeout=5)
        report_unregistered_domains()
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"unregistered_domains_{timestamp}.txt", "w") as f:
            for domain in sorted(unregistered_domains):
                f.write(f"{domain}\n")
        
        if unregistered_domains:
            file_msg = f"Unregistered domains saved to unregistered_domains_{timestamp}.txt"
            logger.info(file_msg)
            if verbose:
                print(f"[INFO] {file_msg}")

if __name__ == "__main__":
    main() 