from urlparse import urlparse

base_domains = ["pypi.org", "pypi.python.org"]
name = "PyPI"
severity = "Medium"


def check(request_url, response_body, response_status_code):
    parsed = urlparse(request_url)
    path_parts = parsed.path.strip("/").split("/")

    # pypi.org/project/{name}/ or pypi.org/pypi/{name}/json
    if len(path_parts) < 2:
        return None

    if path_parts[0] in ("project", "pypi"):
        package = path_parts[1]
    else:
        return None

    if response_status_code == 404:
        return {"detail": "PyPI package not found: %s" % package}

    return None
