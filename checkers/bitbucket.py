import requests, urllib

base_domains = ["bitbucket.org"]
cache_domains = set()


def check(url):
	
	parsed_url = urllib.parse.urlparse(url)
	
	# get only user
	if parsed_url.path.count('/') >= 2 :
		url = '/'.join(url.split('/')[:4])
	
	if url not in cache_domains :
		cache_domains.add(url) 


		r = requests.get(url, verify=False)

		if r.status_code == 404 and "Resource not found" in r.text :
			print("[!] Bitbucket unregistred username:", url)

