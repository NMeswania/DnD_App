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
from dnd_app.utilities.text_utils import StrFieldToReadable

###################################################################################################
###################################################################################################
###################################################################################################


class SpellListRenderer(BoxLayout):

  def __init__(self, config: Config, widget, spell_data: dict):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
    self._spell_data = spell_data
    self.add_widget(self._AddSpells())

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    pass

###################################################################################################

  def _AddSpells(self) -> GridLayout:
    layout = GridLayout(rows=2, cols=5, size_hint=(1, 1))
    for spell_level, spell_list_for_level in self._spell_data.items():
      layout.add_widget(self._AddSpellLevel(spell_level, spell_list_for_level))
    return layout

###################################################################################################

  def _AddSpellLevel(self, level:str, level_spells: list) -> GridLayout:
    layout = GridLayout(cols=1, row_force_default=True, row_default_height=40)
    layout.add_widget(Label(text=StrFieldToReadable(level), size_hint=(1, 1)))
    for spell in level_spells:
      layout.add_widget(self._AddSpell(spell))
    return layout

###################################################################################################

  def _AddSpell(self, spell_name: str) -> BoxLayout:
    layout = BoxLayout(orientation="horizontal", size=(100, 1))
    layout.add_widget(self._AddSpellCheckBox())
    layout.add_widget(self._AddSpellButton(spell_name))
    return layout

###################################################################################################

  def _AddSpellButton(self, spell_name: str) -> Button:
    btn = Button(text=StrFieldToReadable(spell_name), size_hint=(0.9, 1))
    btn.bind(on_press=partial(self._widget.RequestSpellCallback, spell_name))
    return btn

###################################################################################################

  def _AddSpellCheckBox(self) -> CheckBox:
    return CheckBox(active=False, size_hint=(0.1, 1))


###################################################################################################
###################################################################################################
###################################################################################################
