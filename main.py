import socket
import sys
import ipaddress

HOST = input("Enter a host: ")
PORT = input("Enter a port: ")
TARGET = None


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


try:
    TARGET = str(ipaddress.ip_address(HOST))
except ValueError:
    try:
        TARGET = socket.getaddrinfo(HOST, None, socket.AF_INET)
        TARGET = TARGET[0][4][0]
    except socket.gaierror:
        print("Error: unable to resolve host.")
        sys.exit()

if "-" in PORT:
    PORT = PORT.split("-")

    try:
        if (
            validate_port(int(PORT[0]))
            and validate_port(int(PORT[1]))
            and int(PORT[0]) <= int(PORT[1])
        ):
            for port in range(int(PORT[0]), int(PORT[1]) + 1):
                portscan(TARGET, port)
        else:
            print("Error: invalid entry. Please, enter a valid interval.")

    except ValueError:
        print("Error: invalid entry. Please, enter a valid interval.")
        sys.exit()
elif "," in PORT:
    PORT = PORT.split(",")

    try:
        for port in PORT:
            portscan(TARGET, int(port))
    except ValueError:
        print("Error: invalid entry. Please, enter a valid port number.")
else:
    try:
        portscan(TARGET, int(PORT))
    except ValueError:
        print("Error: invalid entry. Please, enter a valid port number.")
        sys.exit()
