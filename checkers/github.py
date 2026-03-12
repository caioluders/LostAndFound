import requests, urllib

base_domains = ["github.com"]
cache_domains = set()
deny_list_usernames = ["orgs", "features", "marketplace", "explore", "topics", "trending", "collections", "events", "sponsors", "settings", "notifications", "login", "join", "new", "about", "pricing", "security", "enterprise", "team", "customer-stories"]


def check(url):

	parsed_url = urllib.parse.urlparse(url)
	path_parts = parsed_url.path.strip("/").split("/")

	# get only user
	username = path_parts[0].lower() if path_parts and path_parts[0] else ""
	if not username:
		return

	if username in deny_list_usernames:
		return
	#remove characters from username
	allowed = "abcdefghijklmnopqrstuvwxyz0123456789-"
	username = ''.join([ c for c in username if c in allowed ])
	if not username:
		return

	profile_url = f"https://github.com/{username}"

	if profile_url in cache_domains:
		return
	cache_domains.add(profile_url)

	try:
		r = requests.get(profile_url, verify=False)
	except:
		return

	if r.status_code != 404:
		return

	# Check if this is a renamed user with retired repos.
	# If the original URL has a repo path and GitHub returns a 301 redirect,
	# the repos are retired/protected — not a real takeover.
	if len(path_parts) >= 2 and path_parts[1]:
		repo_url = f"https://github.com/{username}/{path_parts[1]}"
		try:
			r2 = requests.head(repo_url, allow_redirects=False, verify=False, timeout=10)
			if r2.status_code == 301:
				return
		except:
			pass

	print(f"[!] Github unregistered username: {profile_url}")
