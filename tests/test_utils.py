import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils import clean_url, fnmatch_all


def test_clean_url_bytes():
    assert clean_url(b"https://example.com") == "https://example.com"


def test_clean_url_no_scheme():
    assert clean_url("www.example.com") == "https://www.example.com"


def test_clean_url_http():
    assert clean_url("http://example.com/path") == "https://example.com/path"


def test_fnmatch_all_match():
    assert fnmatch_all("test.s3.amazonaws.com", ["*.s3.amazonaws.com"]) is True


def test_fnmatch_all_no_match():
    assert fnmatch_all("example.com", ["*.s3.amazonaws.com"]) is None


def test_fnmatch_all_multiple_patterns():
    assert fnmatch_all("github.com", ["gitlab.com", "github.com"]) is True
