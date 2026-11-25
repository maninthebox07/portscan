import socket
import sys
import ipaddress
import argparse
from scanner import parse_ports, portscan
from concurrent.futures import ThreadPoolExecutor
from functools import partial

TARGET = None

parser = argparse.ArgumentParser()

parser.add_argument("host")
parser.add_argument("-p", "--port", required=True)
parser.add_argument("-t", "--timeout", type=float, default=0.5)
parser.add_argument("-w", "--workers", type=int, default=10)

args = parser.parse_args()

if args.workers < 1:
    parser.error("workers must be at least 1")

try:
    TARGET = str(ipaddress.ip_address(args.host))
except ValueError:
    try:
        TARGET = socket.getaddrinfo(args.host, None, socket.AF_INET)
        TARGET = TARGET[0][4][0]
    except socket.gaierror:
        print("Error: unable to resolve host.")
        sys.exit(1)

try:
    ports = parse_ports(args.port)
except ValueError as e:
    print(e)
    sys.exit(1)

scan = partial(portscan, h=TARGET, t=args.timeout)

with ThreadPoolExecutor(max_workers=args.workers) as executor:
    for line in executor.map(scan, ports):
        print(line)
