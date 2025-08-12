#!/usr/bin/env python3

import argparse
import socket
import sys
from typing import Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple UDP echo server")
    parser.add_argument("--host", default="127.0.0.1", help="Host/IP to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5001, help="Port to bind (default: 5001)")
    parser.add_argument("--once", action="store_true", help="Handle a single datagram and exit")
    return parser.parse_args()


def run_server(host: str, port: int, once: bool) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        print(f"[UDP] Listening on {host}:{port}")
        while True:
            try:
                data, addr = server_socket.recvfrom(4096)
            except KeyboardInterrupt:
                print("\n[UDP] Shutting down server...")
                break
            if not data:
                continue
            print(f"[UDP] Datagram from {addr[0]}:{addr[1]}")
            response = b"ACK: " + data
            try:
                server_socket.sendto(response, addr)
            except OSError as exc:
                print(f"[UDP] Send error: {exc}", file=sys.stderr)
            if once:
                print("[UDP] --once specified, exiting after one datagram")
                break


def main() -> None:
    args = parse_args()
    try:
        run_server(args.host, args.port, args.once)
    except OSError as exc:
        print(f"[UDP] Server error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()