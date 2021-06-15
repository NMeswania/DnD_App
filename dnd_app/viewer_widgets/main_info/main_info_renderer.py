###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from dnd_app.core.config import Config
from dnd_app.utilities.text_utils import StrFieldToReadable, AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class MainInfoRenderer(BoxLayout):

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
    self.add_widget(self._AddTitle())
    self.add_widget(self._AddContent())

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    for child in self.walk(restrict=True):
      if hasattr(child, "id"):
        child.text = ""

###################################################################################################

  def Update(self, data: dict):
    self.Clear()

    for k, v in data.items():
      value = v
      if isinstance(v, list) and len(v) > 0:
        value = self._UpdateClassesLevels(v)

      elif isinstance(v, int):
        value = str(v)

      for child in self.walk(restrict=True):
        if hasattr(child, "id") and child.id == k:
          child.text = value
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

  def _AddTitle(self) -> Label:
    label = Label(text="", font_size="25sp", size_hint=(1, 0.1))
    label.id = "name"
    return label

###################################################################################################

  def _AddContent(self) -> BoxLayout:
    layout = BoxLayout(orientation="vertical")
    layout.add_widget(self._AddClassesLevels(0.4))
    layout.add_widget(self._AddInfoBlock(0.6))
    return layout

###################################################################################################

  def _AddClassesLevels(self, h: float) -> Label:
    label = Label(text="", font_size="18sp", italic=True, size_hint=(1, h))
    label.id = "classes_levels"
    return label

###################################################################################################

  def _AddInfoBlock(self, h: float) -> GridLayout:
    layout = GridLayout(rows=1,
                        cols=4,
                        row_default_height=40,
                        row_force_default=True,
                        size_hint=(1, h))
    for field in ["race", "background", "alignment", "experience_points"]:
      label = Label(text="", font_size="16sp")
      label.id = field
      layout.add_widget(label)

    return layout


###################################################################################################
###################################################################################################
###################################################################################################
