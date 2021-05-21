###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import multiprocessing

import time

from dnd_app.data_manager.data_manager import DataManager

###################################################################################################
###################################################################################################
###################################################################################################


class DataManagerInterface:

  def __init__(self, config: dict, request_queue: multiprocessing.Queue,
               response_queue: multiprocessing.Queue) -> None:
    self.config = config
    self.requset_queue = request_queue
    self.response_queue = response_queue

###################################################################################################

  def __call__(self):
    while True:
      requests = []

      # Pull from request queue until empty
      while not self.requset_queue.empty():
        requests.append(self.requset_queue.get())

      # Operate on requests
      for request in requests:
        request['data'] += 2

      time.sleep(0.5)

      # Push to response queue
      for request in requests:
        self.response_queue.put(request)


###################################################################################################
###################################################################################################
###################################################################################################
