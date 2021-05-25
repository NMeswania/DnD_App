###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
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
###################################################################################################
###################################################################################################
