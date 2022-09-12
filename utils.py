import fnmatch

def clean_url(url):
	url = url.split(b"//")
	url = b"https://"+url[1] if len(url)>1 else b"https://"+url[0]

	return url


def fnmatch_all(text, filters):
	for f in filters:
		if fnmatch.fnmatch(text, f) :
			return True
