###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import queue

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from multiprocessing import Queue

from dnd_app.core.request import Request
from dnd_app.core.config import Config as DNDConfig

###################################################################################################
###################################################################################################
###################################################################################################


class Viewer(App):

  def __init__(self, config: DNDConfig, request_queue: Queue, response_queue: Queue) -> None:
    super().__init__()
    self.dnd_config = config
    self.request_queue = request_queue
    self.response_queue = response_queue
    self.responses = []
    Clock.schedule_interval(self._CheckResponseQueue, 0.5)

###################################################################################################

  def build(self):
    layout = BoxLayout(orientation="vertical")
    layout.add_widget(self._AddButton())
    layout.add_widget(self._AddText())
    return layout

###################################################################################################

  def _AddButton(self):
    return Button(text="Request some data", on_press=self._RequestData)

###################################################################################################

  def _AddText(self):
    self.label = Label(text=f"Recived data: ")
    return self.label

###################################################################################################

  def _RequestData(self, instance):
    request = Request(type="spell", value="Mass Suggestion")
    logging.info(f"Adding request to queue: {request}")

    try:
      self.request_queue.put(request, block=False, timeout=self.dnd_config.get_common("queue_put_timeout"))

    except queue.Full:
      logging.critical(f"Failed to put request in queue. Request id: {request.id()}")

    self.responses.clear()

###################################################################################################

  def _CheckResponseQueue(self, dt):
    while True:
      try:
        response = self.response_queue.get(block=False,
                                          timeout=self.dnd_config.get_common("queue_get_timeout"))
        self.responses.append(response)

      except queue.Empty:
        logging.critical(f"Failed to get response from queue.")

      if self.response_queue.empty():
        break

      response_text = [f"{str(response)}\n" for response in self.responses]
      response_text_full = f"Recived data: {response_text}"
      self._UpdateLabelText(response_text_full)

###################################################################################################

  def _UpdateLabelText(self, text: str):
    self.label.text = text


###################################################################################################
###################################################################################################
###################################################################################################
