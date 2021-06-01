###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from dnd_app.core.config import Config
from dnd_app.request_handler.request import Request
from dnd_app.request_handler.request_handler_manager import GetRequestHandlerManagerSingleton
from dnd_app.viewer_widgets.ability_scores.ability_scores import AbilityScores
from dnd_app.viewer_widgets.spell_list.spell_list import SpellList

###################################################################################################
###################################################################################################
###################################################################################################


class WidgetManager:

  def __init__(self, config: Config, character: str=""):
    self._dnd_config = config
    self._character = character

###################################################################################################

  def run(self):
    self._character_data = self._GetCharacterData(self._character)
    self._widgets = self._LoadWidgets()

###################################################################################################

  def CheckForUpdates(self, _):
    for widget in self._widgets.values():
      widget.CheckForUpdates()

###################################################################################################

  def GetRenderers(self) -> list:
    renderers = [widget.renderer() for widget in self._widgets.values()]
    return renderers

###################################################################################################

  def _GetCharacterData(self, character: str="") -> dict:
    request = Request(type="character", value=f"{character}/main")
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    response = request_manager_singleton.RequestAndBlock(request)
    return response.data()

###################################################################################################

  def _LoadWidgets(self) -> dict:
    widgets = {}
    widgets_to_load = self._dnd_config.get("widgets")
    if "ability_scores" in widgets_to_load:
      widgets['ability_scores'] = AbilityScores(self._dnd_config, self._character_data['ability_scores'])
    if "spell_list" in widgets_to_load:
      widgets['spell_list'] = SpellList(self._dnd_config, self._character_data['spell_list'])
    return widgets


###################################################################################################
###################################################################################################
###################################################################################################
