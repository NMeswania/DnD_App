###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging

from pathlib import Path

from kivy.clock import Clock
from dnd_app.core.config import Config
from dnd_app.request_handler.request import Request
from dnd_app.request_handler.request_handler_manager import GetRequestHandlerManagerSingleton
from dnd_app.viewer_widgets.widget_base import WidgetBase
from dnd_app.viewer_widgets.spell_list.spell_list_renderer import SpellListRenderer

###################################################################################################
###################################################################################################
###################################################################################################


class SpellList(WidgetBase):

  def __init__(self, config: Config, spell_list_path: Path):
    self._dnd_config = config
    self._receipt = None
    self._LoadData(spell_list_path)
    self._renderer = self._BuildRenderer()

###################################################################################################

  def __del__(self):
    self._renderer.Terminate()
    del self._renderer

###################################################################################################

  def renderer(self) -> SpellListRenderer:
    return self._renderer

###################################################################################################

  def RequestSpellCallback(self, spell_name: str, instance):
    request = Request(type="spell", value=spell_name)
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    self._receipt = request_manager_singleton.Request(request)

###################################################################################################

  def CheckForUpdates(self):
    if self._receipt is not None:
      if self._receipt.IsResponseReady():
        response = self._receipt.GetResponse()
        self._renderer.DisplayResponse(response)
        self._receipt = None

###################################################################################################

  def _LoadData(self, spell_list_path: Path):
    request = Request(type="characters", value="subs/spell_list")
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    self._receipt = request_manager_singleton.Request(request)

###################################################################################################

  def _BuildRenderer(self) -> SpellListRenderer:
    return SpellListRenderer(self._dnd_config, self)


###################################################################################################
###################################################################################################
###################################################################################################
