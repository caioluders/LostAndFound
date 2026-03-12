from urlparse import urlparse

base_domains = ["packagist.org"]
name = "Packagist"
severity = "Medium"


def check(request_url, response_body, response_status_code):
    parsed = urlparse(request_url)
    path_parts = parsed.path.strip("/").split("/")

    # packagist.org/packages/{vendor}/{package}
    if len(path_parts) < 3 or path_parts[0] != "packages":
        return None

    vendor = path_parts[1]
    package = path_parts[2]

    if response_status_code == 404:
        return {"detail": "Packagist package not found: %s/%s" % (vendor, package)}

    return None
