import requests, urllib

base_domains = ["pypi.org", "pypi.python.org"]
cache_domains = set()


def check(url):
	parsed_url = urllib.parse.urlparse(url)
	path_parts = parsed_url.path.strip("/").split("/")

	# pypi.org/project/{name}/ or pypi.org/pypi/{name}/json
	if len(path_parts) < 2:
		return

	if path_parts[0] in ("project", "pypi"):
		package = path_parts[1]
	else:
		return

	if package in cache_domains:
		return
	cache_domains.add(package)

	try:
		r = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=10)
		if r.status_code == 404:
			print(f"[PyPI] Package not found: {package}")
	except:
		pass
