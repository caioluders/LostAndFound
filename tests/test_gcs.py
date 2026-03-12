from unittest.mock import patch, MagicMock


def test_path_style_not_found(load_checker, capsys):
    checker = load_checker("gcs")
    mock_resp = MagicMock(status_code=404)
    with patch("requests.head", return_value=mock_resp):
        checker.check("https://storage.googleapis.com/mybucket/object.txt")
    assert "mybucket" in capsys.readouterr().out


def test_virtual_hosted_not_found(load_checker, capsys):
    checker = load_checker("gcs")
    mock_resp = MagicMock(status_code=404)
    with patch("requests.head", return_value=mock_resp):
        checker.check("https://mybucket.storage.googleapis.com/object.txt")
    assert "mybucket" in capsys.readouterr().out


def test_bucket_exists_403(load_checker, capsys):
    checker = load_checker("gcs")
    mock_resp = MagicMock(status_code=403)
    with patch("requests.head", return_value=mock_resp):
        checker.check("https://storage.googleapis.com/existingbucket/file")
    assert capsys.readouterr().out == ""


def test_cache(load_checker):
    checker = load_checker("gcs")
    mock_resp = MagicMock(status_code=404)
    with patch("requests.head", return_value=mock_resp) as mock_head:
        checker.check("https://storage.googleapis.com/samebucket/file1")
        checker.check("https://storage.googleapis.com/samebucket/file2")
    assert mock_head.call_count == 1
