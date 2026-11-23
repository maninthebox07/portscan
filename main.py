import socket
import sys
import ipaddress
from scanner import validate_port, portscan

HOST = input("Enter a host: ")
PORT = input("Enter a port: ")
TARGET = None

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
            if not validate_port(int(port)):
                print("Error: the port numbers on the list must be between 1-65535.")
                sys.exit()

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
