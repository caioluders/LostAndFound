from unittest.mock import patch, MagicMock


def test_unregistered(load_checker, capsys):
    checker = load_checker("gitlab")
    mock_resp = MagicMock(status_code=302, text='<html><body>You are being <a href="...">redirected</a>.</body></html>')
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://gitlab.com/nonexistentuser123")
    assert "Gitlab unregistred username" in capsys.readouterr().out


def test_registered(load_checker, capsys):
    checker = load_checker("gitlab")
    mock_resp = MagicMock(status_code=200, text="<html>profile page</html>")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://gitlab.com/gitlab-org")
    assert capsys.readouterr().out == ""
