###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from pathlib import Path

from dnd_app.core.config import Config
from dnd_app.request_handler.request import Request
from dnd_app.request_handler.request_handler_manager import GetRequestHandlerManagerSingleton
from dnd_app.viewer_widgets.proficiencies.proficiencies_renderer import ProficienciesRenderer
from dnd_app.viewer_widgets.widget_base import WidgetBase

###################################################################################################
###################################################################################################
###################################################################################################


class Proficiencies(WidgetBase):

  def __init__(self, config: Config, proficiencies_path: Path):
    self._dnd_config = config
    self._receipt = None
    self._LoadData(proficiencies_path)
    self._BuildRenderers()

###################################################################################################

  def __del__(self):
    self._renderer.Terminate()
    del self._renderer

###################################################################################################

  def renderers(self) -> ProficienciesRenderer:
    return self._renderer

###################################################################################################

  def CheckForUpdates(self):
    if self._receipt is not None:
      if self._receipt.IsResponseReady():
        response = self._receipt.GetResponse()
        self._renderer.Update(response.data())
        self._receipt = None

###################################################################################################

  def _LoadData(self, ability_score_path: Path):
    request = Request(type="character", value="subs/proficiencies")
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    self._receipt = request_manager_singleton.Request(request)

###################################################################################################

  def _BuildRenderers(self) -> ProficienciesRenderer:
    self._renderer = ProficienciesRenderer(self._dnd_config, self)


###################################################################################################
###################################################################################################
###################################################################################################
