###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from multiprocessing import Queue

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from dnd_app.viewer_widgets.widget_manager import WidgetManager
from dnd_app.core.config import Config as DNDConfig

###################################################################################################
###################################################################################################
###################################################################################################


class Viewer(App):

  def __init__(self, config: DNDConfig, widget_manager: WidgetManager, request_queue: Queue):
    super().__init__()
    self._dnd_config = config
    self._widget_manager = widget_manager
    self._request_queue = request_queue
    self._responses = []
    Clock.schedule_interval(self._widget_manager.CheckForUpdates, 0.25)
    self._renderers = {}

###################################################################################################

  def build(self):
    layout = BoxLayout(orientation="vertical", size_hint=(1, 1))
    for renderer in self._widget_manager.GetRenderers():
      layout.add_widget(renderer)
    return layout


###################################################################################################
###################################################################################################
###################################################################################################
