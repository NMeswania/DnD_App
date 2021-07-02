###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from dnd_app.core.config import Config
from dnd_app.failure_handler.failure_handler_listener import FailureHandlerListener
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
    self._widgets_to_load = self._GetWidgetsToLoad(self._character)

###################################################################################################

  def run(self):
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

  def GetViewerWidgetsToLoad(self) -> list:
    return list((set(self._dnd_config.get("dont_load_widgets")) ^ set(self._widgets_to_load)) &
                set(self._widgets_to_load))

###################################################################################################

  def _GetWidgetsToLoad(self, character: str="") -> list:
    data_dir = self._dnd_config.get_data_dir()
    return [json_file.stem for json_file in (data_dir / "character" / character).iterdir()]

###################################################################################################

  def _LoadWidgets(self) -> dict:
    widgets = {}

    widgets_to_not_load = self._dnd_config.get("dont_load_widgets")
    if "main_info" not in widgets_to_not_load:
      widgets['main_info'] = MainInfo(self._dnd_config, self._character)

    if "abilities_list" not in widgets_to_not_load:
      widgets['abilities_list'] = AbilitiesList(self._dnd_config, self._character)

    if "ability_scores" not in widgets_to_not_load:
      widgets['ability_scores'] = AbilityScores(self._dnd_config, self._character)

    if "combat" not in widgets_to_not_load:
      widgets['combat'] = Combat(self._dnd_config, self._character)

    if "equipment_list" not in widgets_to_not_load:
      widgets['equipment_list'] = EquipmentList(self._dnd_config, self._character)

    if "proficiencies" not in widgets_to_not_load:
      widgets['proficiencies'] = Proficiencies(self._dnd_config, self._character)

    if "traits" not in widgets_to_not_load:
      widgets['traits'] = Traits(self._dnd_config, self._character)

    if "weapon_list" not in widgets_to_not_load:
      widgets['weapon_list'] = WeaponList(self._dnd_config, self._character)

    if "spell_list" in self._widgets_to_load and not "spell_list" in widgets_to_not_load:
      widgets['spell_list'] = SpellList(self._dnd_config, self._character)

    return widgets


###################################################################################################
###################################################################################################
###################################################################################################
