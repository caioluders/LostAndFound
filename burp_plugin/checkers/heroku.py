from urlparse import urlparse

base_domains = ["herokuapp.com", "herokussl.com", "herokudns.com"]
name = "Heroku"
severity = "Medium"


def check(request_url, response_body, response_status_code):
    parsed = urlparse(request_url)
    netloc = parsed.netloc

    if "No such app" in response_body or "herokucdn.com/error-pages/no-such-app" in response_body:
        return {"detail": "Heroku app not found: %s" % netloc}

    return None
