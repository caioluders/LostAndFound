from unittest.mock import patch, MagicMock


def test_package_not_found(load_checker, capsys):
    checker = load_checker("npm")
    mock_resp = MagicMock(status_code=404, text='{"error":"Not found"}')
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://www.npmjs.com/package/nonexistent-pkg-12345")
    assert "[npm]" in capsys.readouterr().out


def test_package_exists(load_checker, capsys):
    checker = load_checker("npm")
    mock_resp = MagicMock(status_code=200, text='{"name":"express"}')
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://www.npmjs.com/package/express")
    assert capsys.readouterr().out == ""


def test_non_package_url(load_checker):
    checker = load_checker("npm")
    with patch("requests.get") as mock_get:
        checker.check("https://www.npmjs.com/about")
    mock_get.assert_not_called()


def test_scoped_package(load_checker, capsys):
    checker = load_checker("npm")
    mock_resp = MagicMock(status_code=404, text='{"error":"Not found"}')
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://www.npmjs.com/package/@scope/my-pkg")
    assert "[npm]" in capsys.readouterr().out
