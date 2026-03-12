import requests, urllib

base_domains = ["*.blob.core.windows.net"]
cache_domains = set()


def check(url):
	parsed = urllib.parse.urlparse(url)
	netloc = parsed.netloc

	# {account}.blob.core.windows.net
	account = netloc.replace(".blob.core.windows.net", "")

	if not account or "." in account:
		return

	if account in cache_domains:
		return
	cache_domains.add(account)

	try:
		r = requests.get(
			f"https://{account}.blob.core.windows.net/?comp=list",
			timeout=10, verify=False
		)
		if "AccountNotFound" in r.text or "InvalidResourceName" in r.text:
			print(f"[Azure] Storage account not found: {account}")
	except:
		pass
