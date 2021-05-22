###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from multiprocessing import Process, Queue

from dnd_app.core.config import Config
from dnd_app.request_handler.request_handler import RequestHandler

###################################################################################################
###################################################################################################
###################################################################################################


class RequestHandlerManager:

  def __init__(self, config: Config, request_queue: Queue, response_queue: Queue) -> None:
    self.config = config
    self.request_queue = request_queue
    self.response_queue = response_queue

###################################################################################################

  def __del__(self):
    self._shutdown()

###################################################################################################

  def run(self):
    self._LaunchProcesses()


###################################################################################################

  def _shutdown(self):
    for process_handler in self.processes_handlers.values():
      process_handler["process"].terminate()
      process_handler["process"].join()

###################################################################################################

  def _LaunchProcesses(self):
    self.processes_handlers = {}

    # Create processes
    for i in range(self.config.get("num_processes")):
      self.processes_handlers[f'process_{i}'] = {}

      request_handler = RequestHandler(self.config(), self.request_queue, self.response_queue)
      p = Process(target=request_handler)

      self.processes_handlers[f'process_{i}']['process'] = p
      self.processes_handlers[f'process_{i}']['handler'] = request_handler

      p.start()


###################################################################################################
###################################################################################################
###################################################################################################
