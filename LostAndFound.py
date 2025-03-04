import os, sys, argparse, importlib.util, urllib, fnmatch, tqdm, requests
from extractors import from_url, from_string, from_apk, from_binary, from_dir
from utils import *
import dns_proxy  # Import our new DNS proxy module
import threading
import time

args = []

def banner() :
    b = '''
    :･ﾟ✧:･ﾟ✧:☆*:✧:･ﾟ✧::☆*:･ﾟ✧::☆*::･ﾟ:☆*:ﾟ✧:･ﾟ:☆*::･ﾟ::☆☆*:*:･ﾟ✧
    (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧     𝓛𝓸𝓼𝓽 & 𝓕𝓸𝓾𝓷𝓭         。.:☆*:･'(*⌒―⌒*)))
    :･ﾟ✧:･ﾟ✧:☆*:✧:･ﾟ✧::☆*:･ﾟ✧::☆*::･ﾟ:☆*:ﾟ✧:･ﾟ:☆*::･**ﾟ:ﾟ:☆*::･ﾟ✧
    '''

    print(b)

def load_checkers():
    checkers_folder = "./checkers"
    checkers = {}
    checkers_files = os.listdir(checkers_folder)

    for c in checkers_files:
        location = os.path.join(checkers_folder,c)

        if c[-3:] != '.py' or os.path.isfile(location) != True :
            continue

        info = importlib.machinery.PathFinder().find_spec(c[:-3],[checkers_folder])
        p = info.loader.load_module()
        checkers[c[:-3]] = p
    return checkers

def check_all(urls, checkers):

    domains = [] 
    if args.verbose :
        print(urls)
    print("[?] Checking URLS ...")
    for u in tqdm.tqdm(urls) :
        u = clean_url(u)

        parsed_url = urllib.parse.urlparse(u)

        #print(parsed_url)

        domains.append(parsed_url.netloc)

        for c in checkers.keys() :
            if hasattr(checkers[c], "base_domains") :
                if fnmatch_all(parsed_url.netloc, checkers[c].base_domains) :
                    checkers[c].check(u)
                    domains.remove(parsed_url.netloc)

    print("[?] Checking Domains ...")

    checkers["domain"].check(domains)

def main(args):
    checkers = load_checkers()
    banner()

    requests.packages.urllib3.disable_warnings() # ignore SSL warnings

    if args.proxy:
        print("DNS PROXY: ", args.proxy)
        proxy_args = args.proxy.split(',') if args.proxy else []
        dns_server = "8.8.8.8"  # Default value
        proxy_port = 5333  # Default value
        duration = 3600  # Default value (1 hour)
        
        # Parse custom arguments if provided
        if len(proxy_args) >= 1 and proxy_args[0]:
            dns_server = proxy_args[0]
        if len(proxy_args) >= 2 and proxy_args[1]:
            proxy_port = int(proxy_args[1])
        if len(proxy_args) >= 3 and proxy_args[2]:
            duration = int(proxy_args[2])
            
        print(f"Starting DNS proxy with upstream DNS {dns_server}, port {proxy_port}, for {duration} seconds")
        # Create and start the DNS proxy
        dns_proxy.upstream_dns = dns_server
        dns_proxy.proxy_port = proxy_port
        dns_proxy.verbose = args.verbose  # Pass the verbose flag
        
        if args.verbose:
            print("Verbose mode ON - showing all DNS queries\n")
            
        proxy_thread = threading.Thread(target=dns_proxy.dns_proxy_server)
        proxy_thread.daemon = True
        proxy_thread.start()
        
        try:
            # Run for the specified duration
            time.sleep(duration)
        except KeyboardInterrupt:
            print("Keyboard interrupt received, stopping DNS proxy")
        finally:
            dns_proxy.running = False
            proxy_thread.join(timeout=5)
            dns_proxy.report_unregistered_domains()
    elif args.url:
        print("URL: ", args.url)
        urls = set()
        if os.path.isfile(args.url) :
            with open(args.url) as f :
                clean_urls = []
                for l in f :
                    clean_urls.append(clean_url(l.strip()))

                urls = from_url.extract(clean_urls)
        else :
            urls = from_url.extract(args.url)
        
        check_all(urls, checkers)
    elif args.apk:  
        print("APK: ", args.apk)
        urls = from_apk.extract(args.apk)
        check_all(urls, checkers)
    elif args.dir:
        print("DIR: ", args.dir)
        urls = from_dir.extract(args.dir)
        check_all(urls, checkers)
    elif args.ipa:
        print("IPA: ", args.ipa)
    elif args.bin:
        print("BIN: ", args.bin)
        urls = from_binary.extract(args.bin)
        check_all(urls, checkers)
    elif args.txt:
        print("TXT: ", args.txt)
        f = open(args.txt,"r").read()
        urls = from_string.extract(f)
        check_all(urls, checkers)

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description="")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--url", help="URL to check")
    group.add_argument("-a", "--apk", help="APK to check")
    group.add_argument("-d", "--dir", help="Directory of Source Code to check")
    group.add_argument("-i", "--ipa", help="IPA to check")
    group.add_argument("-b", "--bin", help="Binary to check")
    group.add_argument("-t", "--txt", help="Text file to check")
    group.add_argument("-p", "--proxy", help="DNS Proxy with format: [upstream_dns],[port],[duration_seconds]")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")

    args = parser.parse_args()

    if len(sys.argv) == 1 :
        parser.print_help(sys.stderr)
        sys.exit()

    main(args)
