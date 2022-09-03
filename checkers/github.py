import requests, urllib

base_domain = "github.com"

def check(url):
	if url.startswith("//") :
		url = "https:"+url

	parsed_url = urllib.parse.urlparse(url)
	
	if parsed_url.path.count('/') >= 2 :
		url = '/'.join(url.split('/')[:4])
	r = requests.get(url)

	if r.status_code == 404 :
		print("[!] Github unregistred username:", url)