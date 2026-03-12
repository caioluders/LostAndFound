import requests, urllib

base_domains = ["gitlab.com"]
cache_domains = set()


def check(url):

	parsed_url = urllib.parse.urlparse(url)
	path_parts = parsed_url.path.strip("/").split("/")

	# get only user
	username = path_parts[0] if path_parts and path_parts[0] else ""
	if not username:
		return

	profile_url = f"https://gitlab.com/{username}"

	if profile_url in cache_domains:
		return
	cache_domains.add(profile_url)

	try:
		r = requests.get(profile_url, verify=False, allow_redirects=False)
	except:
		return

	if r.status_code != 302 or "You are being" not in r.text:
		return

	# Check if this is a renamed user — if a repo path redirects (301),
	# the repos are protected and the username is not truly available.
	if len(path_parts) >= 2 and path_parts[1]:
		repo_url = f"https://gitlab.com/{username}/{path_parts[1]}"
		try:
			r2 = requests.head(repo_url, allow_redirects=False, verify=False, timeout=10)
			if r2.status_code == 301:
				return
		except:
			pass

	print(f"[!] Gitlab unregistered username: {profile_url}")
