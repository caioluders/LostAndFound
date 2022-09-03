import os, sys, argparse, importlib.util, urllib
from extractors import from_url 

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
		if hasattr(p,'base_domain'):
			checkers[p.base_domain] = p
		else :
			checkers[c[:-3]] = p
	return checkers

def check_all(urls, checkers):

	domains = []
	print(urls)
	for u in urls :
		if not (u.startswith('http') or u.startswith('//')): # vai quebrar com ctz
			u = u[1:]
		u = u.replace("www.","") # fodase os edgecase

		parsed_url = urllib.parse.urlparse(u)

		if parsed_url.netloc in checkers.keys() :
			checkers[parsed_url.netloc].check(u)
			urls.remove(u)
		else :
			domains.append(parsed_url.netloc)

	checkers["domain"].check(domains)

def main(args):
	checkers = load_checkers()
	if args.url:
		print("URL: ", args.url)
		urls = from_url.extract(args.url)
		check_all(urls, checkers)
	elif args.apk:  
		print("APK: ", args.apk)
	elif args.dir:
		print("DIR: ", args.dir)
	elif args.ipa:
		print("IPA: ", args.ipa)
	elif args.bin:
		print("BIN: ", args.bin)
	elif args.proxy:
		print("PROXY: ", args.proxy)

if __name__ == "__main__" :
	parser = argparse.ArgumentParser(description="")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-u", "--url", help="URL to check")
	group.add_argument("-a", "--apk", help="APK to check")
	group.add_argument("-d", "--dir", help="Directory of Source Code to check")
	group.add_argument("-i", "--ipa", help="IPA to check")
	group.add_argument("-b", "--bin", help="Binary to check")
	group.add_argument("-p", "--proxy", help="Proxy to check")

	args = parser.parse_args()
	main(args)
