###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from dnd_app.core.config import Config
from dnd_app.utilities.container_utils import FlattenDict
from dnd_app.utilities.text_utils import StrFieldToReadable, AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class TraitsRenderer(BoxLayout):

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
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
    flattened_data = FlattenDict(data)
    for k, v in flattened_data.items():
      for child in self.walk(restrict=True):
        if hasattr(child, "id") and child.id == k:
          child.text = str(v)
          break

###################################################################################################

  def _AddContent(self) -> BoxLayout:
    layout = BoxLayout(orientation="vertical")
    layout.add_widget(self._AddAppearance(0.4))
    layout.add_widget(self._AddTraits(0.6))
    return layout

###################################################################################################

  def _AddAppearance(self, h: float) -> GridLayout:
    layout = GridLayout(rows=2, cols=3, size_hint=(1, h))
    for field in ["age", "height", "weight", "eyes", "skin", "hair"]:
      layout.add_widget(self._AddAppearanceField(field))
    return layout

###################################################################################################

  def _AddAppearanceField(self, field: str) -> BoxLayout:
    layout = BoxLayout(orientation="horizontal")
    layout.add_widget(
        Label(text=StrFieldToReadable(field), font_size="13sp", italic=True, size_hint=(0.4, 1)))
    label = Label(text="", font_size="13sp", size_hint=(0.6, 1))
    label.id = f"appearance_{field}"
    layout.add_widget(label)
    return layout

###################################################################################################

  def _AddTraits(self, h: float) -> GridLayout:
    layout = GridLayout(cols=1, rows=4, size_hint=(1, h))
    for field in ["personality_traits", "ideals", "bonds", "flaws"]:
      layout.add_widget(self._AddTraitField(field))
    return layout

###################################################################################################

  def _AddTraitField(self, field: str) -> BoxLayout:
    layout = BoxLayout(orientation="horizontal")
    layout.add_widget(
        Label(text=StrFieldToReadable(field), font_size="13sp", italic=True, size_hint=(0.2, 1)))
    label = Label(text="", font_size="13sp", size_hint=(0.8, 1))
    label.id = f"traits_{field}"
    layout.add_widget(label)
    AlignWidgetLabelChildren(layout)
    return layout


###################################################################################################
###################################################################################################
###################################################################################################
