import requests, urllib

base_domains = ["npmjs.com", "npmjs.org"]
cache_domains = set()


def check(url):
	parsed_url = urllib.parse.urlparse(url)
	path_parts = parsed_url.path.strip("/").split("/")

	# npmjs.com/package/{name} or npmjs.com/package/{@scope}/{name}
	if len(path_parts) < 2 or path_parts[0] != "package":
		return

	package = "/".join(path_parts[1:])

	if package in cache_domains:
		return
	cache_domains.add(package)

	try:
		r = requests.get(f"https://registry.npmjs.org/{package}", timeout=10)
		if r.status_code == 404:
			print(f"[npm] Package not found: {package}")
	except:
		pass
