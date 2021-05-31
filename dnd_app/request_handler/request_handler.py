###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import json
import logging
import queue

from jsonschema import validate

from multiprocessing import Queue

from dnd_app.core.config import Config
from dnd_app.request_handler.request import Request
from dnd_app.request_handler.response import Response
from dnd_app.request_handler.exceptions import RequestHandlerException, \
                                               FailedToProcessRequest, \
                                               FailedToValidateRequestedData

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

      except RequestHandlerException:
        logging.critical(
            f"Got exception when trying to handler request. Unable to send requested data.")

###################################################################################################

  def _ProcessNewRequest(self, request: Request) -> Response:
    try:
      response_data = self._ParseJSONMatchingGlob(f"{request.type()}/{request.value()}.json")
      self._MaybeValidateResponseData(response_data, request)

    except Exception as err:
      logging.error(f"Failed to process request: {request.type()}::{request.value()}, "
                    f"{request.id()}. Got exception: {err}")
      raise FailedToProcessRequest

    else:
      return Response(request, response_data)

###################################################################################################

  def _MaybeValidateResponseData(self, response_data: dict, request: Request) -> dict:
    schema = self._GetSchemaForRequestTypeValue(request.type(), request.value())
    try:
      validate(instance=response_data, schema=schema)
    except Exception as err:
      logging.critical(f"Validation failed, got exception:\n{err}")
      raise FailedToValidateRequestedData

###################################################################################################

  def _GetSchemaForRequestTypeValue(self, request_type: str, request_value: str):
    schema_type = request_type
    if request_type == "character":
      schema_type = f"character/{request_value.split('/')[-1]}"
    return self._ParseJSONMatchingGlob(f"schemas/{schema_type}_schema.json")

###################################################################################################

  def _ParseJSONMatchingGlob(self, pattern: str) -> dict:
    data_dir = self._config.get_data_dir()
    found_files = sorted(data_dir.glob(pattern))

    if len(found_files) == 0:
      logging.critical(f"No matching pattern '{pattern}'")
      raise FailedToProcessRequest

    elif len(found_files) > 1:
      logging.warning(f"Found {len(found_files)} matching pattern '{pattern}', using first match")

    with open(found_files[0], 'r') as reader:
      return json.load(reader)


###################################################################################################
###################################################################################################
###################################################################################################
