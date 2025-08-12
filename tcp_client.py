#!/usr/bin/env python3

import argparse
import socket
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple TCP client")
    parser.add_argument("--host", default="127.0.0.1", help="Server host/IP (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Server port (default: 5000)")
    parser.add_argument("--message", default="hello over tcp", help="Message to send")
    parser.add_argument("--timeout", type=float, default=5.0, help="Socket timeout in seconds (default: 5.0)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(args.timeout)
        try:
            sock.connect((args.host, args.port))
            sock.sendall(args.message.encode("utf-8"))
            data = sock.recv(4096)
        except (OSError, socket.timeout) as exc:
            print(f"[TCP] Client error: {exc}", file=sys.stderr)
            sys.exit(1)
    print(data.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()