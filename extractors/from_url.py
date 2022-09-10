import requests, sys, re

def extract(domain):
	try :
		r = requests.get(domain, timeout=4)
		result = from_string.extract(r.text)
		return result
	except Exception as e :
		print("[!] Error %s " % e )
		return []

def main() :
	if len(sys.argv) < 2 :
		sys.exit("[!] Url required; python3 from_url.py http://google.com") 
	print(extract(sys.argv[1]))

if __name__ == "__main__" :
	import from_string
	main()
else :
	from . import from_string
