###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from functools import partial

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout

from dnd_app.core.config import Config
from dnd_app.utilities.text_utils import StrFieldToReadable

###################################################################################################
###################################################################################################
###################################################################################################


class WeaponListRenderer(BoxLayout):

  ids = {}
  ids['weapon_table'] = ObjectProperty("")

  def __init__(self, config: Config, widget):
    super().__init__()
    self._dnd_config = config
    self._widget = widget

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    self.ids['weapon_table'].clear_widgets()

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    for v in data.values():
      for weapon in v:
        if isinstance(weapon, list):
          self._AddWeapon(weapon)

###################################################################################################

  def _AddWeapon(self, weapon_data: dict):
    layout = Factory.WeaponListRendererWeaponRow()
    layout.ids['name'].text = StrFieldToReadable(weapon_data[0])
    layout.ids['attack'].text = StrFieldToReadable(weapon_data[1])
    layout.ids['damage'].text = StrFieldToReadable(weapon_data[2])
    layout.ids['name'].bind(on_press=partial(self._widget.RequestCallback, "weapon", weapon_data[0]))    # pylint: disable=no-member
    self.ids['weapon_table'].add_widget(layout)


###################################################################################################
###################################################################################################
###################################################################################################
