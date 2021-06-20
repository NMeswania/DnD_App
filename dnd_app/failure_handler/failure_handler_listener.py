###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
import queue

from multiprocessing import Queue

from dnd_app.core.config import Config
from dnd_app.failure_handler.failure_renderer import FailureRenderer

###################################################################################################
###################################################################################################
###################################################################################################


class FailureHandlerListener():

  def __init__(self, config: Config, recv_queue: Queue):
    self._dnd_config = config
    self._recv_queue = recv_queue

###################################################################################################

  def __del__(self):
    self._recv_queue.close()
    del self._renderer

###################################################################################################

  def LoadRenderer(self):
    self._BuildRenderers()

###################################################################################################

  def CheckForUpdates(self):
    try:
      data = self._recv_queue.get_nowait()
      self._renderer.Update(data)

    except queue.Empty:
      pass
    
    except:
      logging.critical("Could not update renderer")

###################################################################################################

  def _BuildRenderers(self) -> FailureRenderer:
    self._renderer = FailureRenderer()


###################################################################################################
###################################################################################################
###################################################################################################
