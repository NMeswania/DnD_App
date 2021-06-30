###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from functools import partial

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.factory import Factory
from kivy.uix.popup import Popup

from dnd_app.utilities.text_utils import StrFieldToReadable

###################################################################################################
###################################################################################################
###################################################################################################


class WeaponDetailRenderer(Popup):

  ids = {}
  ids['name'] = ObjectProperty("")
  ids['weapon_description'] = ObjectProperty("")
  ids['tags'] = ObjectProperty("")

  def __init__(self, widget):
    super().__init__()
    self._widget = widget
    self._is_open = False

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    self.ids['tags'].clear_widgets()
    for v in self.ids.values():
      if hasattr(v, "text"):
        v.text = ""

###################################################################################################

  def Update(self, weapon_data: dict):
    if not self._is_open:
      self.open()
      self._is_open = True
    else:
      self.Clear()
    self._UpdateInternal(weapon_data)

###################################################################################################

  def _UpdateInternal(self, weapon_data: dict):
    for k, v in weapon_data.items():
      if isinstance(v, list) and k == "tags":
        for tag in v:
          self._AddTag(tag)
      else:
        for k_, v_ in self.ids.items():
          if k_ == k:
            v_.text = v
            break

###################################################################################################

  def _Close(self):
    self._is_open = False
    self.dismiss()

###################################################################################################

  def _AddTag(self, tag_name):
    btn = Factory.WeaponDetailRendererTag()
    btn.text = StrFieldToReadable(tag_name)
    btn.bind(on_press=partial(self._widget.RequestCallback, "weapon_attribute", tag_name))    # pylint: disable=no-member
    self.ids['tags'].add_widget(btn)


###################################################################################################
###################################################################################################
###################################################################################################
