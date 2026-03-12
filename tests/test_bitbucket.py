from unittest.mock import patch, MagicMock


def test_unregistered(load_checker, capsys):
    checker = load_checker("bitbucket")
    mock_resp = MagicMock(status_code=404, text="Resource not found")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://bitbucket.org/nonexistent123")
    assert "unregistered username" in capsys.readouterr().out


def test_registered(load_checker, capsys):
    checker = load_checker("bitbucket")
    mock_resp = MagicMock(status_code=200, text="<html>profile</html>")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://bitbucket.org/atlassian")
    assert capsys.readouterr().out == ""


def test_renamed_user_with_redirect(load_checker, capsys):
    """Renamed user with repo redirect should not be flagged."""
    checker = load_checker("bitbucket")
    mock_404 = MagicMock(status_code=404, text="Resource not found")
    mock_301 = MagicMock(status_code=301)
    with patch("requests.get", return_value=mock_404), \
         patch("requests.head", return_value=mock_301):
        checker.check("https://bitbucket.org/olduser/somerepo")
    assert capsys.readouterr().out == ""
