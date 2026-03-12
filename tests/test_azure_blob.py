from unittest.mock import patch, MagicMock


def test_account_not_found(load_checker, capsys):
    checker = load_checker("azure_blob")
    mock_resp = MagicMock(status_code=400, text="<Error><Code>AccountNotFound</Code></Error>")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://myaccount.blob.core.windows.net/container/blob")
    assert "myaccount" in capsys.readouterr().out


def test_account_exists(load_checker, capsys):
    checker = load_checker("azure_blob")
    mock_resp = MagicMock(status_code=403, text="AuthorizationRequired")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://existingaccount.blob.core.windows.net/container/blob")
    assert capsys.readouterr().out == ""


def test_cache(load_checker):
    checker = load_checker("azure_blob")
    mock_resp = MagicMock(status_code=400, text="AccountNotFound")
    with patch("requests.get", return_value=mock_resp) as mock_get:
        checker.check("https://sameaccount.blob.core.windows.net/a")
        checker.check("https://sameaccount.blob.core.windows.net/b")
    assert mock_get.call_count == 1
