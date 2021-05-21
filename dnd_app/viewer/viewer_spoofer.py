###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import multiprocessing

import time

###################################################################################################
###################################################################################################
###################################################################################################


class ViewerSpoofer:

  def __init__(self, request_queue: multiprocessing.Queue,
               response_queue: multiprocessing.Queue) -> None:
    self.request_queue = request_queue
    self.response_queue = response_queue

###################################################################################################

  def __call__(self):
    while True:
      requests = []
      for i in range(0, 4):
        new_data = 3 + i * 2
        requests.append({"ID": i, "data": new_data})

      for request in requests:
        self.request_queue.put(request)

      time.sleep(0.3)

      responses = []
      while not self.response_queue.empty():
        responses.append(self.response_queue.get())

      print([response for response in responses])


###################################################################################################
###################################################################################################
###################################################################################################
