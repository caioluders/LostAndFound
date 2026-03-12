#!/usr/bin/env python3

import socket
import tldextract
import logging

base_domains = ["*"]  # Match all domains
cache_domains = set()

logger = logging.getLogger(__name__)

def check_domain_status(domain):
    """Check if a domain exists by attempting to resolve it"""
    try:
        # Extract the main domain without subdomains
        ext = tldextract.extract(domain)
        domain_to_check = f"{ext.domain}.{ext.suffix}"
        
        # Try to resolve the domain
        socket.gethostbyname(domain_to_check)
        return True
    except socket.gaierror as e:
        # Only flag NXDOMAIN (EAI_NONAME), not timeouts or transient failures
        if e.errno == socket.EAI_NONAME:
            return False
        return True
    except Exception as e:
        logger.error(f"Error checking domain {domain}: {e}")
        return True  # Assume registered in case of error

def check(url):
    """Check function called by LostAndFound"""
    try:
        # Parse URL to get domain
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        # Skip if no domain found or already checked
        if not domain or domain in cache_domains:
            return
        cache_domains.add(domain)

        # Check if domain exists
        domain_exists = check_domain_status(domain)
        
        if not domain_exists:
            print(f"[DNS] Potential domain takeover opportunity: {domain} is unregistered")
    
    except Exception as e:
        logger.error(f"Error in DNS status checker: {e}") 