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
    self.config = config
    self.request_handler_request_queue = multiprocessing.Queue()
    self.request_handler_response_queue = multiprocessing.Queue()

    self.request_handler_manager = RequestHandlerManager(config('request_handler_manager'),
                                                         self.request_handler_request_queue,
                                                         self.request_handler_response_queue)
    self.viewer = Viewer(config('viewer'), self.request_handler_request_queue,
                         self.request_handler_response_queue)

    self.processes = {}

###################################################################################################

  def __del__(self):
    self._shutdown()

###################################################################################################

  def LaunchRequestHandlerManagerProcess(self):
    self.processes['request_handler_manager'] = multiprocessing.Process(
        target=self.request_handler_manager.run)
    self.processes['request_handler_manager'].start()

###################################################################################################

  def LaunchViewerProcess(self):
    self.processes['spoofer'] = multiprocessing.Process(target=self.viewer.run)
    self.processes['spoofer'].start()

###################################################################################################

  def run(self):
    self.LaunchRequestHandlerManagerProcess()
    # self.LaunchViewerProcess()
    self.viewer.run()

###################################################################################################

  def _shutdown(self):
    logging.info(f"Shutting down gracefully, "
                 f"num active processes = {len(multiprocessing.active_children())}")
    for process in self.processes.values():
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
