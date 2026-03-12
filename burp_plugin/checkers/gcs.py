from urlparse import urlparse

base_domains = ["storage.googleapis.com", "*.storage.googleapis.com"]
name = "Google Cloud Storage"
severity = "High"


def check(request_url, response_body, response_status_code):
    parsed = urlparse(request_url)
    netloc = parsed.netloc

    # path-style: storage.googleapis.com/bucket-name/...
    if netloc == "storage.googleapis.com":
        parts = parsed.path.strip("/").split("/")
        if not parts or not parts[0]:
            return None
        bucket = parts[0]
    else:
        # virtual-hosted: bucket-name.storage.googleapis.com
        bucket = netloc.replace(".storage.googleapis.com", "")

    if not bucket:
        return None

    if response_status_code == 404:
        return {"detail": "GCS bucket not found: %s" % bucket}

    return None
