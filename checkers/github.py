import requests, urllib

base_domains = ["github.com"]
cache_domains = set()


def check(url):

	
	parsed_url = urllib.parse.urlparse(url)
	
	# get only user
	if parsed_url.path.count('/') >= 2 :
		url = '/'.join(url.split('/')[:4])
	username = url.split("/")[-1].lower()
	#remove characters from username
	allowed = "abcdefghijklmnopqrstuvwxyz0123456789-"
	username = ''.join([ c for c in username if c in allowed ])
	url = url.replace(url.split("/")[-1], username)

	if url not in cache_domains :
		cache_domains.add(url) 


		try:
			r = requests.get(url, verify=False)
		except:
			return
		
		if r.status_code == 404 :
			print("[!] Github unregistred username:", url)

