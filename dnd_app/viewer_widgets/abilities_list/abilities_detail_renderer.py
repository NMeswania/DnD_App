###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.uix.popup import Popup

###################################################################################################
###################################################################################################
###################################################################################################


class AbilitiesDetailRenderer(Popup):

  ids = {}
  ids['name'] = ObjectProperty()
  ids['source'] = ObjectProperty()
  ids['ability_description'] = ObjectProperty()

  def __init__(self, widget):
    super().__init__()
    self._widget = widget
    self._is_open = False

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    for item in self.ids.values():
      item.text = ""

###################################################################################################

  def Update(self, ability_data: dict):
    if not self._is_open:
      self.open()
      self._is_open = True
    else:
      self.Clear()
    self._UpdateInternal(ability_data)

###################################################################################################

  def _UpdateInternal(self, ability_data: dict):
    for k, v in ability_data.items():
      value = v
      if isinstance(v, dict):
        value = self._FormatSourceText(v)
      
      self.ids[k].text = value

###################################################################################################

  def _Close(self):
    self._is_open = False
    self.dismiss()

###################################################################################################

  def _FormatSourceText(self, data: dict) -> str:
    text = f"{data['category']}: {data['name']}"
    if "subtype" in data.keys():
      text += f" ({data['subtype']})"
    return text


###################################################################################################
###################################################################################################
###################################################################################################
