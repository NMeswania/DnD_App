###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from pathlib import PurePath, Path

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout

from dnd_app.viewer_widgets.widget_manager import WidgetManager
from dnd_app.core.config import Config as DNDConfig

###################################################################################################
###################################################################################################
###################################################################################################


class Viewer(App):

  def __init__(self, config: DNDConfig, widget_manager: WidgetManager):
    super().__init__()
    self._dnd_config = config
    self._widget_manager = widget_manager
    Window.maximize()
    Clock.schedule_interval(self._widget_manager.CheckForUpdates, 0.25)
    self._renderers = {}
    self._LoadKvFiles()

###################################################################################################

  def build(self):
    layout = BoxLayout(orientation="vertical", size_hint=(1, 1))
    for renderer in self._widget_manager.GetRenderers():
      layout.add_widget(renderer)
    return layout

###################################################################################################

  def _LoadKvFiles(self):
    widgets_dir = PurePath(__file__).parent.parent / "viewer_widgets"
    kv_files = sorted(Path(widgets_dir).glob("**/*.kv"))
    for widget_to_load in self._dnd_config.get("load_widgets"):
      for kv_file in kv_files:
        if widget_to_load in kv_file.as_posix():
          Builder.load_file(kv_file.as_posix())


###################################################################################################
###################################################################################################
###################################################################################################
