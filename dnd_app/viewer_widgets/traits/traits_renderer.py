###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.properties import StringProperty, NumericProperty    #pylint: disable=no-name-in-module
from kivy.uix.boxlayout import BoxLayout

from dnd_app.core.config import Config
from dnd_app.utilities.container_utils import FlattenDict
from dnd_app.utilities.text_utils import GetRendererLabelFromFilename

###################################################################################################
###################################################################################################
###################################################################################################


class TraitsRenderer(BoxLayout):

  ids = {}
  ids['appearance_age'] = NumericProperty()
  ids['appearance_height'] = NumericProperty()
  ids['appearance_weight'] = NumericProperty()
  ids['appearance_eyes'] = NumericProperty()
  ids['appearance_skin'] = NumericProperty()
  ids['appearance_hair'] = NumericProperty()
  ids['traits_personality_traits'] = StringProperty("")
  ids['traits_ideals'] = StringProperty("")
  ids['traits_bonds'] = StringProperty("")
  ids['traits_flaws'] = StringProperty("")

###################################################################################################

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    for v_ in self.ids.values():
      v_.text = ""

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    flattened_data = FlattenDict(data)
    for k, v in flattened_data.items():
      for k_, v_ in self.ids.items():
        if k_ == k:
          v_.text = str(v)
          break

###################################################################################################

  def GetLabel(self):
    return GetRendererLabelFromFilename(__file__)


###################################################################################################
###################################################################################################
###################################################################################################
