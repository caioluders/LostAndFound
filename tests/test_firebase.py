from unittest.mock import patch, MagicMock


def test_project_not_found(load_checker, capsys):
    checker = load_checker("firebase")
    mock_resp = MagicMock(status_code=404, text='{"error":"PROJECT_NOT_FOUND"}')
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://myproject.firebaseio.com/data")
    assert "myproject" in capsys.readouterr().out


def test_project_exists(load_checker, capsys):
    checker = load_checker("firebase")
    mock_resp = MagicMock(status_code=200, text='{"users":{"a":1}}')
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://existingproject.firebaseio.com/")
    assert capsys.readouterr().out == ""


def test_firebaseapp(load_checker, capsys):
    checker = load_checker("firebase")
    mock_resp = MagicMock(status_code=404, text="PROJECT_NOT_FOUND")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://myapp.firebaseapp.com/page")
    assert "[Firebase]" in capsys.readouterr().out
