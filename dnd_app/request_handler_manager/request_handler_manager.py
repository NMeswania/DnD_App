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
    self._config = config
    self._request_queue = request_queue
    self._response_queue = response_queue

###################################################################################################

  def __del__(self):
    self._Shutdown()

###################################################################################################

  def run(self):
    self._LaunchProcesses()


###################################################################################################

  def _Shutdown(self):
    for process_handler in self._processes_handlers.values():
      process_handler["process"].terminate()
      process_handler["process"].join()

###################################################################################################

  def _LaunchProcesses(self):
    self._processes_handlers = {}

    # Create processes
    for i in range(self._config.get("num_processes")):
      self._processes_handlers[f'process_{i}'] = {}

      request_handler = RequestHandler(self._config(), self._request_queue, self._response_queue)
      p = Process(target=request_handler)

      self._processes_handlers[f'process_{i}']['process'] = p
      self._processes_handlers[f'process_{i}']['handler'] = request_handler

      p.start()


###################################################################################################
###################################################################################################
###################################################################################################
