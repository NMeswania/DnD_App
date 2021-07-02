###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout

from dnd_app.core.config import Config
from dnd_app.utilities.text_utils import StrFieldToReadable

###################################################################################################
###################################################################################################
###################################################################################################


class ProficienciesRenderer(BoxLayout):

  ids = {}
  ids['content'] = ObjectProperty("")

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    self.ids['content'].clear_widgets()

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    for k, v in data.items():
      if isinstance(v, list) and len(v) > 0:
        self._AddProficiencyGroup(k, v)

###################################################################################################

  def _AddProficiencyGroup(self, group_name: str, group_content: list):
    layout = Factory.ProficienciesRendererProficiencyGroup()
    layout.ids['heading'].text = StrFieldToReadable(group_name)

    for item in group_content:
      label = Factory.ProficienciesRendererProficiencyItem()
      label.text = StrFieldToReadable(item)
      layout.add_widget(label)

    self.ids['content'].add_widget(layout)

###################################################################################################
###################################################################################################
###################################################################################################
