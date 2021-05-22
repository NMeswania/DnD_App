###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import kivy

from kivy.app import App
from kivy.uix.label import Label

from dnd_app.request_handler_manager.request_handler_manager import RequestHandlerManager

###################################################################################################
###################################################################################################
###################################################################################################


class Viewer(App):
  def __init__(self, request_handler_manager: RequestHandlerManager):
    super().__init__()
    self.request_handler_manager = request_handler_manager

  def build(self):
    data = self.request_handler_manager.request_from_request_handler()
    return Label(text=f"Got data: {str(data)}")


###################################################################################################
###################################################################################################
###################################################################################################
