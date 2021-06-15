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


class DetailRenderer(Popup):

  def __init__(self, widget):
    super().__init__()
    self._widget = widget
    self.title = "Spell Details"
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
    layout.add_widget(self._AddSpellName(0.1))
    layout.add_widget(self._AddSpellLevel(0.1))
    layout.add_widget(self._AddBasicData(0.3))
    layout.add_widget(self._AddDescriptions(0.3))
    layout.add_widget(self._AddButtonBar(0.1))
    return layout

###################################################################################################

  def _AddSpellName(self, h: float):
    label = Label(text="", font_size="18sp", size_hint=(1, h))
    label.id = "name"
    return label

###################################################################################################

  def _AddSpellLevel(self, h: float):
    layout = BoxLayout(orientation="horizontal", size_hint=(1, h))

    for field in ["level", "school"]:
      label = Label(text="", italic=True, font_size="13sp", size_hint=(1, 0.2))
      label.id = field
      layout.add_widget(label)
    return layout

###################################################################################################

  def _AddBasicData(self, h: float):
    layout = GridLayout(rows=4, cols=2, size_hint=(1, h))

    for field in ["range", "casting_time", "components", "duration"]:
      layout.add_widget(
          Label(text=StrFieldToReadable(field), bold=True, font_size="13sp",
                size_hint=(0.3, 0.22)))
      label = Label(text="", font_size="13sp", size_hint=(0.7, 0.22))
      label.id = field
      layout.add_widget(label)

    AlignWidgetLabelChildren(layout)

    return layout

###################################################################################################

  def _AddDescriptions(self, h: float):
    layout = BoxLayout(orientation="vertical", size_hint=(1, h))
    for section in ["spell_description", "higher_level_description"]:
      label = Label(text="", font_size="12sp")
      label.id = section
      layout.add_widget(label)
    AlignWidgetLabelChildren(layout, valign="top")
    return layout

###################################################################################################

  def _AddButtonBar(self, h: float):
    layout = BoxLayout(orientation="horizontal", size_hint=(1, h))
    prev_button = Button(text="<", size_hint=(0.4, 1), font_size="15sp", padding=(5, 5))
    prev_button.bind(on_press=partial(self._widget.RequestNextSpellCallback, -1))    # pylint: disable=no-member

    close_button = Button(text="Close", size_hint=(0.2, 1), font_size="15sp", padding=(5, 5))
    close_button.bind(on_press=self._Close)    # pylint: disable=no-member

    next_button = Button(text=">", size_hint=(0.4, 1), font_size="15sp", padding=(5, 5))
    next_button.bind(on_press=partial(self._widget.RequestNextSpellCallback, 1))    # pylint: disable=no-member

    layout.add_widget(prev_button)
    layout.add_widget(close_button)
    layout.add_widget(next_button)
    return layout


###################################################################################################
###################################################################################################
###################################################################################################
