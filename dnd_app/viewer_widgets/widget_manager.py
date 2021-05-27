###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import queue

from multiprocessing import Queue

from dnd_app.core.config import Config
from dnd_app.core.request import Request
from dnd_app.viewer_widgets.spell_list.spell_list import SpellList

###################################################################################################
###################################################################################################
###################################################################################################


class WidgetManager:

  def __init__(self,
               config: Config,
               request_queue: Queue,
               response_queue: Queue,
               character: str = ""):
    self._dnd_config = config
    self._request_queue = request_queue
    self._response_queue = response_queue
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
    request_id = request.id()
    try:
      self._request_queue.put(request,
                              block=False,
                              timeout=self._dnd_config.get_common("queue_put_timeout"))

    except queue.Full:
      logging.critical(f"Failed to send request: {request.id()}")

    while True:
      try:
        response = self._response_queue.get(
            block=False, timeout=self._dnd_config.get_common("queue_get_timeout"))

        if response.request.id() == request_id:
          return response.data()

        else:
          try:
            self._response_queue.put(response,
                                     block=False,
                                     timeout=self._dnd_config.get_common("queue_put_timeout"))

          except:
            logging.debug(f"Pulled response ({response.request.id()}) "
                          f"that doesn't match request ({request_id})")

      except queue.Empty:
        continue

###################################################################################################

  def _LoadWidgets(self) -> dict:
    widgets = {}
    widgets['spell_list'] = SpellList(self._dnd_config, self._request_queue, self._response_queue,
                                      self._character_data['character']['spell_list'])
    return widgets


###################################################################################################
###################################################################################################
###################################################################################################
