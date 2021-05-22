###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from multiprocessing import Queue

import time

from dnd_app.core.request import Request

###################################################################################################
###################################################################################################
###################################################################################################


class ViewerSpoofer:

  def __init__(self, request_queue: Queue, response_queue: Queue) -> None:
    self.request_queue = request_queue
    self.response_queue = response_queue

###################################################################################################

  def run(self):
    while True:
      requests = [
        Request(type="spell", value="Fireball"),
        Request(type="item", value="Ring of Protection"),
        Request(type="feat", value="Pole-arm Master"),
        Request(type="spell", value="Shatter")
      ]

      for request in requests:
        self.request_queue.put(request)

      time.sleep(0.3)

      responses = []
      while not self.response_queue.empty():
        responses.append(self.response_queue.get())

      print("got responses: ")
      for response in responses:
        print(response)


###################################################################################################
###################################################################################################
###################################################################################################
