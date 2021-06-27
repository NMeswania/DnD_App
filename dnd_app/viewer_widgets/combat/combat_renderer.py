###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label

from dnd_app.core.config import Config
from dnd_app.utilities.text_utils import StrFieldToReadable

###################################################################################################
###################################################################################################
###################################################################################################


class CombatRenderer(BoxLayout):

  ids = {}
  ids['main_properties'] = ObjectProperty("")
  ids['hit_points'] = ObjectProperty("")
  ids['hit_die'] = ObjectProperty("")
  ids['death_saves'] = ObjectProperty("")

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
    self._AddContent()

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    for value in self.ids.values():
      self._ClearInternal(value)

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    for k, v in data.items():
      if k == "death_saves":
        self._UpdateDeathSaves(v)
        continue

      for id, value in self.ids.items():
        if k == id:
          self._UpdateInternal(value, v)
          break

###################################################################################################

  def _AddContent(self):
    self._AddMainProperties()
    self._AddHitPoints()
    self._AddHitDie()
    self._AddDeathSaves()

###################################################################################################

  def _ClearInternal(self, value):
    if isinstance(value, Label):
      value.text = ""
    elif isinstance(value, CheckBox):
      value.active = False
    elif hasattr(value, "children") and len(value.children) > 0:
      for child in value.children:
        for nested_value in child.ids:
          self._ClearInternal(nested_value)

###################################################################################################

  def _UpdateDeathSaves(self, death_saves: dict):
    for death_save, number in death_saves.items():
      for child in self.ids['death_saves'].children:
        if len(child.ids) > 0 and child.ids['name'] == death_save:
          n = 0
          for check_box in child.ids['checkboxes'].children:
            n += 1
            check_box.active = True
            if n >= number:
              break
          break

###################################################################################################

  def _UpdateInternal(self, widget, data: dict):
    for k, v in data.items():
      for child in widget.children:
        if len(child.ids) > 0 and child.ids['name'] == k:
          child.ids['value'].text = str(v)
          break

###################################################################################################

  def _AddMainProperties(self):
    self._GenerateGenericSection(section_headings=["armor_class", "initiative", "speed"],
                                 section_title='main_properties')

###################################################################################################

  def _AddHitPoints(self):
    self._GenerateGenericSection(section_headings=["max", "current", "temporary"],
                                 section_title='hit_points',
                                 display_section_title=True)

###################################################################################################

  def _AddHitDie(self):
    self._GenerateGenericSection(section_headings=["total", "current"],
                                 section_title='hit_die',
                                 display_section_title=True)


###################################################################################################

  def _AddDeathSaves(self):
    for field in ["successes", "failures"]:
      death_save = Factory.DeathSave()
      death_save.ids['name'] = field
      death_save.ids['label'].text = StrFieldToReadable(field)
      self.ids['death_saves'].add_widget(death_save)

###################################################################################################

  def _GenerateGenericSection(self,
                              section_headings: list,
                              section_title: str,
                              display_section_title: bool=False):
    assert len(section_headings) > 0
    assert section_title in self.ids.keys()

    if display_section_title:
      section_title_label = Factory.SectionTitle()
      section_title_label.text = StrFieldToReadable(section_title)
      self.ids[section_title].add_widget(section_title_label)

    for field in section_headings:
      info_label = Factory.InfoLabel()
      info_label.ids['name'] = field
      info_label.ids['label'].text = StrFieldToReadable(field)
      self.ids[section_title].add_widget(info_label)


###################################################################################################
###################################################################################################
###################################################################################################
