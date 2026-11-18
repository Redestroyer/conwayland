"""
This is the server script, setting up the TCP/IP listener and the database for the patterns.
"""
from concurrent.futures import ThreadPoolExecutor;
import socket;

HOST = "127.0.0.1";
PORT = 2020;

def hear(conn: socket.socket, addr: socket._RetAddress):
  with conn:
    print(f"Accepted connection from {addr}.");
  print(f"Cut connection with {addr}.");

def main():
  with socket.socket() as sock:
    sock.bind(f"{HOST}:{PORT}");
    sock.listen();
    with ThreadPoolExecutor(32) as pool:
      while connection := sock.accept():
        conn, addr = connection;
        pool.submit(hear, conn, addr);

if __name__ == "__main__":
  main()
