#!/usr/bin/env python3

import argparse
import socket
import sys
from typing import Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple TCP echo server")
    parser.add_argument("--host", default="127.0.0.1", help="Host/IP to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind (default: 5000)")
    parser.add_argument("--once", action="store_true", help="Handle a single connection and exit")
    return parser.parse_args()


def receive_all(connection: socket.socket, buffer_size: int = 4096) -> bytes:
    connection.settimeout(5.0)
    try:
        data = connection.recv(buffer_size)
        return data
    except socket.timeout:
        return b""


def handle_client_connection(client_socket: socket.socket, client_addr: Tuple[str, int]) -> None:
    try:
        data = receive_all(client_socket)
        if not data:
            return
        response = b"ACK: " + data
        client_socket.sendall(response)
    finally:
        try:
            client_socket.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        client_socket.close()


def run_server(host: str, port: int, once: bool) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"[TCP] Listening on {host}:{port}")
        while True:
            try:
                client_socket, client_addr = server_socket.accept()
            except KeyboardInterrupt:
                print("\n[TCP] Shutting down server...")
                break
            print(f"[TCP] Connection from {client_addr[0]}:{client_addr[1]}")
            handle_client_connection(client_socket, client_addr)
            if once:
                print("[TCP] --once specified, exiting after one connection")
                break


def main() -> None:
    args = parse_args()
    try:
        run_server(args.host, args.port, args.once)
    except OSError as exc:
        print(f"[TCP] Server error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()