###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import signal
import sys

###################################################################################################
###################################################################################################
###################################################################################################


class SignalHandler:

  def __init__(self, main_task):
    self.main_task = main_task

###################################################################################################

  def assign(self):
    signal.signal(signal.SIGINT, self.handle_signal)

###################################################################################################

  def handle_signal(self, sig, frame):
    del self.main_task
    sys.exit(0)


###################################################################################################
###################################################################################################
###################################################################################################