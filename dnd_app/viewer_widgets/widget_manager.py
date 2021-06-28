###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from dnd_app.core.config import Config
from dnd_app.failure_handler.failure_handler_listener import FailureHandlerListener
from dnd_app.request_handler.request import Request
from dnd_app.request_handler.request_handler_manager import GetRequestHandlerManagerSingleton
from dnd_app.utilities.container_utils import FlattenList

from dnd_app.viewer_widgets.abilities_list.abilities_list import AbilitiesList
from dnd_app.viewer_widgets.ability_scores.ability_scores import AbilityScores
from dnd_app.viewer_widgets.combat.combat import Combat
from dnd_app.viewer_widgets.equipment_list.equipment_list import EquipmentList
from dnd_app.viewer_widgets.main_info.main_info import MainInfo
from dnd_app.viewer_widgets.proficiencies.proficiencies import Proficiencies
from dnd_app.viewer_widgets.spell_list.spell_list import SpellList
from dnd_app.viewer_widgets.traits.traits import Traits
from dnd_app.viewer_widgets.weapon_list.weapon_list import WeaponList

###################################################################################################
###################################################################################################
###################################################################################################


class WidgetManager:

  def __init__(self,
               config: Config,
               failure_listener: FailureHandlerListener,
               character: str = ""):
    self._dnd_config = config
    self._character = character
    self._failure_listener = failure_listener

###################################################################################################

  def run(self):
    self._character_data = self._GetCharacterData(self._character)
    self._widgets = self._LoadWidgets()
    self._failure_listener.LoadRenderer()

###################################################################################################

  def CheckForUpdates(self, _):
    self._failure_listener.CheckForUpdates()
    for widget in self._widgets.values():
      widget.CheckForUpdates()

###################################################################################################

  def GetRenderers(self) -> list:
    renderers = [widget.renderers() for widget in self._widgets.values()]
    return FlattenList(renderers)

###################################################################################################

  def _GetCharacterData(self, character: str="") -> dict:
    request = Request(type="character", value=f"{character}/main")
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    response = request_manager_singleton.RequestAndBlock(request)
    return response.data()

###################################################################################################

  def _LoadWidgets(self) -> dict:
    widgets = {}
    widgets_to_load = self._character_data.keys()
    widgets_to_not_load = self._dnd_config.get("dont_load_widgets")
    widgets['main_info'] = MainInfo(self._dnd_config, self._character_data['main_info'])

    if "ability_scores" in widgets_to_load and not "ability_scores" in widgets_to_not_load:
      widgets['ability_scores'] = AbilityScores(self._dnd_config, self._character_data['ability_scores'])
    if "combat" in widgets_to_load and not "combat" in widgets_to_not_load:
      widgets['combat'] = Combat(self._dnd_config, self._character_data['combat'])
    if "proficiencies" in widgets_to_load and not "proficiencies" in widgets_to_not_load:
      widgets['proficiencies'] = Proficiencies(self._dnd_config, self._character_data['proficiencies'])
    if "abilities_list" in widgets_to_load and not "abilities_list" in widgets_to_not_load:
      widgets['abilities_list'] = AbilitiesList(self._dnd_config, self._character_data['abilities_list'])
    if "equipment_list" in widgets_to_load and not "equipment_list" in widgets_to_not_load:
      widgets['equipment_list'] = EquipmentList(self._dnd_config, self._character_data['equipment_list'])
    if "spell_list" in widgets_to_load and not "spell_list" in widgets_to_not_load:
      widgets['spell_list'] = SpellList(self._dnd_config, self._character_data['spell_list'])
    if "traits" in widgets_to_load and not "traits" in widgets_to_not_load:
      widgets['traits'] = Traits(self._dnd_config, self._character_data['traits'])
    if "weapon_list" in widgets_to_load and not "weapon_list" in widgets_to_not_load:
      widgets['weapon_list'] = WeaponList(self._dnd_config, self._character_data['weapon_list'])
    return widgets


###################################################################################################
###################################################################################################
###################################################################################################
