###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import multiprocessing

from dnd_app.data_manager_interface.data_manager_interface import DataManagerInterface
from dnd_app.viewer.viewer_spoofer import ViewerSpoofer

###################################################################################################
###################################################################################################
###################################################################################################


class AppRunner:

  def __init__(self) -> None:
    self.data_manager_request_queue = multiprocessing.Queue()
    self.data_manager_response_queue = multiprocessing.Queue()

    self.data_manager_interface = DataManagerInterface(self.data_manager_request_queue,
                                                       self.data_manager_response_queue)
    self.viewer_spoofer = ViewerSpoofer(self.data_manager_request_queue,
                                                self.data_manager_response_queue)

    self.processes = {}

###################################################################################################

  def __del__(self):
    self._shutdown()

###################################################################################################

  def LaunchDataManagerInterfaceProcess(self):
    self.processes['data_manager_interface'] = multiprocessing.Process(target=self.data_manager_interface)
    self.processes['data_manager_interface'].start()

###################################################################################################

  def LaunchViewerSpooferProcess(self):
    self.processes['spoofer'] = multiprocessing.Process(target=self.viewer_spoofer)
    self.processes['spoofer'].start()

###################################################################################################

  def run(self):
    self.LaunchDataManagerInterfaceProcess()
    self.LaunchViewerSpooferProcess()

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
