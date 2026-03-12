from urlparse import urlparse

base_domains = ["rubygems.org"]
name = "RubyGems"
severity = "Medium"


def check(request_url, response_body, response_status_code):
    parsed = urlparse(request_url)
    path_parts = parsed.path.strip("/").split("/")

    # rubygems.org/gems/{name}
    if len(path_parts) < 2 or path_parts[0] != "gems":
        return None

    gem = path_parts[1]

    if response_status_code == 404:
        return {"detail": "RubyGems gem not found: %s" % gem}

    return None
