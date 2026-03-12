import requests, urllib

base_domains = ["firebaseio.com", "*.firebasedatabase.app", "firebaseapp.com"]
cache_domains = set()


def check(url):
	parsed = urllib.parse.urlparse(url)
	netloc = parsed.netloc

	# extract project name from {project}.firebaseio.com etc
	project = netloc.split(".")[0]

	if not project:
		return

	if project in cache_domains:
		return
	cache_domains.add(project)

	try:
		r = requests.get(f"https://{project}.firebaseio.com/.json", timeout=10)
		if r.status_code == 404 or "PROJECT_NOT_FOUND" in r.text:
			print(f"[Firebase] Project not found: {project}")
	except:
		pass
