# Portscan

A lightweight TCP port scanner written in Python. It checks the status of TCP ports on a target host and reports whether they are open, closed, or inconclusive.

Created as an educational project to practice Python programming, computer networking, concurrency, and command-line interface development.

## Features

- Scan a single port, a comma-separated list, or a port range.
- Accept IPv4 addresses and domain names.
- Concurrent scanning using `ThreadPoolExecutor`.
- Configurable connection timeout and number of workers.
- Option to display only open ports.
- Export scan results to a text file.
- Error handling and input validation.

## Requirements

- Python 3.9 or newer.
- No external dependencies required to run the scanner.
- `pytest` is required only to run the test suite.

## Installation

Clone the repository:

```bash
git clone https://github.com/maninthebox07/portscan.git
cd portscan
```

Optionally, create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

## Usage

Run the scanner with:

```bash
python main.py HOST -p PORTS
```

### Examples

Replace the example hosts below with systems you own or have explicit permission to test.

Scan a single port:

```bash
python main.py 127.0.0.1 -p 80
```

Scan multiple ports:

```bash
python main.py example.com -p 22,80,443
```

Scan a range of ports:

```bash
python main.py 192.168.1.1 -p 1-1000
```

Set a custom timeout and number of workers:

```bash
python main.py 192.168.1.1 -p 1-1000 -t 1.0 -w 50
```

Display only open ports:

```bash
python main.py example.com -p 1-1000 --open
```

Save results to a text file:

```bash
python main.py example.com -p 1-1000 -O results.txt
```

Display all available arguments:

```bash
python main.py --help
```

### Command-line arguments

| Argument | Description | Default |
|---|---|---|
| `host` | Target IPv4 address or domain name | Required |
| `-p`, `--port` | Port, comma-separated ports, or range | Required |
| `-t`, `--timeout` | Connection timeout in seconds | `0.5` |
| `-w`, `--workers` | Maximum number of concurrent workers | `10` |
| `-o`, `--open` | Display only open ports | Disabled |
| `-O`, `--output` | Save results to a text file | Disabled |
| `-h`, `--help` | Display help information | — |

## Port Status

The scanner reports the following statuses:

- **Open:** The TCP connection was successfully established.
- **Closed:** The target refused the connection.
- **Inconclusive:** The connection timed out.
- **Error:** Another socket-related error occurred.

A timeout does not necessarily mean that a port is closed.

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Scan completed successfully. |
| `1` | Runtime error. |
| `2` | Invalid input or command-line usage error. |

## Limitations

- Supports TCP scanning only.
- Supports IPv4 addresses and domain names resolved to IPv4.
- Does not perform UDP scanning, service detection, or operating system fingerprinting.
- Scan results may be affected by firewalls, network filtering, and connection timeouts.

## Running Tests

Install pytest if it is not already available:

```bash
python -m pip install pytest
```

Run the test suite from the project root:

```bash
python -m pytest -v
```

## Responsible Use

This tool was created for educational purposes.

Only scan systems and networks that you own or have explicit permission to test. Unauthorized scanning may violate laws, policies, or terms of service.
