###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from dnd_app.core.config import Config
from dnd_app.utilities.container_utils import FlattenDict
from dnd_app.utilities.text_utils import StrFieldToReadable

###################################################################################################
###################################################################################################
###################################################################################################


class CombatRenderer(BoxLayout):

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
    for child in self.walk():
      if hasattr(child, "id") and isinstance(child, Label):
        child.text = ""
      elif isinstance(child, CheckBox):
        child.active = False

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    flatten_data = FlattenDict(data)
    for k, v in flatten_data.items():
      for child in self.walk():
        if hasattr(child, "id") and child.id == k:
          if isinstance(child, Label):
            child.text = str(v)
            break

          elif isinstance(child, GridLayout):
            grandchildren = child.children
            if len(grandchildren) >= v:
              for i in range(v):
                grandchildren[i].active = True

            else:
              logging.critical(f"Number of {k} ({v}) is more than max saves {len(grandchildren)}")

            break

###################################################################################################

  def _AddTitle(self) -> Label:
    return Label(text="Combat", font_size="20sp", size_hint=(1, 0.05))

###################################################################################################

  def _AddContent(self) -> BoxLayout:
    layout = BoxLayout(orientation="vertical")
    layout.add_widget(self._AddMainProperties())
    layout.add_widget(self._AddHitPoints())
    layout.add_widget(self._AddHitDie())
    layout.add_widget(self._AddDeathSaves())
    return layout

###################################################################################################

  def _AddMainProperties(self) -> GridLayout:
    fields = ["armor_class", "initiative", "speed"]
    return self._GenerateGenericSection(fields)

###################################################################################################

  def _AddHitPoints(self) -> GridLayout:
    fields = ["max", "current", "temporary"]
    title = "hit_points"
    return self._GenerateGenericSection(fields, title)

###################################################################################################

  def _AddHitDie(self) -> GridLayout:
    fields = ["total", "current"]
    title = "hit_die"
    return self._GenerateGenericSection(fields, title)

###################################################################################################

  def _AddDeathSaves(self) -> BoxLayout:
    layout = BoxLayout(orientation="horizontal")
    title = "death_saves"
    layout.add_widget(Label(text=StrFieldToReadable(title), size_hint=(0.4, 1), font_size="15sp"))
    layout.add_widget(self._AddDeathSaveSection("successes"))
    layout.add_widget(self._AddDeathSaveSection("failures"))
    return layout

###################################################################################################

  def _GenerateGenericSection(self,
                              section_headings: list,
                              section_title: str = None) -> GridLayout:
    assert len(section_headings) > 0
    n_cols = len(section_headings) + ( 1 if section_title is not None else 0)
    layout = GridLayout(rows=1, cols=n_cols)

    id_prefix = ""
    if section_title is not None:
      id_prefix = f"{section_title}_"
      layout.add_widget(Label(text=StrFieldToReadable(section_title), font_size="15sp"))

    for field in section_headings:
      field_layout = BoxLayout(orientation="vertical")
      field_layout.add_widget(
          Label(text=StrFieldToReadable(field), size_hint=(1, 0.3), font_size="12sp"))
      field_label = Label(text="", size_hint=(1, 0.7), font_size="15sp")
      field_label.id = f"{id_prefix}{field}"
      field_layout.add_widget(field_label)
      layout.add_widget(field_layout)

    return layout

###################################################################################################

  def _AddDeathSaveSection(self, section_title: str, id_prefix: str="death_saves_") -> BoxLayout:
    layout = BoxLayout(orientation="horizontal")
    layout.add_widget(Label(text=StrFieldToReadable(section_title), font_size="13sp"))
    grid_layout = GridLayout(rows=1, cols=3, col_force_default=True, col_default_width=40)
    grid_layout.id = id_prefix + section_title

    for _ in range(3):
      grid_layout.add_widget(CheckBox(active=False))

    layout.add_widget(grid_layout)

    return layout


###################################################################################################
###################################################################################################
###################################################################################################
