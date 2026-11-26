import socket


def validate_port(port):
    return isinstance(port, int) and not isinstance(port, bool) and 1 <= port <= 65535


def parse_ports(port_spec):
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


def portscan(p, h, t=0.5):
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
