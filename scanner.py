import socket

def validate_port(port):
    return not (port < 1 or port > 65535)


def portscan(h, p):
    if not validate_port(p):
        print("Error: the port number must be between 1-65535.")
        sys.exit()
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        try:
            s.connect((h, p))
            print(f"{p}/tcp → open")
        except TimeoutError:
            print(f"{p}/tcp → inconclusive (timeout)")
        except ConnectionRefusedError:
            print(f"{p}/tcp → closed")
        finally:
            s.close()