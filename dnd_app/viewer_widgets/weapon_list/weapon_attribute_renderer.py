###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.uix.popup import Popup

###################################################################################################
###################################################################################################
###################################################################################################


class WeaponAttributeRenderer(Popup):

  ids = {}
  ids['name'] = ObjectProperty("")
  ids['attribute_description'] = ObjectProperty("")

  def __init__(self, widget):
    super().__init__()
    self._widget = widget
    self._is_open = False

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    for v in self.ids.values():
      v.text = ""

###################################################################################################

  def Update(self, weapon_data: dict):
    if not self._is_open:
      self.open()
      self._is_open = True
    else:
      self.Clear()
    self._UpdateInternal(weapon_data)

###################################################################################################

  def _UpdateInternal(self, weapon_data: dict):
    for k, v in weapon_data.items():
      for k_, v_ in self.ids.items():
        if k_ == k:
          v_.text = v
          break

###################################################################################################

  def _Close(self):
    self._is_open = False
    self.dismiss()


###################################################################################################
###################################################################################################
###################################################################################################
