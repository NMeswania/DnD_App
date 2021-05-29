###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import uuid

from multiprocessing.connection import Connection

from dnd_app.request_handler.exceptions import RequestResponseIDsNotMatching
from dnd_app.request_handler.response import Response

###################################################################################################
###################################################################################################
###################################################################################################


class Receipt:

  def __init__(self, request_id: uuid.UUID, pipe_connection: Connection):
    self._request_id = request_id
    self._pipe_connection = pipe_connection

###################################################################################################

  def IsResponseReady(self) -> bool:
    return self._pipe_connection.poll()

###################################################################################################

  def GetResponse(self) -> Response:
    response = self._pipe_connection.recv()

    if response.request.id() != str(self._request_id):
      raise RequestResponseIDsNotMatching(response.request.id(), self._request_id)

    self._pipe_connection.close()

    return response


###################################################################################################
###################################################################################################
###################################################################################################
