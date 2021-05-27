###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import queue

from pathlib import Path

from multiprocessing import Queue

from dnd_app.core.config import Config
from dnd_app.core.request import Request
from dnd_app.viewer_widgets.widget_base import WidgetBase
from dnd_app.viewer_widgets.spell_list.spell_list_renderer import SpellListRenderer

###################################################################################################
###################################################################################################
###################################################################################################


class SpellList(WidgetBase):

  def __init__(self, config: Config, request_queue: Queue(), response_queue: Queue(),
               spell_list_path: Path):
    self._dnd_config = config
    self._request_queue = request_queue
    self._response_queue = response_queue
    self._spell_data = self._LoadData(spell_list_path)
    self._renderer = self._BuildRenderer()

###################################################################################################

  def __del__(self):
    self._renderer.Terminate()
    del self._renderer

###################################################################################################

  def renderer(self) -> SpellListRenderer:
    return self._renderer

###################################################################################################

  def RequestSpellCallback(self, instance, spell_name: str):
    request = Request(type="spell", value=spell_name)
    try:
      self._request_queue.put(request,
                              block=False,
                              timeout=self._dnd_config.get_common("queue_put_timeout"))

    except queue.Full:
      logging.critical(f"Failed to send request: {request.id()}")

###################################################################################################

  def _LoadData(self, file_path: Path) -> dict:
    request = Request(type="characters", value="subs/spell_list")
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
        logging.debug(f"Failed to get request: {request.id()}")

###################################################################################################

  def _BuildRenderer(self) -> SpellListRenderer:
    return SpellListRenderer(self._dnd_config, self, self._spell_data)


###################################################################################################
###################################################################################################
###################################################################################################
