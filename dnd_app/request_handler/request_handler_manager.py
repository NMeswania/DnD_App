###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import queue
import threading

from multiprocessing import Process, Queue, Pipe
from multiprocessing.connection import Connection

from dnd_app.core.config import Config
from dnd_app.request_handler.receipt import Receipt
from dnd_app.request_handler.request import Request
from dnd_app.request_handler.request_handler import RequestHandler
from dnd_app.request_handler.internal.request_dispatch import RequestDispatch

###################################################################################################
###################################################################################################
###################################################################################################

class ThreadSafeSingleton(type):

  _instances = {}
  _lock = threading.Lock()

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      with cls._lock:
        cls._instances[cls] = super(ThreadSafeSingleton, cls).__call__(*args, **kwargs)

    return cls._instances[cls]

###################################################################################################
###################################################################################################
###################################################################################################


class RequestHandlerManager(metaclass=ThreadSafeSingleton):

  def __init__(self, config: Config, request_queue: Queue) -> None:
    self._config = config
    self._request_queue = request_queue

###################################################################################################

  def __del__(self):
    self._Shutdown()

###################################################################################################

  def run(self):
    self._LaunchProcesses()

###################################################################################################

  def Request(self, request: Request) -> Receipt:
    conn_1, conn_2 = Pipe()

    request_dispatch = RequestDispatch(request, conn_2)

    try:
      self._request_queue.put(request_dispatch,
                              block=False,
                              timeout=self._config.get_common("queue_put_timeout"))

    except queue.Full:
      logging.critical(f"Failed to put request in job queue ({request.id()})")

    return Receipt(request._id, conn_1)

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

      request_handler = RequestHandler(self._config(), self._request_queue)
      p = Process(target=request_handler)

      self._processes_handlers[f'process_{i}']['process'] = p
      self._processes_handlers[f'process_{i}']['handler'] = request_handler

      p.start()


###################################################################################################
###################################################################################################
###################################################################################################

def GetRequestHandlerManagerSingleton():
  return RequestHandlerManager(None, None)

###################################################################################################
###################################################################################################
###################################################################################################
