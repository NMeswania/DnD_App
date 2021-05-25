###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import queue

from multiprocessing import Queue

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from dnd_app.core.request import Request
from dnd_app.viewer_widgets.spell_renderer import SpellRenderer
from dnd_app.core.config import Config as DNDConfig

###################################################################################################
###################################################################################################
###################################################################################################


class Viewer(App):

  def __init__(self, config: DNDConfig, _request_queue: Queue, _response_queue: Queue) -> None:
    super().__init__()
    self._dnd_config = config
    self._request_queue = _request_queue
    self._response_queue = _response_queue
    self._responses = []
    Clock.schedule_interval(self._CheckResponseQueue, 0.5)
    self._renderers = {}

###################################################################################################

  def build(self):
    layout = BoxLayout(orientation="vertical")
    self._renderers['spell'] = SpellRenderer()
    layout.add_widget(self._renderers['spell'])
    layout.add_widget(self._AddButtons())
    return layout

###################################################################################################

  def _AddButton(self):
    return Button(text="Request some data", on_press=self._RequestData)

###################################################################################################

  def _AddButtons(self):
    layout = BoxLayout(orientation="horizontal")
    layout.add_widget(Button(text="Request earthbind", on_press=self._RequestEarthbind))
    layout.add_widget(Button(text="Request mass sugestion", on_press=self._RequestMassSuggestion))
    return layout

###################################################################################################

  def _RequestEarthbind(self, instance):
    self._RequestData("earthbind")

  def _RequestMassSuggestion(self, instance):
    self._RequestData("mass_suggestion")

###################################################################################################

  def _RequestData(self, data: str=""):
    request = Request(type="spell", value=data)
    logging.info(f"Adding request to queue: {request.id()}")

    try:
      self._request_queue.put(request,
                             block=False,
                             timeout=self._dnd_config.get_common("queue_put_timeout"))

    except queue.Full:
      logging.critical(f"Failed to put request in queue. Request id: {request.id()}")

    self._responses.clear()
    self._ClearRenderers()

###################################################################################################

  def _CheckResponseQueue(self, dt):
    while not self._response_queue.empty():
      try:
        response = self._response_queue.get(block=False,
                                          timeout=self._dnd_config.get_common("queue_get_timeout"))
        self._responses.append(response)

      except queue.Empty:
        logging.critical(f"Failed to get response from queue.")

      else:
        self._UpdateRenderers()

###################################################################################################

  def _UpdateRenderers(self):
    for response in self._responses:
      response_type = response.request.type()
      if response_type not in self._renderers.keys():
        logging.critical(f"No renderer of type: {response_type}")
        continue
      self._renderers[response_type].Update(response.response_data)


###################################################################################################

  def _ClearRenderers(self):
    for v in self._renderers.values():
      v.Clear()


###################################################################################################
###################################################################################################
###################################################################################################
