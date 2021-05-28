###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import queue

from multiprocessing import Queue

from dnd_app.core.config import Config
from dnd_app.request_handler.request import Request
from dnd_app.request_handler.request_handler_manager import GetRequestHandlerManagerSingleton
from dnd_app.viewer_widgets.spell_list.spell_list import SpellList

###################################################################################################
###################################################################################################
###################################################################################################


class WidgetManager:

  def __init__(self, config: Config, request_queue: Queue, character: str = ""):
    self._dnd_config = config
    self._request_queue = request_queue
    self._character = character

###################################################################################################

  def run(self):
    self._character_data = self._GetCharacterData(self._character)
    self._widgets = self._LoadWidgets()

###################################################################################################

  def GetRenderers(self) -> list:
    renderers = [widget.renderer() for widget in self._widgets.values()]
    return renderers

###################################################################################################

  def _GetCharacterData(self, character: str="") -> dict:
    request = Request(type="characters", value=f"{character}/{character}")

    request_manager_singleton = GetRequestHandlerManagerSingleton()
    receipt = request_manager_singleton.Request(request)

    while True:
      if receipt.IsResponseReady():
        response = receipt.GetRepsonse()
        return response.data()

###################################################################################################

  def _LoadWidgets(self) -> dict:
    widgets = {}
    widgets['spell_list'] = SpellList(self._dnd_config,
                                      self._character_data['character']['spell_list'])
    return widgets


###################################################################################################
###################################################################################################
###################################################################################################
