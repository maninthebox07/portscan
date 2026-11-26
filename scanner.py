import socket


def validate_port(port: int) -> bool:
    """
    Check whether a port number is within the valid range.

    Args:
        port: Port number to validate.

    Returns:
        True if the port is valid, False otherwise.
    """
    return isinstance(port, int) and not isinstance(port, bool) and 1 <= port <= 65535


def parse_ports(port_spec: str) -> list[int]:
    """
    Parse a port specification into a list of unique port numbers.

    Accepts a single port, a comma-separated list, or an interval.

    Args:
        port_spec: Port specification to parse.

    Returns:
        A list of unique port numbers, preserving their original order.

    Raises:
        ValueError: If the port specification is invalid.
    """
    ports = []

    if "-" in port_spec:
        if port_spec.count("-") != 1:
            raise ValueError("Error: invalid port interval")

        start, end = port_spec.split("-")
        try:
            start, end = int(start), int(end)
        except ValueError:
            raise ValueError("Error: invalid port interval")

        if start <= end:
            ports = list(range(start, end + 1))
        else:
            raise ValueError("Error: invalid port interval")

    elif "," in port_spec:
        split_ports = port_spec.split(",")

        try:
            ports = [int(port) for port in split_ports]
        except ValueError:
            raise ValueError("Error: invalid port sequence")
    else:
        try:
            ports = [int(port_spec)]
        except ValueError:
            raise ValueError("Error: invalid port value")

    for port in ports:
        if not validate_port(port):
            raise ValueError("Error: invalid entry")

    return list(dict.fromkeys(ports))


def portscan(p: int, h: str, t: float = 0.5) -> str:
    """
    Scan a TCP port on a target host.

    Args:
        p: TCP port number to scan.
        h: Target host IP address.
        t: Connection timeout in seconds.

    Returns:
        A string describing the port status: open, closed,
        inconclusive, or error.

    Raises:
        ValueError: If the port number is invalid.
    """
    if not validate_port(p):
        raise ValueError("Error: the port number must be between 1-65535.")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(t)

    try:
        s.connect((h, p))
        return f"{p}/tcp → open"
    except TimeoutError:
        return f"{p}/tcp → inconclusive (timeout)"
    except ConnectionRefusedError:
        return f"{p}/tcp → closed"
    except OSError as e:
        return f"{p}/tcp → error ({e.strerror or str(e)})"
    finally:
        s.close()
