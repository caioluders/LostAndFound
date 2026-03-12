import requests, urllib

base_domains = ["packagist.org"]
cache_domains = set()


def check(url):
	parsed_url = urllib.parse.urlparse(url)
	path_parts = parsed_url.path.strip("/").split("/")

	# packagist.org/packages/{vendor}/{package}
	if len(path_parts) < 3 or path_parts[0] != "packages":
		return

	vendor = path_parts[1]
	package = path_parts[2]
	full_name = f"{vendor}/{package}"

	if full_name in cache_domains:
		return
	cache_domains.add(full_name)

	try:
		r = requests.get(f"https://packagist.org/packages/{full_name}.json", timeout=10)
		if r.status_code == 404:
			print(f"[Packagist] Package not found: {full_name}")
	except:
		pass
