from unittest.mock import patch, MagicMock


def test_unregistered_username(load_checker, capsys):
    checker = load_checker("github")
    mock_resp = MagicMock(status_code=404)
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://github.com/nonexistentuser123")
    assert "Github unregistred username" in capsys.readouterr().out


def test_registered_username(load_checker, capsys):
    checker = load_checker("github")
    mock_resp = MagicMock(status_code=200)
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://github.com/torvalds")
    assert capsys.readouterr().out == ""


def test_deny_list(load_checker, capsys):
    checker = load_checker("github")
    with patch("requests.get") as mock_get:
        checker.check("https://github.com/orgs/worldcoin/teams")
    mock_get.assert_not_called()


def test_cache(load_checker):
    checker = load_checker("github")
    mock_resp = MagicMock(status_code=404)
    with patch("requests.get", return_value=mock_resp) as mock_get:
        checker.check("https://github.com/testuser999")
        checker.check("https://github.com/testuser999")
    assert mock_get.call_count == 1


def test_deep_path(load_checker, capsys):
    checker = load_checker("github")
    mock_resp = MagicMock(status_code=404)
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://github.com/someuser/somerepo/blob/main/file.py")
    assert "someuser" in capsys.readouterr().out
