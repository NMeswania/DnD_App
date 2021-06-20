###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from dnd_app.utilities.text_utils import AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class FailureRenderer(Popup):

  def __init__(self):
    super().__init__()
    self.title = "Failure"
    self.content = self._AddContent()
    self._is_open = False
    self.size_hint = (0.6, 0.6)

###################################################################################################

  def Clear(self):
    for widget in self.walk(restrict=True):
      if hasattr(widget, "id"):
        widget.text = ""

###################################################################################################

  def Update(self, data: dict):
    if not self._is_open:
      self.open()
      self._is_open = True
    else:
      self.Clear()
    self._UpdateInternal(data)

###################################################################################################

  def _UpdateInternal(self, data: dict):
    for k, v in data.items():
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
    layout.add_widget(self._AddFailureType(0.2))
    layout.add_widget(self._AddMessage(0.7))
    layout.add_widget(self._AddButtonBar(0.1))
    return layout

###################################################################################################

  def _AddFailureType(self, h: float) -> Label:
    label = Label(text="", font_size="18sp", size_hint=(1, h), color=(1, 0.5, 0.5, 1))
    label.id = "type"
    return label

###################################################################################################

  def _AddMessage(self, h: float) -> Label:
    label = Label(text="", font_size="12sp", size_hint=(1, h), color=(1, 0.5, 0.5, 1))
    label.id = "message"
    AlignWidgetLabelChildren(label, valign="top")
    return label

###################################################################################################

  def _AddButtonBar(self, h: float) -> BoxLayout:
    layout = BoxLayout(orientation="horizontal", size_hint=(1, h))
    close_button = Button(text="Close", size_hint=(0.2, 1), font_size="15sp", padding=(5, 5))
    close_button.bind(on_press=self._Close)    # pylint: disable=no-member
    layout.add_widget(close_button)
    return layout


###################################################################################################
###################################################################################################
###################################################################################################
