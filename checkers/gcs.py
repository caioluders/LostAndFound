import requests, urllib

base_domains = ["storage.googleapis.com", "*.storage.googleapis.com"]
cache_domains = set()


def check(url):
	parsed = urllib.parse.urlparse(url)
	netloc = parsed.netloc

	# path-style: storage.googleapis.com/bucket-name/...
	if netloc == "storage.googleapis.com":
		parts = parsed.path.strip("/").split("/")
		if not parts or not parts[0]:
			return
		bucket = parts[0]
	else:
		# virtual-hosted: bucket-name.storage.googleapis.com
		bucket = netloc.replace(".storage.googleapis.com", "")

	if not bucket:
		return

	bucket_url = f"https://storage.googleapis.com/{bucket}"

	if bucket_url in cache_domains:
		return
	cache_domains.add(bucket_url)

	try:
		r = requests.head(bucket_url, timeout=10)
		if r.status_code == 404:
			print(f"[GCS] Bucket not found: {bucket}")
	except:
		pass
