###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import queue

from multiprocessing import Queue

from dnd_app.core.config import Config
from dnd_app.core.request import Request
from dnd_app.core.response import Response
from dnd_app.request_handler.request_handler_exceptions import RequestHandlerException

###################################################################################################
###################################################################################################
###################################################################################################


class RequestHandler:

  def __init__(self, config: Config, request_queue: Queue, response_queue: Queue) -> None:
    self.config = config
    self.request_queue = request_queue
    self.response_queue = response_queue

###################################################################################################

  def __call__(self):
    while True:
      try:
        request = self.request_queue.get(block=True,
                                         timeout=self.config.get_common("queue_put_timeout"))
        response = self._ProcessNewRequest(request)

        try:
          self.response_queue.put(response,
                                  block=True,
                                  timeout=self.config.get_common("queue_get_timeout"))

        except queue.Full:
          logging.critical(
              f"Failed to put response in queue. Response id: {response.request.id()}")

      except queue.Empty:
        pass

      except RequestHandlerException as err:
        logging.critical(f"Got exception when trying to handler request, exception: {err}")

###################################################################################################

  def _ProcessNewRequest(self, request: Request):
    response_data = f"Done the thing for: {request.data['value']}"

    return Response(request, {'value': response_data})


###################################################################################################
###################################################################################################
###################################################################################################