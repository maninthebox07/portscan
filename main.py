import socket
import sys
import ipaddress
import argparse
from scanner import parse_ports, portscan
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from output import save_results

TARGET = None

parser = argparse.ArgumentParser(
    description="TCP port scanner",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument("host", help="Hostname or IPv4 address to scan.")

parser.add_argument(
    "-p",
    "--port",
    required=True,
    metavar="PORTS",
    help="Port(s) to scan. Accepts a single port, a comma-separated list or a range.",
)

parser.add_argument(
    "-t",
    "--timeout",
    type=float,
    default=0.5,
    metavar="SECONDS",
    help="Connection timeout.",
)

parser.add_argument(
    "-w",
    "--workers",
    type=int,
    default=10,
    metavar="N",
    help="Maximum number of concurrent workers.",
)

parser.add_argument(
    "-o",
    "--open",
    action="store_true",
    help="Show only open ports.",
)

parser.add_argument(
    "-O",
    "--output",
    type=str,
    default=None,
    metavar="FILE",
    help="Save scan results to a file.",
)

args = parser.parse_args()

if args.workers < 1:
    parser.error("workers must be at least 1")

if args.timeout <= 0:
    parser.error("timeout must be greater than 0")

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

found_open = False
results = []

with ThreadPoolExecutor(max_workers=args.workers) as executor:
    for line in executor.map(scan, ports):
        if not args.open or line.endswith("→ open"):
            print(line)
            results.append(line)

            if line.endswith("→ open"):
                found_open = True

if args.output is not None:
    try:
        save_results(results, args.output)
        print(f"Results saved to {args.output}")
    except OSError as e:
        print(f"Error saving results: {e}")
        sys.exit(1)

if args.open and not found_open:
    print("No open ports found.")
