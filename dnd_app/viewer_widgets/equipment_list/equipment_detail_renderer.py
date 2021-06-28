###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from functools import partial

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from dnd_app.utilities.text_utils import StrFieldToReadable, AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class EquipmentDetailRenderer(Popup):

  ids = {}
  ids['name'] = ObjectProperty("")
  ids['rarity'] = ObjectProperty("")
  ids['equipment_description'] = ObjectProperty("")
  ids['tags'] = ObjectProperty("")

  def __init__(self, widget):
    super().__init__()
    self._widget = widget
    self._is_open = False
    self.size_hint = (0.6, 0.6)

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    for item in self.ids.values():
      if hasattr(item, "text"):
        item.text = ""
    self.ids['tags'].clear_widgets()

###################################################################################################

  def Update(self, equipment_data: dict):
    if not self._is_open:
      self.open()
      self._is_open = True
    else:
      self.Clear()
    self._UpdateInternal(equipment_data)

###################################################################################################

  def _UpdateInternal(self, equipment_data: dict):
    for k, v in equipment_data.items():
      if isinstance(v, list):
        for item in v:
          self._AddTag(item)
      else:
        if k in self.ids.keys():
          self.ids[k].text = v

###################################################################################################

  def _Close(self):
    self._is_open = False
    self.dismiss()

###################################################################################################

  def _AddTag(self, tag_name: str):
    label = Factory.EquipmentDetailRendererTag()
    label.text = StrFieldToReadable(tag_name)
    self.ids['tags'].add_widget(label)


###################################################################################################
###################################################################################################
###################################################################################################
