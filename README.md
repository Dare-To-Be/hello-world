# TCP and UDP Echo Examples (Python)

This workspace contains minimal TCP and UDP echo servers and clients implemented in Python's standard library `socket`.

## Files

- `tcp_server.py`: TCP echo server
- `tcp_client.py`: TCP client
- `udp_server.py`: UDP echo server
- `udp_client.py`: UDP client

## Quickstart

Open two terminals or run servers in the background.

### TCP

Start the server (single connection):

```bash
python3 /workspace/tcp_server.py --host 127.0.0.1 --port 5000 --once
```

In another terminal, run the client:

```bash
python3 /workspace/tcp_client.py --host 127.0.0.1 --port 5000 --message "hello tcp"
```

Expected output:

```
ACK: hello tcp
```

### UDP

Start the server (single datagram):

```bash
python3 /workspace/udp_server.py --host 127.0.0.1 --port 5001 --once
```

In another terminal, run the client:

```bash
python3 /workspace/udp_client.py --host 127.0.0.1 --port 5001 --message "hello udp"
```

Expected output:

```
ACK: hello udp
```

## Notes

- All scripts are self-contained and require only Python 3.
- Use `--once` to make servers exit after handling one request. Omit it to keep them running.