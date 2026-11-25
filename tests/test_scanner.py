import pytest
from unittest.mock import patch, MagicMock
from scanner import parse_ports, portscan


def test_single_port():
    assert parse_ports("80") == [80]


def test_multiple_ports():
    assert parse_ports("22,80,443") == [22, 80, 443]


def test_port_range():
    assert parse_ports("1-5") == [1, 2, 3, 4, 5]


def test_invalid_port():
    with pytest.raises(ValueError):
        parse_ports("abc")


def test_port_out_of_range():
    with pytest.raises(ValueError):
        parse_ports("70000")


def test_inverted_range():
    with pytest.raises(ValueError):
        parse_ports("100-1")


def test_lower_limit():
    assert parse_ports("1") == [1]


def test_upper_limit():
    assert parse_ports("65535") == [65535]


def test_port_zero():
    with pytest.raises(ValueError):
        parse_ports("0")


def test_negative_number():
    with pytest.raises(ValueError):
        parse_ports("-1")


def test_range_with_text():
    with pytest.raises(ValueError):
        parse_ports("abc-abc")


def test_empty_element():
    with pytest.raises(ValueError):
        parse_ports("80,,443")


def test_duplicated_interval():
    assert parse_ports("80-80") == [80]


def test_duplicate_ports():
    assert parse_ports("80,443,80,22,443") == [80, 443, 22]


def test_invalid_range_format():
    with pytest.raises(ValueError):
        parse_ports("80-90-100")


def test_portscan_open():
    with patch("scanner.socket.socket") as mock_socket:
        mock_socket.return_value.connect.return_value = None

        result = portscan(80, "127.0.0.1")

        assert result == "80/tcp → open"


def test_portscan_closed():
    with patch("scanner.socket.socket") as mock_socket:
        mock_socket.return_value.connect.side_effect = ConnectionRefusedError

        result = portscan(80, "127.0.0.1")

        assert result == "80/tcp → closed"


def test_portscan_timeout():
    with patch("scanner.socket.socket") as mock_socket:
        mock_socket.return_value.connect.side_effect = TimeoutError

        result = portscan(80, "127.0.0.1")

        assert result == "80/tcp → inconclusive (timeout)"


def test_portscan_socket_error():
    with patch("scanner.socket.socket") as mock_socket:
        mock_socket.return_value.connect.side_effect = OSError("Network is unreachable")

        result = portscan(80, "127.0.0.1")

        assert result == "80/tcp → error (Network is unreachable)"
