from urlparse import urlparse

base_domains = ["bitbucket.org"]
cache_domains = set()

def check(request_url, response_body, response_status_code):

	parsed_url = urlparse(request_url)

	if response_status_code == 404 and "Resource not found" in response_body :
		return True
	else :
		return False