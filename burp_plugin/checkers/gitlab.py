from urlparse import urlparse

base_domains = ["gitlab.com"]
name = "GitLab"
severity = "Medium"


def check(request_url, response_body, response_status_code):
    parsed = urlparse(request_url)
    path_parts = parsed.path.strip("/").split("/")

    if not path_parts or not path_parts[0]:
        return None

    username = path_parts[0]

    if response_status_code == 302 and "You are being" in response_body:
        return {"detail": "Unregistered GitLab username: %s" % username}

    return None
