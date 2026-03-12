from urlparse import urlparse

base_domains = ["*.s3.amazonaws.com", "*.s3.*.amazonaws.com", "s3*.amazonaws.com"]
name = "AWS S3"
severity = "High"


def check(request_url, response_body, response_status_code):
    parsed = urlparse(request_url)
    netloc = parsed.netloc

    # path-style: s3.amazonaws.com/bucket or s3.region.amazonaws.com/bucket
    if netloc.startswith("s3") and not netloc.split(".")[0].replace("s3", ""):
        parts = parsed.path.strip("/").split("/")
        if not parts or not parts[0]:
            return None
        bucket = parts[0]
    else:
        # virtual-hosted: bucket.s3.amazonaws.com or bucket.s3.region.amazonaws.com
        bucket = netloc.split(".s3")[0]

    if not bucket:
        return None

    if response_status_code == 404 and "NoSuchBucket" in response_body:
        return {"detail": "S3 bucket not found: %s" % bucket}

    return None
