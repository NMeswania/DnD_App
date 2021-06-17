###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from dnd_app.core.config import Config
from dnd_app.utilities.text_utils import StrFieldToReadable, AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class SpellListRenderer(BoxLayout):

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
    self.add_widget(self._AddTitle())
    self.add_widget(self._AddContent())
    self._spells = []

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    self._spell_layout.clear_widgets()
    self._spells = []

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    for k, v in data.items():
      if isinstance(v, list) and len(v) > 0:
        level_layout = self._AddSpellLevel(k)
        for spell in v:
          level_layout.add_widget(self._AddSpell(spell_name=spell))
        self._spell_layout.add_widget(level_layout)
      elif isinstance(v, dict):
        for k_, v_ in v.items():
          for child in self.walk(restrict=True):
            if hasattr(child, "id") and child.id == k_:
              child.text = str(v_)
              break

###################################################################################################

  def GetNextSpellAndIndex(self, index: int) -> list:
    idx = index % len(self._spells)
    return [self._spells[idx], idx]

###################################################################################################

  def _AddContent(self):
    layout = BoxLayout(orientation="vertical")
    layout.add_widget(self._AddInfo())
    self._spell_layout = self._AddSpells()
    layout.add_widget(self._spell_layout)
    return layout

###################################################################################################

  def _AddTitle(self) -> Label:
    return Label(text="Spells", font_size="20sp", size_hint=(1, 0.05))

###################################################################################################

  def _AddInfo(self) -> BoxLayout:
    layout = BoxLayout(orientation="horizontal", height=40)
    for field in ["ability", "save", "attack"]:
      layout.add_widget(self._AddInfoLabel(field))
    return layout

###################################################################################################

  def _AddInfoLabel(self, field: str) -> BoxLayout:
    layout = BoxLayout(orientation="horizontal")
    layout.add_widget(
        Label(text=StrFieldToReadable(field), font_size="13sp", italic=True, size_hint=(0.4, 1)))
    label = Label(text="", font_size="14sp", size_hint=(0.6, 1))
    label.id = field
    layout.add_widget(label)
    return layout

###################################################################################################

  def _AddSpells(self) -> GridLayout:
    layout = GridLayout(cols=5)
    return layout

###################################################################################################

  def _AddSpellLevel(self, level: str) -> GridLayout:
    layout = GridLayout(cols=1, row_force_default=True, row_default_height=40, padding=5)
    layout.id = level
    layout.add_widget(
        Label(text=StrFieldToReadable(level, strip_end_numbers=False), size_hint=(1, 1)))
    return layout

###################################################################################################

  def _AddSpell(self, spell_name: str) -> BoxLayout:
    self._spells.append(spell_name)
    layout = BoxLayout(orientation="horizontal", size=(100, 1))
    layout.add_widget(self._AddSpellCheckBox())
    layout.add_widget(self._AddSpellButton(spell_name))
    return layout

###################################################################################################

  def _AddSpellButton(self, spell_name: str) -> Button:
    btn = Button(text=StrFieldToReadable(spell_name),
                 size_hint=(0.9, 1),
                 font_size="13sp",
                 padding=(5, 5))
    AlignWidgetLabelChildren(btn)
    btn.bind(on_press=partial(self._widget.RequestSpellCallback, spell_name, len(self._spells)))    # pylint: disable=no-member
    return btn

###################################################################################################

  def _AddSpellCheckBox(self) -> CheckBox:
    return CheckBox(active=False, size_hint=(0.1, 1))


###################################################################################################
###################################################################################################
###################################################################################################
