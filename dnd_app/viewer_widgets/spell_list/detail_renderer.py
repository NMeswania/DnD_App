###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from dnd_app.utilities.text_utils import StrFieldToReadable, AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class DetailRenderer(BoxLayout):

  def __init__(self):
    super().__init__(orientation="vertical", size_hint=(0.3, 1))
    self._AddSpellName()
    self._AddBasicData()
    self._AddDescriptions()

###################################################################################################

  def Clear(self):
    for widget in self.walk():
      if hasattr(widget, "id"):
        widget.text = ""

###################################################################################################

  def Update(self, spell_data: dict):
    self.Clear()
    self._UpdateInternal(spell_data)

###################################################################################################

  def _UpdateInternal(self, spell_data: dict):
    for k, v in spell_data.items():
      if isinstance(v, dict):
        self._UpdateInternal(v)
      else:
        for child in self.walk():
          if hasattr(child, "id") and child.id == k:
            child.text = v
            break

###################################################################################################

  def _AddSpellName(self):
    label = Label(text="", font_size="18sp", size_hint=(1, 0.3))
    label.id = "name"
    self.add_widget(label)

###################################################################################################

  def _AddBasicData(self):
    layout = GridLayout(rows=4,
                        cols=2,
                        row_force_default=True,
                        row_default_height=40,
                        size_hint=(1, 0.5))

    for field in ["range", "casting_time", "components", "duration"]:
      layout.add_widget(Label(text=StrFieldToReadable(field), bold=True, font_size="13sp"))
      label = Label(text="", font_size="13sp")
      label.id = field
      layout.add_widget(label)

    AlignWidgetLabelChildren(layout)

    self.add_widget(layout)

###################################################################################################

  def _AddDescriptions(self):
    layout = BoxLayout(orientation="vertical")
    for section in ["spell_description", "higher_level_description"]:
      label = Label(text="", font_size="12sp")
      label.id = section
      layout.add_widget(label)
    AlignWidgetLabelChildren(layout, valign="top")
    self.add_widget(layout)


###################################################################################################
###################################################################################################
###################################################################################################
