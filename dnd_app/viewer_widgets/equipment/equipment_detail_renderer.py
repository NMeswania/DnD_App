###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from functools import partial

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

  def __init__(self, widget):
    super().__init__()
    self._widget = widget
    self.title = "Equipment Details"
    self.content = self._AddContent()
    self._is_open = False
    self.size_hint = (0.6, 0.6)

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    for widget in self.walk(restrict=True):
      if hasattr(widget, "id"):
        widget.text = ""
    self._tags_layout.clear_widgets()

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
          self._tags_layout.add_widget(self._AddTag(item))
      else:
        for child in self.walk(restrict=True):
          if hasattr(child, "id") and child.id == k:
            child.text = v
            break

###################################################################################################

  def _Close(self, instance):
    self._is_open = False
    self.dismiss()

###################################################################################################

  def _AddContent(self):
    layout = BoxLayout(orientation="vertical")
    layout.add_widget(self._AddEquipmentName(0.1))
    layout.add_widget(self._AddRarity(0.1))
    layout.add_widget(self._AddDescription(0.4))
    layout.add_widget(self._AddTags(0.3))
    layout.add_widget(self._AddButtonBar(0.1))
    return layout

###################################################################################################

  def _AddEquipmentName(self, h: float) -> Label:
    label = Label(text="", font_size="18sp", size_hint=(1, h))
    label.id = "name"
    return label

###################################################################################################

  def _AddRarity(self, h: float) -> Label:
    label = Label(text="", font_size="13sp", size_hint=(1, h), italic=True)
    label.id = "rarity"
    return label

###################################################################################################

  def _AddDescription(self, h: float) -> Label:
    label = Label(text="", font_size="12sp", size_hint=(1, h))
    label.id = "equipment_description"
    AlignWidgetLabelChildren(label, valign="top")
    return label

###################################################################################################

  def _AddTags(self, h: float) -> GridLayout:
    self._tags_layout = GridLayout(rows=5,
                                   row_default_height=40,
                                   row_force_default=True,
                                   size_hint=(1, h))
    self._tags_layout.id = "tags"
    AlignWidgetLabelChildren(self._tags_layout, valign="top")
    return self._tags_layout

###################################################################################################

  def _AddButtonBar(self, h: float) -> BoxLayout:
    layout = BoxLayout(orientation="horizontal", size_hint=(1, h))
    prev_button = Button(text="<", size_hint=(0.4, 1), font_size="15sp", padding=(5, 5))
    prev_button.bind(on_press=partial(self._widget.RequestNextEquipmentCallback, -1))    # pylint: disable=no-member

    close_button = Button(text="Close", size_hint=(0.2, 1), font_size="15sp", padding=(5, 5))
    close_button.bind(on_press=self._Close)    # pylint: disable=no-member

    next_button = Button(text=">", size_hint=(0.4, 1), font_size="15sp", padding=(5, 5))
    next_button.bind(on_press=partial(self._widget.RequestNextEquipmentCallback, 1))    # pylint: disable=no-member

    layout.add_widget(prev_button)
    layout.add_widget(close_button)
    layout.add_widget(next_button)
    return layout

###################################################################################################

  def _AddTag(self, tag_name: str) -> Label:
    label = Label(text=StrFieldToReadable(tag_name), font_size="13sp")
    AlignWidgetLabelChildren(label)
    return label


###################################################################################################
###################################################################################################
###################################################################################################
