from unittest.mock import patch, MagicMock


def test_virtual_hosted_not_found(load_checker, capsys):
    checker = load_checker("aws_s3")
    mock_resp = MagicMock(status_code=404, text="<Error><Code>NoSuchBucket</Code></Error>")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://mybucket.s3.amazonaws.com/key.txt")
    assert "mybucket" in capsys.readouterr().out


def test_regional_not_found(load_checker, capsys):
    checker = load_checker("aws_s3")
    mock_resp = MagicMock(status_code=404, text="<Error><Code>NoSuchBucket</Code></Error>")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://mybucket.s3.eu-central-1.amazonaws.com/obj?X-Amz-Algorithm=test")
    assert "mybucket" in capsys.readouterr().out


def test_path_style_not_found(load_checker, capsys):
    checker = load_checker("aws_s3")
    mock_resp = MagicMock(status_code=404, text="<Error><Code>NoSuchBucket</Code></Error>")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://s3.amazonaws.com/mybucket/key.txt")
    assert "mybucket" in capsys.readouterr().out


def test_bucket_exists(load_checker, capsys):
    checker = load_checker("aws_s3")
    mock_resp = MagicMock(status_code=403, text="AccessDenied")
    with patch("requests.get", return_value=mock_resp):
        checker.check("https://existingbucket.s3.amazonaws.com/file")
    assert capsys.readouterr().out == ""


def test_cache(load_checker):
    checker = load_checker("aws_s3")
    mock_resp = MagicMock(status_code=404, text="NoSuchBucket")
    with patch("requests.get", return_value=mock_resp) as mock_get:
        checker.check("https://samebucket.s3.amazonaws.com/file1")
        checker.check("https://samebucket.s3.amazonaws.com/file2")
    assert mock_get.call_count == 1
