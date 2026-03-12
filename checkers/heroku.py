import requests, urllib

base_domains = ["herokuapp.com", "herokussl.com", "herokudns.com"]
cache_domains = set()


def check(url):
	parsed = urllib.parse.urlparse(url)
	netloc = parsed.netloc

	if netloc in cache_domains:
		return
	cache_domains.add(netloc)

	try:
		r = requests.get(f"https://{netloc}/", timeout=10, verify=False)
		if "No such app" in r.text or "herokucdn.com/error-pages/no-such-app" in r.text:
			print(f"[Heroku] App not found: {netloc}")
	except:
		pass
