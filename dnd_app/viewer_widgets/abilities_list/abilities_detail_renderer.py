###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from dnd_app.utilities.text_utils import StrFieldToReadable, AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class AbilitiesDetailRenderer(Popup):

  def __init__(self, widget):
    super().__init__()
    self._widget = widget
    self.title = "Ability Details"
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
        value = self._SetSourceText(v)
      for child in self.walk(restrict=True):
        if hasattr(child, "id") and child.id == k:
          child.text = value
          break

###################################################################################################

  def _Close(self, instance):
    self._is_open = False
    self.dismiss()

###################################################################################################

  def _AddContent(self):
    layout = BoxLayout(orientation="vertical")
    layout.add_widget(self._AddAbilityName(0.1))
    layout.add_widget(self._AddSource(0.2))
    layout.add_widget(self._AddDescription(0.6))
    layout.add_widget(self._AddButtonBar(0.1))
    return layout

###################################################################################################

  def _AddAbilityName(self, h: float) -> Label:
    label = Label(text="", font_size="18sp", size_hint=(1, h))
    label.id = "name"
    return label

###################################################################################################

  def _AddSource(self, h: float) -> Label:
    label = Label(text="", font_size="13sp", italic=True, size_hint=(1, h))
    label.id = "source"
    return label

###################################################################################################

  def _AddDescription(self, h: float) -> Label:
    label = Label(text="", font_size="12sp", size_hint=(1, h))
    label.id = "ability_description"
    AlignWidgetLabelChildren(label, valign="top")
    return label

###################################################################################################

  def _AddButtonBar(self, h: float) -> BoxLayout:
    layout = BoxLayout(orientation="horizontal", size_hint=(1, h))
    prev_button = Button(text="<", size_hint=(0.4, 1), font_size="15sp", padding=(5, 5))
    prev_button.bind(on_press=partial(self._widget.RequestNextAbilityCallback, -1))    # pylint: disable=no-member

    close_button = Button(text="Close", size_hint=(0.2, 1), font_size="15sp", padding=(5, 5))
    close_button.bind(on_press=self._Close)    # pylint: disable=no-member

    next_button = Button(text=">", size_hint=(0.4, 1), font_size="15sp", padding=(5, 5))
    next_button.bind(on_press=partial(self._widget.RequestNextAbilityCallback, 1))    # pylint: disable=no-member

    layout.add_widget(prev_button)
    layout.add_widget(close_button)
    layout.add_widget(next_button)
    return layout

###################################################################################################

  def _SetSourceText(self, data: dict) -> str:
    text = f"{data['category']}: {data['name']}"
    if "subtype" in data.keys():
      text += f" ({data['subtype']})"
    return text


###################################################################################################
###################################################################################################
###################################################################################################
