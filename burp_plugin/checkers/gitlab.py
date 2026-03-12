import urllib

base_domains = ["gitlab.com"]
cache_domains = set()


def check(request_url, response_body, response_status_code):
	
	if request_url not in cache_domains :
		cache_domains.add(request_url) 


		if response_status_code == 302 and "You are being" in response_body :
			return True
		else :
			return False