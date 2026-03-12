import requests, urllib

base_domains = ["*.s3.amazonaws.com","*.s3.*.amazonaws.com","s3*.amazonaws.com"]
cache_domains = set()


def check(url):
	parsed = urllib.parse.urlparse(url)
	netloc = parsed.netloc

	# path-style: s3.amazonaws.com/bucket-name/...
	if netloc.startswith("s3") and not netloc.split(".")[0].replace("s3",""):
		parts = parsed.path.strip("/").split("/")
		if not parts or not parts[0]:
			return
		bucket = parts[0]
		bucket_url = f"https://s3.amazonaws.com/{bucket}"
	else:
		# virtual-hosted: bucket-name.s3[.region].amazonaws.com
		bucket = netloc.split(".s3")[0]
		bucket_url = f"https://{bucket}.s3.amazonaws.com/"

	if bucket_url in cache_domains:
		return
	cache_domains.add(bucket_url)

	try:
		r = requests.get(bucket_url, verify=False, timeout=10)
		if r.status_code == 404 and "NoSuchBucket" in r.text:
			print(f"[S3] Bucket not found: {bucket}")
	except:
		pass