from tkinter import Misc
from tkinter.ttk import Button, Entry, Frame, Label

import socket


def into_addr_and_port(s: str) -> tuple[str, int]:
  *addr, port = s.split(":")
  addr = ":".join(addr)
  port = int(port)
  return addr, port

def validate_address(addr: str) -> tuple[str, int] | None:
  addr, port = into_addr_and_port(addr)
  try:
    socket.inet_pton(socket.AF_INET, addr)
    return addr, port
  except OSError:
    return None

class ConnectorTab(Frame):
  def __init__(self, master: Misc):
    super().__init__(master)

    self._addr_frame = Frame(self)
    self._addr_label = Label(self._addr_frame, text="Server: ")
    self._addr_entry = Entry(self._addr_frame)
    self._addr_submt = Button(self._addr_frame, text="Connect", command=self._connect)
    self._addr_label.pack(side="left")
    self._addr_entry.pack(side="left")
    self._addr_submt.pack(side="left")
    self._addr_frame.pack()
  
  def _connect(self):
    addr = validate_address(self._addr_entry.get())
    if not addr:
      print("Invalid address!")
      return
    addr, port = addr
    with socket.socket() as sock:
      sock.connect((addr, port))
      sock.sendall(b"Hello, World!")
      print(f"Recieved: {sock.recv(1024)!r}")
    