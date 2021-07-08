###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from functools import partial

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout

from dnd_app.core.config import Config
from dnd_app.utilities.text_utils import StrFieldToReadable, GetRendererLabelFromFilename

###################################################################################################
###################################################################################################
###################################################################################################


class EquipmentListRenderer(BoxLayout):

  ids = {}
  ids['money'] = ObjectProperty("")
  ids['equipment'] = ObjectProperty("")

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
    self._equipment_list = []
    self._AddMoney()

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    self.ids['equipment'].clear_widgets()
    for child in self.ids['money'].children:
      child.ids['value'].text = ""
    self._equipment_list = []

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    for _, v in data.items():
      if isinstance(v, list) and len(v) > 0:
        for item in v:
          self._AddEquipment(item)
      elif isinstance(v, dict):
        for key, value in v.items():
          for child in self.ids['money'].children:
            if key == child.ids['name']:
              child.ids['value'].text = str(value)
              break

###################################################################################################

  def GetNextEquipmentAndIndex(self, index: int) -> list:
    idx = index % len(self._equipment_list)
    return [self._equipment_list[idx], idx]

###################################################################################################

  def GetLabel(self):
    return GetRendererLabelFromFilename(__file__)

###################################################################################################

  def _AddMoney(self):
    for value in ["platinum", "gold", "electrum", "silver", "copper"]:
      layout = Factory.EquipmentListRendererMoneyLabel()
      layout.ids['name'] = value
      layout.ids['demarkation'].text = StrFieldToReadable(value)
      self.ids['money'].add_widget(layout)

###################################################################################################

  def _AddEquipment(self, equipment_name: str):
    self._equipment_list.append(equipment_name)
    btn = Factory.EquipmentListRendererEquipmentButton()
    btn.text = StrFieldToReadable(equipment_name)
    btn.bind(on_press=partial(self._widget.RequestEquipmentCallback, equipment_name,
                              len(self._equipment_list) - 1))   # pylint: disable=no-member
    self.ids['equipment'].add_widget(btn)

###################################################################################################
###################################################################################################
###################################################################################################
