import os, sys, argparse, importlib.util, urllib, fnmatch
from extractors import from_url, from_string, from_apk, from_binary
from utils import *

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
	print(urls)
	for u in urls :

		u = clean_url(u)	
		parsed_url = u.replace("www.","") # fodase os edgecase

		parsed_url = urllib.parse.urlparse(parsed_url)

		#print(parsed_url)

		domains.append(parsed_url.netloc)

		for c in checkers.keys() :
			if hasattr(checkers[c], "base_domains") :
				if fnmatch_all(parsed_url.netloc, checkers[c].base_domains) :
					checkers[c].check(u)
					domains.remove(parsed_url.netloc)

	checkers["domain"].check(domains)

def main(args):
	checkers = load_checkers()
	if args.url:
		print("URL: ", args.url)
		urls = from_url.extract(args.url)
		check_all(urls, checkers)
	elif args.apk:  
		print("APK: ", args.apk)
		urls = from_apk.extract(args.apk)
		check_all(urls, checkers)
	elif args.dir:
		print("DIR: ", args.dir)
	elif args.ipa:
		print("IPA: ", args.ipa)
	elif args.bin:
		print("BIN: ", args.bin)
		urls = from_binary.extract(args.bin)
		check_all(urls, checkers)
	elif args.proxy:
		print("PROXY: ", args.proxy)
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
	group.add_argument("-p", "--proxy", help="Proxy to check")

	args = parser.parse_args()

	if len(sys.argv) == 1 :
		parser.print_help(sys.stderr)
		sys.exit()

	main(args)
