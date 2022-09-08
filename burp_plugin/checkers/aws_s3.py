base_domains = ["*.s3.amazonaws.com","s3*.amazonaws.com"]
cache_domains = set()

def check(request_url, response_body, response_status_code):

	if response_status_code == 404 and "NoSuchBucket" in response_body :
		return True
	else :
		return False