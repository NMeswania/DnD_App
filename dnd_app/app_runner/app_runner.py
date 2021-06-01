###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import multiprocessing

from dnd_app.core.config import Config
from dnd_app.request_handler.request_handler_manager import RequestHandlerManager
from dnd_app.viewer.viewer import Viewer
from dnd_app.viewer_widgets.widget_manager import WidgetManager

###################################################################################################
###################################################################################################
###################################################################################################


class AppRunner:

  def __init__(self, config: Config) -> None:
    self._config = config
    self._request_queue = multiprocessing.Queue()

    self._request_handler_manager = RequestHandlerManager(config('request_handler_manager'),
                                                          self._request_queue)
    self._widget_manager = WidgetManager(config('widget_manager'), "subs")
    self._viewer = Viewer(config('viewer'), self._widget_manager, self._request_queue)

    self._processes = {}

###################################################################################################

  def __del__(self):
    self._Shutdown()

###################################################################################################

  def run(self):
    self._LaunchRequestHandlerManagerProcess()
    self._LaunchWidgetManager()
    self._LaunchViewer()

###################################################################################################

  def _LaunchRequestHandlerManagerProcess(self):
    self._processes['request_handler_manager'] = multiprocessing.Process(
        target=self._request_handler_manager.run)
    self._processes['request_handler_manager'].start()

###################################################################################################

  def _LaunchViewer(self):
    self._viewer.run()

###################################################################################################

  def _LaunchWidgetManager(self):
    self._widget_manager.run()

###################################################################################################

  def _Shutdown(self):
    logging.info(f"Shutting down gracefully, "
                 f"num active processes = {len(multiprocessing.active_children())}")
    for process in self._processes.values():
      process.terminate()
      process.join()

    num_active_children = len(multiprocessing.active_children())
    if num_active_children != 0:
      logging.critical(
          f"Failed to shutdown gracefully, still have {num_active_children} active processes.")
    logging.info("Shutdown processes gracefuly, you're welcome")


###################################################################################################
###################################################################################################
###################################################################################################
