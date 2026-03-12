from unittest.mock import patch, MagicMock


def test_unregistered(load_checker, capsys):
    checker = load_checker("gitlab")
    mock_resp = MagicMock(status_code=302, text='<html><body>You are being <a href="...">redirected</a>.</body></html>')
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://gitlab.com/nonexistentuser123")
    assert "unregistered username" in capsys.readouterr().out


def test_registered(load_checker, capsys):
    checker = load_checker("gitlab")
    mock_resp = MagicMock(status_code=200, text="<html>profile page</html>")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://gitlab.com/gitlab-org")
    assert capsys.readouterr().out == ""


def test_renamed_user_with_redirect(load_checker, capsys):
    """Renamed user with repo redirect should not be flagged."""
    checker = load_checker("gitlab")
    mock_302 = MagicMock(status_code=302, text='You are being redirected')
    mock_301 = MagicMock(status_code=301)
    with patch("requests.get", return_value=mock_302), \
         patch("requests.head", return_value=mock_301):
        checker.check("https://gitlab.com/olduser/somerepo")
    assert capsys.readouterr().out == ""
