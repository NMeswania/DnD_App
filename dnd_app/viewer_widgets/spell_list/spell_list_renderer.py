###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import numpy as np

from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from dnd_app.core.config import Config
from dnd_app.request_handler.response import Response
from dnd_app.viewer_widgets.spell_list.detail_renderer import DetailRenderer
from dnd_app.utilities.text_utils import StrFieldToReadable, AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class SpellListRenderer(BoxLayout):

  def __init__(self, config: Config, widget):
    super().__init__(orientation="horizontal")
    self._dnd_config = config
    self._widget = widget
    self._detail_renderer = DetailRenderer()
    self.add_widget(self._AddSpells())
    self.add_widget(self._detail_renderer)

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def DisplayResponse(self, response: Response):
    response_type = response.request.type()
    if response_type == "spell":
      self._detail_renderer.Update(response.data())

    elif response_type == "characters":
      self.Update(response.data())

    else:
      logging.critical(f"Unknown response type in SpellListRenderer: {response_type}")

###################################################################################################

  def Update(self, data: dict):
    for k, v in data.items():
      for child in self.walk():
        if hasattr(child, 'id') and child.id == k:
          for spell in v:
            child.add_widget(self._AddSpell(spell_name=spell))
          break

###################################################################################################

  def _AddSpells(self) -> GridLayout:
    layout = GridLayout(rows=2, cols=5, size_hint=(0.7, 1))
    levels = [f"level_{n}" for n in np.arange(1, 10)]
    levels.insert(0, "cantrip")
    for spell_level in levels:
      layout.add_widget(self._AddSpellLevel(spell_level))
    return layout

###################################################################################################

  def _AddSpellLevel(self, level: str) -> GridLayout:
    layout = GridLayout(cols=1, row_force_default=True, row_default_height=40)
    layout.id = level
    layout.add_widget(Label(text=StrFieldToReadable(level), size_hint=(1, 1)))
    return layout

###################################################################################################

  def _AddSpell(self, spell_name: str) -> BoxLayout:
    layout = BoxLayout(orientation="horizontal", size=(100, 1))
    layout.add_widget(self._AddSpellCheckBox())
    layout.add_widget(self._AddSpellButton(spell_name))
    return layout

###################################################################################################

  def _AddSpellButton(self, spell_name: str) -> Button:
    btn = Button(text=StrFieldToReadable(spell_name), size_hint=(0.9, 1), font_size="15sp")
    AlignWidgetLabelChildren(btn)
    btn.bind(on_press=partial(self._widget.RequestSpellCallback, spell_name))  # pylint: disable=no-member
    return btn

###################################################################################################

  def _AddSpellCheckBox(self) -> CheckBox:
    return CheckBox(active=False, size_hint=(0.1, 1))


###################################################################################################
###################################################################################################
###################################################################################################
