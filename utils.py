import fnmatch
from xml.dom.minidom import TypeInfo

def clean_url(url):
	if type(url) == bytes:
		url = url.split(b"//")
		url = b"https://"+url[1] if len(url)>1 else b"https://"+url[0]
		url.decode("utf8")
	return url


def fnmatch_all(text, filters):
	for f in filters:
		if fnmatch.fnmatch(text, f) :
			return True
