###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.factory import Factory
from kivy.uix.popup import Popup

###################################################################################################
###################################################################################################
###################################################################################################


class SpellDetailRenderer(Popup):

  ids = {}
  ids['name'] = ObjectProperty("")
  ids['level'] = ObjectProperty("")
  ids['school'] = ObjectProperty("")
  ids['range'] = ObjectProperty("")
  ids['casting_time'] = ObjectProperty("")
  ids['components'] = ObjectProperty("")
  ids['duration'] = ObjectProperty("")
  ids['descriptions_layout'] = ObjectProperty("")
  ids['spell_description'] = ObjectProperty("")
  _higher_level_description = None

  def __init__(self, widget):
    super().__init__()
    self._widget = widget
    self._is_open = False

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    if self._higher_level_description is not None:
      self.ids['descriptions_layout'].remove_widget(self._higher_level_description)
    self._higher_level_description = None
    for v in self.ids.values():
      v.text = ""

###################################################################################################

  def Update(self, spell_data: dict):
    if not self._is_open:
      self.open()
      self._is_open = True
    else:
      self.Clear()
    self._UpdateInternal(spell_data)

###################################################################################################

  def _UpdateInternal(self, spell_data: dict):
    for k, v in spell_data.items():
      if isinstance(v, dict):
        self._UpdateInternal(v)
      else:
        for k_, v_ in self.ids.items():
          if k == "higher_level_description":
            self._AddHigherLevelDescription(v)
            break
          if k_ == k:
            v_.text = v
            break

###################################################################################################

  def _Close(self):
    self._is_open = False
    self.dismiss()

###################################################################################################

  def _AddHigherLevelDescription(self, description: str):
    self._higher_level_description = Factory.SpellDetailRendererDescription()
    self._higher_level_description.text = description
    self.ids['descriptions_layout'].add_widget(self._higher_level_description)


###################################################################################################
###################################################################################################
###################################################################################################
