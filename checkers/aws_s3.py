import requests, urllib

base_domains = ["*.s3.amazonaws.com","s3*.amazonaws.com"]
cache_domains = set()


def check(url):

	r = requests.get(url)

	if r.status_code == 404 and "NoSuchBucket" in r.text :
		print("[!] S3 Bucket not found:",url)
