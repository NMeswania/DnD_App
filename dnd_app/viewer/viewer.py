###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.uix.boxlayout import BoxLayout

###################################################################################################
###################################################################################################
###################################################################################################


class Viewer(BoxLayout):

  ids = {}
  ids['scroll_content'] = ObjectProperty("")
  ids['main_info'] = ObjectProperty("")
  ids['ability_scores'] = ObjectProperty("")

  def __init__(self):
    super().__init__()
    self._height = 0

###################################################################################################

  def add_renderer(self, renderer):
    renderer_label = renderer.GetLabel()
    if renderer_label in self.ids.keys():
      self.ids[renderer_label].add_widget(renderer)
      self._height += renderer.height

    self.ids['scroll_content'].height = self._height


###################################################################################################
###################################################################################################
###################################################################################################
