###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from dnd_app.utilities.text_utils import StrFieldToReadable, AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class WeaponAttributeRenderer(Popup):

  def __init__(self, widget):
    super().__init__()
    self._widget = widget
    self.title = "Weapon Attribute"
    self.content = self._AddContent()
    self._is_open = False
    self.size_hint = (0.4, 0.4)

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    for widget in self.walk(restrict=True):
      if hasattr(widget, "id") and isinstance(widget, Label):
        widget.text = ""

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
    layout.add_widget(self._AddWeaponName(0.2))
    layout.add_widget(self._AddDescription(0.7))
    layout.add_widget(self._AddButtonBar(0.1))
    return layout

###################################################################################################

  def _AddWeaponName(self, h: float) -> Button:
    label = Label(text="", font_size="18sp", size_hint=(1, h))
    label.id = "name"
    return label

###################################################################################################

  def _AddDescription(self, h: float) -> Label:
    label = Label(text="", font_size="12sp", size_hint=(1, h))
    label.id = "attribute_description"
    AlignWidgetLabelChildren(label, valign="top")
    return label

###################################################################################################

  def _AddButtonBar(self, h: float) -> Button:
    close_button = Button(text="Close", size_hint=(1, h), font_size="15sp", padding=(5, 5))
    close_button.bind(on_press=self._Close)    # pylint: disable=no-member
    return close_button


###################################################################################################
###################################################################################################
###################################################################################################
