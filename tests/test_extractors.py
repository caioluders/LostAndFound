import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from extractors.from_string import extract


def test_basic_https():
    urls = extract("visit https://example.com for info")
    assert "https://example.com" in urls


def test_http_with_path():
    urls = extract("http://example.com/path/to/page")
    assert "http://example.com/path/to/page" in urls


def test_query_string():
    urls = extract("https://example.com/path?a=1&b=2")
    assert "https://example.com/path?a=1&b=2" in urls


def test_port():
    urls = extract("https://example.com:8080/path")
    assert "https://example.com:8080/path" in urls


def test_s3_protocol():
    urls = extract("s3://my-bucket/key/file.txt")
    assert "s3://my-bucket/key/file.txt" in urls


def test_gs_protocol():
    urls = extract("gs://my-bucket/file.txt")
    assert "gs://my-bucket/file.txt" in urls


def test_json_escaped_slashes():
    urls = extract(r'{"url":"https:\/\/example.com\/api\/v1"}')
    assert "https://example.com/api/v1" in urls


def test_trailing_comma():
    urls = extract("https://example.com, and more")
    assert "https://example.com" in urls


def test_trailing_period():
    urls = extract("Visit https://example.com.")
    assert "https://example.com" in urls


def test_trailing_paren_in_markdown():
    urls = extract("[link](https://github.com/user/repo)")
    assert "https://github.com/user/repo" in urls


def test_balanced_parens_preserved():
    urls = extract("https://en.wikipedia.org/wiki/Foo_(bar)")
    assert "https://en.wikipedia.org/wiki/Foo_(bar)" in urls


def test_www_prefix():
    urls = extract("www.example.com/page")
    assert "www.example.com/page" in urls


def test_multiple_urls():
    text = "see https://one.com and https://two.com"
    urls = extract(text)
    assert "https://one.com" in urls
    assert "https://two.com" in urls


def test_deduplication():
    text = "https://example.com https://example.com https://example.com"
    urls = extract(text)
    assert urls.count("https://example.com") == 1


def test_ftp():
    urls = extract("ftp://files.example.com/pub")
    assert "ftp://files.example.com/pub" in urls


def test_presigned_s3_url():
    url = "https://bucket.s3.eu-central-1.amazonaws.com/key?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA"
    urls = extract(url)
    assert any("bucket.s3.eu-central-1.amazonaws.com" in u for u in urls)
