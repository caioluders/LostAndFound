from unittest.mock import patch, MagicMock


def test_package_not_found(load_checker, capsys):
    checker = load_checker("packagist")
    mock_resp = MagicMock(status_code=404, text="Not Found")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://packagist.org/packages/vendor/nonexistent-pkg")
    assert "[Packagist]" in capsys.readouterr().out


def test_package_exists(load_checker, capsys):
    checker = load_checker("packagist")
    mock_resp = MagicMock(status_code=200, text='{"package":{"name":"monolog/monolog"}}')
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://packagist.org/packages/monolog/monolog")
    assert capsys.readouterr().out == ""


def test_non_package_url(load_checker):
    checker = load_checker("packagist")
    with patch("requests.get") as mock_get:
        checker.check("https://packagist.org/about")
    mock_get.assert_not_called()
