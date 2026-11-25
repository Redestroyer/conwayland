"""
This is the server script, setting up the TCP/IP listener and the database for the patterns.
"""
from concurrent.futures import ThreadPoolExecutor;
from typing import Any

import socket;
import sys


HOST = "127.0.0.1";
PORT = 2020;

def hear(conn: socket.socket, addr: Any):
  with conn:
    print(f"Accepted connection from {addr}.");
    msg = conn.recv(1024);
    print(f"Recieved data {msg!r}");
    conn.sendall(msg);
  print(f"Cut connection with {addr}.");

def main():
  try:
    with socket.socket(socket.AF_INET) as sock:
      sock.bind((HOST, PORT));
      sock.listen();
      print(f"Listening at {HOST}:{PORT}")
      with ThreadPoolExecutor(32) as pool:
        while connection := sock.accept():
          conn, addr = connection;
          pool.submit(hear, conn, addr);
  except KeyboardInterrupt:
    print("KEYBOARD INTERRUPT")
    sys.exit()

if __name__ == "__main__":
  main()
