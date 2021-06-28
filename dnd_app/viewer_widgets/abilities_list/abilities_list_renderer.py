###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from functools import partial

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from dnd_app.core.config import Config
from dnd_app.utilities.text_utils import StrFieldToReadable

###################################################################################################
###################################################################################################
###################################################################################################


class AbilitiesListRenderer(BoxLayout):

  ids = {}
  ids['content'] = ObjectProperty("")

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
    self._abilities_list = []

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    self.ids['content'].clear_widgets()
    self._abilities_list = []

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    for v in data.values():
      for ability in v:
        self._AddAbilityButton(ability)

###################################################################################################

  def GetNextAbilityAndIndex(self, index: int) -> list:
    idx = index % len(self._abilities_list)
    return [self._abilities_list[idx], idx]

###################################################################################################

  def _AddAbilityButton(self, ability_name: str) -> Button:
    self._abilities_list.append(ability_name)
    btn = Factory.AbilitiesListRendererButtonBarButton()
    btn.name = ability_name
    btn.text = StrFieldToReadable(ability_name)
    btn.bind(on_press=partial(self._widget.RequestCallback, ability_name,
                              len(self._abilities_list) - 1))
    self.ids['content'].add_widget(btn)


###################################################################################################
###################################################################################################
###################################################################################################
