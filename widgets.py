from tkinter import Widget


def pack_all(*widgets: Widget):
  for widget in widgets:
    widget.pack()