###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from pathlib import Path

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang.builder import Builder

from dnd_app.viewer_widgets.widget_manager import WidgetManager
from dnd_app.core.config import Config as DNDConfig
from dnd_app.viewer.viewer import Viewer

###################################################################################################
###################################################################################################
###################################################################################################


class ViewerApp(App):

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
    viewer = Viewer()
    for renderer in self._widget_manager.GetRenderers():
      viewer.add_renderer(renderer)
    return viewer

###################################################################################################

  def _LoadKvFiles(self):
    widgets_dir = self._dnd_config.get_data_dir().parent / "viewer_widgets"
    kv_files = sorted(Path(widgets_dir).glob("**/*.kv"))
    for widget_to_load in self._widget_manager.GetViewerWidgetsToLoad():
      for kv_file in kv_files:
        if widget_to_load in kv_file.as_posix():
          Builder.load_file(kv_file.as_posix())


###################################################################################################
###################################################################################################
###################################################################################################
