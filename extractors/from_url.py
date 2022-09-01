import requests, sys, re
import from_string

def main(domain) :
	r = requests.get(domain)
	result = from_string.main(r.text)
	return result

if __name__ == "__main__" :
	if len(sys.argv) < 2 :
		sys.exit("[!] Url required; python3 from_url.py http://google.com")	
	print(main(sys.argv[1]))
