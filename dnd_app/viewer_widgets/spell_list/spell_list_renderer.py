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
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
    self._detail_renderer = DetailRenderer()
    self.add_widget(self._AddTitle())
    self.add_widget(self._AddContent())

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def DisplayResponse(self, response: Response):
    response_type = response.request.type()
    if response_type == "spell":
      self._detail_renderer.Update(response.data())

    elif response_type == "character":
      self.Update(response.data())

    else:
      logging.critical(f"Unknown response type in SpellListRenderer: {response_type}")

###################################################################################################

  def Clear(self):
    self._spell_layout.clear_widgets()

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    for k, v in data.items():
      if isinstance(v, list) and len(v) > 0:
        level_layout = self._AddSpellLevel(k)
        for spell in v:
          level_layout.add_widget(self._AddSpell(spell_name=spell))
        self._spell_layout.add_widget(level_layout)

###################################################################################################

  def _AddContent(self):
    self._main_layout = BoxLayout(orientation="horizontal")
    self._spell_layout = self._AddSpells()
    self._main_layout.add_widget(self._spell_layout)
    self._main_layout.add_widget(self._detail_renderer)
    return self._main_layout

###################################################################################################

  def _AddTitle(self) -> Label:
    return Label(text="Spells", font_size="20sp", size_hint=(1, 0.05))

###################################################################################################

  def _AddSpells(self) -> GridLayout:
    layout = GridLayout(cols=5)
    return layout

###################################################################################################

  def _AddSpellLevel(self, level: str) -> GridLayout:
    layout = GridLayout(cols=1, row_force_default=True, row_default_height=40, padding=5)
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
    btn = Button(text=StrFieldToReadable(spell_name),
                 size_hint=(0.9, 1),
                 font_size="13sp",
                 padding=(5, 5))
    AlignWidgetLabelChildren(btn)
    btn.bind(on_press=partial(self._widget.RequestSpellCallback, spell_name))  # pylint: disable=no-member
    return btn

###################################################################################################

  def _AddSpellCheckBox(self) -> CheckBox:
    return CheckBox(active=False, size_hint=(0.1, 1))


###################################################################################################
###################################################################################################
###################################################################################################
