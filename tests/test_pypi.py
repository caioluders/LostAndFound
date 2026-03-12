from unittest.mock import patch, MagicMock


def test_package_not_found(load_checker, capsys):
    checker = load_checker("pypi")
    mock_resp = MagicMock(status_code=404, text="Not Found")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://pypi.org/project/nonexistent-pkg-12345/")
    assert "[PyPI]" in capsys.readouterr().out


def test_package_exists(load_checker, capsys):
    checker = load_checker("pypi")
    mock_resp = MagicMock(status_code=200, text='{"info":{"name":"requests"}}')
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://pypi.org/project/requests/")
    assert capsys.readouterr().out == ""


def test_pypi_json_url(load_checker, capsys):
    checker = load_checker("pypi")
    mock_resp = MagicMock(status_code=404, text="Not Found")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://pypi.org/pypi/nonexistent-pkg/json")
    assert "[PyPI]" in capsys.readouterr().out
