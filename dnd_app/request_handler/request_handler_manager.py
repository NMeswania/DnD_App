###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import queue

from multiprocessing import Process, Queue, Pipe

from dnd_app.core.config import Config
from dnd_app.core.thread_safe_singleton import ThreadSafeSingleton
from dnd_app.request_handler.receipt import Receipt
from dnd_app.request_handler.request import Request
from dnd_app.request_handler.response import Response
from dnd_app.request_handler.request_handler import RequestHandler
from dnd_app.request_handler.internal.request_dispatch import RequestDispatch

###################################################################################################
###################################################################################################
###################################################################################################

def GetRequestHandlerManagerSingleton():
  return RequestHandlerManager(None, None, None)

###################################################################################################
###################################################################################################
###################################################################################################


class RequestHandlerManager(metaclass=ThreadSafeSingleton):

  def __init__(self, config: Config, request_queue: Queue, failure_queue: Queue) -> None:
    self._config = config
    self._request_queue = request_queue
    self._failure_queue = failure_queue

###################################################################################################

  def __del__(self):
    self._Shutdown()

###################################################################################################

  def run(self):
    self._LaunchProcesses()

###################################################################################################

  def Request(self, request: Request) -> Receipt:
    conn_1, conn_2 = Pipe()

    request_id = request._id
    request_type = request.type()
    request_value = request.value()
    request_dispatch = RequestDispatch(request, conn_2)

    try:
      self._request_queue.put(request_dispatch,
                              block=False,
                              timeout=self._config.get_common("queue_put_timeout"))

    except queue.Full:
      logging.critical(f"Failed to put request in job queue ({request.id()})")

    else:
      logging.info(f"Sent request for {request_type}:{request_value}, {request_id}")

    return Receipt(request_id, conn_1)

###################################################################################################

  def RequestAndBlock(self, request: Request) -> Response:
    receipt = self.Request(request)
    while True:
      if receipt.IsResponseReady():
        return receipt.GetResponse()

###################################################################################################

  def _Shutdown(self):
    for process_handler in self._processes_handlers.values():
      process_handler["process"].join()

###################################################################################################

  def _LaunchProcesses(self):
    self._processes_handlers = {}

    # Create processes
    for i in range(self._config.get("num_processes")):
      self._processes_handlers[f'process_{i}'] = {}

      request_handler = RequestHandler(self._config(), self._request_queue, self._failure_queue)
      p = Process(target=request_handler)

      self._processes_handlers[f'process_{i}']['process'] = p
      self._processes_handlers[f'process_{i}']['handler'] = request_handler

      p.start()

    logging.info(f"Launched {self._config.get('num_processes')} RequestHandler processes.")


###################################################################################################
###################################################################################################
###################################################################################################
