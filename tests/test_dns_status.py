import socket
from unittest.mock import patch


def test_unregistered_nxdomain(load_checker, capsys):
    checker = load_checker("dns_status")
    err = socket.gaierror(socket.EAI_NONAME, "Name or service not known")
    with patch("socket.gethostbyname", side_effect=err):
        checker.check("https://unregistered-domain-12345.com/path")
    assert "[DNS]" in capsys.readouterr().out


def test_registered(load_checker, capsys):
    checker = load_checker("dns_status")
    with patch("socket.gethostbyname", return_value="93.184.216.34"):
        checker.check("https://example.com/path")
    assert capsys.readouterr().out == ""


def test_timeout_not_flagged(load_checker, capsys):
    checker = load_checker("dns_status")
    err = socket.gaierror(socket.EAI_AGAIN, "Temporary failure in name resolution")
    with patch("socket.gethostbyname", side_effect=err):
        checker.check("https://slow-dns-domain.com/path")
    assert capsys.readouterr().out == ""
