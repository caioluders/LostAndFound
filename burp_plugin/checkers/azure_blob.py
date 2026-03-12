from urlparse import urlparse

base_domains = ["*.blob.core.windows.net"]
name = "Azure Blob Storage"
severity = "High"


def check(request_url, response_body, response_status_code):
    parsed = urlparse(request_url)
    netloc = parsed.netloc

    # {account}.blob.core.windows.net
    account = netloc.replace(".blob.core.windows.net", "")

    if not account or "." in account:
        return None

    if "AccountNotFound" in response_body or "InvalidResourceName" in response_body:
        return {"detail": "Azure storage account not found: %s" % account}

    return None
