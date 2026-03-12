from unittest.mock import patch, MagicMock


def test_gem_not_found(load_checker, capsys):
    checker = load_checker("rubygems")
    mock_resp = MagicMock(status_code=404, text="This rubygem could not be found.")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://rubygems.org/gems/nonexistent-gem-12345")
    assert "[RubyGems]" in capsys.readouterr().out


def test_gem_exists(load_checker, capsys):
    checker = load_checker("rubygems")
    mock_resp = MagicMock(status_code=200, text='{"name":"rails"}')
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://rubygems.org/gems/rails")
    assert capsys.readouterr().out == ""


def test_non_gem_url(load_checker):
    checker = load_checker("rubygems")
    with patch("requests.get") as mock_get:
        checker.check("https://rubygems.org/pages/about")
    mock_get.assert_not_called()
