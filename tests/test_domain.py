def test_clean_domain_basic(load_checker):
    mod = load_checker("domain")
    assert mod.clean_domain("sub.example.com") == "example.com"


def test_clean_domain_trailing_junk(load_checker):
    mod = load_checker("domain")
    assert mod.clean_domain("example.com)") == "example.com"


def test_clean_domain_invalid_tld(load_checker):
    mod = load_checker("domain")
    assert mod.clean_domain("something.invalidtld") is False


def test_clean_domain_simple(load_checker):
    mod = load_checker("domain")
    assert mod.clean_domain("github.com") == "github.com"
