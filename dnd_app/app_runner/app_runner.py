###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import multiprocessing

from dnd_app.core.config import Config
from dnd_app.request_handler_manager.request_handler_manager import RequestHandlerManager
from dnd_app.viewer.viewer import Viewer

###################################################################################################
###################################################################################################
###################################################################################################


class AppRunner:

  def __init__(self, config: Config) -> None:
    self._config = config
    self._request_handler_request_queue = multiprocessing.Queue()
    self._request_handler_response_queue = multiprocessing.Queue()

    self._request_handler_manager = RequestHandlerManager(config('request_handler_manager'),
                                                          self._request_handler_request_queue,
                                                          self._request_handler_response_queue)
    self._viewer = Viewer(config('viewer'), self._request_handler_request_queue,
                          self._request_handler_response_queue)

    self._processes = {}

###################################################################################################

  def __del__(self):
    self._Shutdown()

###################################################################################################

  def run(self):
    self._LaunchRequestHandlerManagerProcess()
    # self._LaunchViewerProcess()
    self._viewer.run()

###################################################################################################

  def _LaunchRequestHandlerManagerProcess(self):
    self._processes['request_handler_manager'] = multiprocessing.Process(
        target=self._request_handler_manager.run)
    self._processes['request_handler_manager'].start()

###################################################################################################

  def _LaunchViewerProcess(self):
    self._processes['spoofer'] = multiprocessing.Process(target=self._viewer.run)
    self._processes['spoofer'].start()

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
