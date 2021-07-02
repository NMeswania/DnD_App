###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.uix.boxlayout import BoxLayout

from dnd_app.core.config import Config

###################################################################################################
###################################################################################################
###################################################################################################


class MainInfoRenderer(BoxLayout):

  ids = {}
  ids['name'] = ObjectProperty("")
  ids['classes_levels'] = ObjectProperty("")
  ids['race'] = ObjectProperty("")
  ids['background'] = ObjectProperty("")
  ids['alignment'] = ObjectProperty("")
  ids['experience_points'] = ObjectProperty("")

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget

###################################################################################################

  def build(self):
    return self

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    for v_ in self.ids.values():
      if hasattr(v_, "text"):
        v_.text = ""

###################################################################################################

  def Update(self, data: dict):
    self.Clear()

    for k, v in data.items():
      value = v
      if isinstance(v, list) and len(v) > 0:
        value = self._UpdateClassesLevels(v)

      elif isinstance(v, int):
        value = str(v)

      for k_, v_ in self.ids.items():
        if k == k_ and hasattr(v_, "text"):
          v_.text = value
          break

###################################################################################################

  def _UpdateClassesLevels(self, data: dict) -> str:
    label_text = ""
    for item in data:
      if label_text != "":
        label_text += ", "

      class_level = f"Level {item[2]} {item[0]} ({item[1]})"
      label_text += class_level

    return label_text


###################################################################################################
###################################################################################################
###################################################################################################
