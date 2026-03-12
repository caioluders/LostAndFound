from unittest.mock import patch, MagicMock


def test_unregistered(load_checker, capsys):
    checker = load_checker("bitbucket")
    mock_resp = MagicMock(status_code=404, text="Resource not found")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://bitbucket.org/nonexistent123")
    assert "Bitbucket unregistred username" in capsys.readouterr().out


def test_registered(load_checker, capsys):
    checker = load_checker("bitbucket")
    mock_resp = MagicMock(status_code=200, text="<html>profile</html>")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://bitbucket.org/atlassian")
    assert capsys.readouterr().out == ""
