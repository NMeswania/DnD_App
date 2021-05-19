###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import kivy

from kivy.app import App
from kivy.uix.label import Label

from dnd_app.data_manager_interface.data_manager_interface import DataManagerInterface

###################################################################################################
###################################################################################################
###################################################################################################


class Viewer(App):
  def __init__(self, data_manager_interface: DataManagerInterface):
    super().__init__()
    self.data_manager_interface = data_manager_interface

  def build(self):
    data = self.data_manager_interface.request_from_data_manager()
    return Label(text=f"Got data: {str(data)}")


###################################################################################################
###################################################################################################
###################################################################################################
