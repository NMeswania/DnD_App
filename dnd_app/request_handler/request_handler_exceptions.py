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
    self.type = request_type
    self.message = "Unknown request type."
    super().__init__(self.message)

  def __str__(self):
    return f"{self.message} Type: {self.type}"

###################################################################################################

class FailedToProcessRequest(RequestHandlerException):
  """ Generic unable to process request exception. """
  pass

###################################################################################################
###################################################################################################
###################################################################################################
