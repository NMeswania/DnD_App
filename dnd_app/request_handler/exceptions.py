###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import uuid

###################################################################################################
###################################################################################################
###################################################################################################


class RequestResponseIDsNotMatching(Exception):

  def __init__(self, request_id: uuid.UUID, repsonse_id: uuid.UUID):
    self._message = f"Request ID: {str(request_id)}, Response ID: {str(repsonse_id)}"
    super().__init__(self._message)

  def __str__(self):
    return self._message

###################################################################################################

class RequestHandlerException(Exception):
  """ Base class exceptions for the RequestHandler class. """
  pass

###################################################################################################

class UnknownRequestType(RequestHandlerException):
  """ When the type of request is unknown. """
  def __init__(self, request_type: str):
    self._type = request_type
    self._message = "Unknown request type."
    super().__init__(self._message)

  def __str__(self):
    return f"{self._message} Type: {self._type}"

###################################################################################################

class FailedToProcessRequest(RequestHandlerException):
  """ Generic unable to process request exception. """
  pass

###################################################################################################

class FailedToValidateRequestedData(RequestHandlerException):
  """ jsonschema validation failed """
  pass

###################################################################################################
###################################################################################################
###################################################################################################
