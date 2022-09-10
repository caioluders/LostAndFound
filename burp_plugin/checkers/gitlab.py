import urllib

base_domains = ["gitlab.com"]
cache_domains = set()


def check(request_url, response_body, response_status_code):
	
	if url not in cache_domains :
		cache_domains.add(url) 


		if response_status_code == 302 and "You are being" in response_body :
			return True
		else :
			return False