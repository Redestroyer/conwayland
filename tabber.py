from tkinter import *  # pyright: ignore[reportWildcardImportFromLibrary]
from tkinter.ttk import *  # pyright: ignore[reportWildcardImportFromLibrary]

from connector_tab import ConnectorTab
from conway_widget import ConwayWidget


class Tabber(Notebook):
  def __init__(self, master: Misc):
    super().__init__(master)
    
    self.conway = ConwayWidget(self)
    self.add(self.conway, text="Board")
    self.connector = ConnectorTab(self)
    self.add(self.connector, text="Connection")
