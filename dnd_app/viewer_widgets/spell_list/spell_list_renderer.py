###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from functools import partial

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout

from dnd_app.core.config import Config
from dnd_app.utilities.text_utils import StrFieldToReadable, GetRendererLabelFromFilename

###################################################################################################
###################################################################################################
###################################################################################################


class SpellListRenderer(BoxLayout):

  ids = {}
  ids['ability'] = ObjectProperty("")
  ids['save'] = ObjectProperty("")
  ids['attack'] = ObjectProperty("")
  ids['spell_layout'] = ObjectProperty("")

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
    self._spells = []

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    self.ids['spell_layout'].clear_widgets()
    for v in self.ids.values():
      if hasattr(v, "text"):
        v.text = ""
    self._spells = []

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    self._UpdateInternal(data)

###################################################################################################

  def GetNextSpellAndIndex(self, index: int) -> list:
    idx = index % len(self._spells)
    return [self._spells[idx], idx]

###################################################################################################

  def GetLabel(self):
    return GetRendererLabelFromFilename(__file__)

###################################################################################################

  def _UpdateInternal(self, data):
    for k, v in data.items():
      if isinstance(v, list) and len(v) > 0:
        self._AddSpellLevel(k, v)
      elif isinstance(v, dict):
        self._UpdateInternal(v)
      else:
        for k_, v_ in self.ids.items():
          if k_ == k:
            v_.text = str(v)
            break

###################################################################################################

  def _AddSpellLevel(self, level: str, spells: list):
    layout = Factory.SpellListRendererSpellLevel()
    layout.ids['spell_level'].text = StrFieldToReadable(level, strip_end_numbers=False)

    for spell in spells:
      self._spells.append(spell)
      spell_layout = Factory.SpellListRendererSpell()
      spell_layout.ids['name'].text = StrFieldToReadable(spell)
      spell_layout.ids['name'].bind(on_press=partial(self._widget.RequestSpellCallback, spell,
                                                     len(self._spells) - 1))    # pylint: disable=no-member
      layout.add_widget(spell_layout)

    self.ids['spell_layout'].add_widget(layout)


###################################################################################################
###################################################################################################
###################################################################################################
