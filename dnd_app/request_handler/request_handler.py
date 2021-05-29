###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import queue

from multiprocessing import Queue

from dnd_app.core.config import Config
from dnd_app.core.json_parser import JSONParser
from dnd_app.request_handler.request import Request
from dnd_app.request_handler.response import Response
from dnd_app.request_handler.exceptions import RequestHandlerException, FailedToProcessRequest

###################################################################################################
###################################################################################################
###################################################################################################


class RequestHandler:

  def __init__(self, config: Config, request_queue: Queue):
    self._config = config
    self._request_queue = request_queue

###################################################################################################

  def __call__(self):
    while True:
      try:
        request_dispatch = self._request_queue.get(
            block=True, timeout=self._config.get_common("queue_get_timeout"))
        response = self._ProcessNewRequest(request_dispatch.request)
        request_dispatch.pipe_connection.send(response)

      except queue.Empty:
        pass

      except RequestHandlerException as err:
        logging.critical(f"Got exception when trying to handler request, exception: {err}")

###################################################################################################

  def _ProcessNewRequest(self, request: Request):
    try:
      data_dir = self._config.get_data_dir()
      glob_pattern = f"{request.type()}/{request.value()}.json"
      found_files = sorted(data_dir.glob(glob_pattern))
      if len(found_files) == 0:
        logging.critical(f"No matching pattern '{glob_pattern}'")
        raise FailedToProcessRequest

      elif len(found_files) > 1:
        logging.warning(
            f"Found {len(found_files)} matching pattern '{glob_pattern}', using first match")

      response_data = JSONParser(found_files[0]).ParseData()


    except Exception as err:
      logging.error(f"Failed to process request: {request.id()}. Got exception: {err}")
      return Response(request, repsonse_data={}, fulfilled=False)

    else:
      return Response(request, response_data)


###################################################################################################
###################################################################################################
###################################################################################################
