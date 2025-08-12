#!/usr/bin/env python3

import argparse
import socket
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple UDP client")
    parser.add_argument("--host", default="127.0.0.1", help="Server host/IP (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5001, help="Server port (default: 5001)")
    parser.add_argument("--message", default="hello over udp", help="Message to send")
    parser.add_argument("--timeout", type=float, default=5.0, help="Socket timeout in seconds (default: 5.0)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(args.timeout)
        try:
            sock.sendto(args.message.encode("utf-8"), (args.host, args.port))
            data, _ = sock.recvfrom(4096)
        except (OSError, socket.timeout) as exc:
            print(f"[UDP] Client error: {exc}", file=sys.stderr)
            sys.exit(1)
    print(data.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()