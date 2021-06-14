###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from dnd_app.core.config import Config
from dnd_app.utilities.text_utils import StrFieldToReadable, AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class AbilitiesListRenderer(BoxLayout):

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
    self._abilities_list = []
    self.add_widget(self._AddTitle())
    self.add_widget(self._AddContent())

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    self._main_layout.clear_widgets()
    self._abilities_list = []

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    for v in data.values():
      for ability in v:
        self._main_layout.add_widget(self._AddAbilityButton(ability))

###################################################################################################

  def GetNextAbilityAndIndex(self, index: int) -> list:
    idx = index % len(self._abilities_list)
    return [self._abilities_list[idx], idx]

###################################################################################################

  def _AddTitle(self) -> Label:
    return Label(text="Abilities", font_size="20sp", size_hint=(1, 0.05))

###################################################################################################

  def _AddContent(self) -> GridLayout:
    self._main_layout = GridLayout(cols=4,
                                   row_default_height=40,
                                   row_force_default=True,
                                   padding=5)
    return self._main_layout

###################################################################################################

  def _AddAbilityButton(self, ability_name: str) -> Button:
    self._abilities_list.append(ability_name)
    btn = Button(text=StrFieldToReadable(ability_name),
                 size_hint=(0.3, 1),
                 font_size="13sp",
                 padding=(5, 5))
    AlignWidgetLabelChildren(btn)
    btn.bind(
        on_press=partial(self._widget.RequestCallback, ability_name, len(self._abilities_list)))
    return btn


###################################################################################################
###################################################################################################
###################################################################################################
