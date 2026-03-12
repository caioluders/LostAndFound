from urlparse import urlparse

base_domains = ["npmjs.com", "npmjs.org"]
name = "npm"
severity = "Medium"


def check(request_url, response_body, response_status_code):
    parsed = urlparse(request_url)
    path_parts = parsed.path.strip("/").split("/")

    # npmjs.com/package/{name} or npmjs.com/package/{@scope}/{name}
    if len(path_parts) < 2 or path_parts[0] != "package":
        return None

    package = "/".join(path_parts[1:])

    if response_status_code == 404:
        return {"detail": "npm package not found: %s" % package}

    return None
