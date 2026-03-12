from urlparse import urlparse

base_domains = ["github.com"]
name = "GitHub"
severity = "Medium"

deny_list_usernames = [
    "orgs", "features", "marketplace", "explore", "topics", "trending",
    "collections", "events", "sponsors", "settings", "notifications",
    "login", "join", "new", "about", "pricing", "security", "enterprise",
    "team", "customer-stories",
]


def check(request_url, response_body, response_status_code):
    parsed = urlparse(request_url)
    path_parts = parsed.path.strip("/").split("/")

    if not path_parts or not path_parts[0]:
        return None

    username = path_parts[0].lower()

    if username in deny_list_usernames:
        return None

    allowed = "abcdefghijklmnopqrstuvwxyz0123456789-"
    if not all(c in allowed for c in username):
        return None

    if response_status_code == 404:
        return {"detail": "Unregistered GitHub username: %s" % username}

    return None
