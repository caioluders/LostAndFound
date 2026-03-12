from urlparse import urlparse

base_domains = ["firebaseio.com", "*.firebasedatabase.app", "firebaseapp.com"]
name = "Firebase"
severity = "Medium"


def check(request_url, response_body, response_status_code):
    parsed = urlparse(request_url)
    netloc = parsed.netloc

    # extract project name from {project}.firebaseio.com etc
    project = netloc.split(".")[0]

    if not project:
        return None

    if response_status_code == 404 or "PROJECT_NOT_FOUND" in response_body:
        return {"detail": "Firebase project not found: %s" % project}

    return None
