import requests, urllib

base_domains = ["rubygems.org"]
cache_domains = set()


def check(url):
	parsed_url = urllib.parse.urlparse(url)
	path_parts = parsed_url.path.strip("/").split("/")

	# rubygems.org/gems/{name}
	if len(path_parts) < 2 or path_parts[0] != "gems":
		return

	gem = path_parts[1]

	if gem in cache_domains:
		return
	cache_domains.add(gem)

	try:
		r = requests.get(f"https://rubygems.org/api/v1/gems/{gem}.json", timeout=10)
		if r.status_code == 404:
			print(f"[RubyGems] Gem not found: {gem}")
	except:
		pass
