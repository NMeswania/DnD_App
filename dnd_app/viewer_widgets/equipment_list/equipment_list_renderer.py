###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from dnd_app.core.config import Config
from dnd_app.utilities.text_utils import StrFieldToReadable, AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class EquipmentListRenderer(BoxLayout):

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
    self.add_widget(self._AddTitle())
    self.add_widget(self._AddContent())
    self._equipment_list = []

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    self._equipment_layout.clear_widgets()
    for child in self.walk(restrict=True):
      if hasattr(child, "id"):
        child.text = ""
    self._equipment_list = []

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    for _, v in data.items():
      if isinstance(v, list) and len(v) > 0:
        for item in v:
          self._equipment_layout.add_widget(self._AddEquipment(item))
      elif isinstance(v, dict):
        for key, value in v.items():
          for child in self.walk(restrict=True):
            if hasattr(child, "id") and child.id == key:
              child.text = str(value)

###################################################################################################

  def GetNextEquipmentAndIndex(self, index: int) -> list:
    idx = index % len(self._equipment_list)
    return [self._equipment_list[idx], idx]

###################################################################################################

  def _AddTitle(self) -> Label:
    return Label(text="Equipment", font_size="20sp", size_hint=(1, 0.05))

###################################################################################################

  def _AddContent(self) -> BoxLayout:
    layout = BoxLayout(orientation="vertical")
    self._equipment_layout = GridLayout(cols=4, row_default_height=40, row_force_default=True)
    layout.add_widget(self._AddMoney())
    layout.add_widget(self._equipment_layout)
    return layout

###################################################################################################

  def _AddMoney(self) -> BoxLayout:
    layout = BoxLayout(orientation="vertical")
    for value in ["platinum", "gold", "electrum", "silver", "copper"]:
      internal_layout = BoxLayout(orientation="horizontal")
      internal_layout.add_widget(Label(text=StrFieldToReadable(value), size_hint=(0.3, 1)))
      money_label = Label(text="", size_hint=(0.7, 1))
      money_label.id = value
      internal_layout.add_widget(money_label)
      layout.add_widget(internal_layout)
    return layout

###################################################################################################

  def _AddEquipment(self, equipment_name: str) -> Button:
    self._equipment_list.append(equipment_name)
    btn = Button(text=StrFieldToReadable(equipment_name),
                 size_hint=(0.9, 1),
                 font_size="13sp",
                 padding=(5, 5))
    AlignWidgetLabelChildren(btn)
    btn.bind(on_press=partial(self._widget.RequestEquipmentCallback, equipment_name,
                              len(self._equipment_list)))    # pylint: disable=no-member
    return btn

###################################################################################################
###################################################################################################
###################################################################################################
