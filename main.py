import socket
import sys
import ipaddress
import argparse
from scanner import validate_port, portscan

TARGET = None

parser = argparse.ArgumentParser()

parser.add_argument("host")
parser.add_argument("-p", "--port", required=True)
parser.add_argument("-t", "--timeout", type=float, default=0.5)

args = parser.parse_args()

try:
    TARGET = str(ipaddress.ip_address(args.host))
except ValueError:
    try:
        TARGET = socket.getaddrinfo(args.host, None, socket.AF_INET)
        TARGET = TARGET[0][4][0]
    except socket.gaierror:
        print("Error: unable to resolve host.")
        sys.exit()

if "-" in args.port:
    args.port = args.port.split("-")

    try:
        if (
            validate_port(int(args.port[0]))
            and validate_port(int(args.port[1]))
            and int(args.port[0]) <= int(args.port[1])
        ):
            for port in range(int(args.port[0]), int(args.port[1]) + 1):
                portscan(TARGET, port, args.timeout)
        else:
            print("Error: invalid entry. Please, enter a valid interval.")

    except ValueError:
        print("Error: invalid entry. Please, enter a valid interval.")
        sys.exit()
elif "," in args.port:
    args.port = args.port.split(",")

    try:
        for port in args.port:
            if not validate_port(int(port)):
                print("Error: the port numbers on the list must be between 1-65535.")
                sys.exit()

        for port in args.port:
            portscan(TARGET, int(port), args.timeout)
    except ValueError:
        print("Error: invalid entry. Please, enter a valid port number.")
else:
    try:
        portscan(TARGET, int(args.port), args.timeout)
    except ValueError:
        print("Error: invalid entry. Please, enter a valid port number.")
        sys.exit()