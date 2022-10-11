import fnmatch

def clean_url(url):
    if type(url) == bytes:
        url = url.decode('utf-8')

    url = url.split("//")
    url = "https://"+url[1] if len(url)>1 else "https://"+url[0]
    return url


def fnmatch_all(text, filters):
    for f in filters:
        if fnmatch.fnmatch(text, f) :
            return True
