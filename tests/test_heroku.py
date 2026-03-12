from unittest.mock import patch, MagicMock


def test_no_such_app(load_checker, capsys):
    checker = load_checker("heroku")
    mock_resp = MagicMock(status_code=404, text="<html><head><title>No such app</title></head></html>")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://myapp.herokuapp.com/path")
    assert "myapp.herokuapp.com" in capsys.readouterr().out


def test_app_exists(load_checker, capsys):
    checker = load_checker("heroku")
    mock_resp = MagicMock(status_code=200, text="<html>Welcome to my app</html>")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://existingapp.herokuapp.com/")
    assert capsys.readouterr().out == ""


def test_herokussl(load_checker, capsys):
    checker = load_checker("heroku")
    mock_resp = MagicMock(status_code=404, text="No such app")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://myapp.herokussl.com")
    assert "[Heroku]" in capsys.readouterr().out
