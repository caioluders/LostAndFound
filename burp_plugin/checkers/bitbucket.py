from urlparse import urlparse

base_domains = ["bitbucket.org"]
name = "Bitbucket"
severity = "Medium"


def check(request_url, response_body, response_status_code):
    parsed = urlparse(request_url)
    path_parts = parsed.path.strip("/").split("/")

    if not path_parts or not path_parts[0]:
        return None

    username = path_parts[0]

    if response_status_code == 404 and "Resource not found" in response_body:
        return {"detail": "Unregistered Bitbucket username: %s" % username}

    return None
