from urlparse import urlparse

base_domains = ["github.com"]
cache_domains = set()

def check(request_url, response_body, response_status_code):

	parsed_url = urlparse(request_url)

	if response_status_code == 404 :
		return True
	else :
		return False