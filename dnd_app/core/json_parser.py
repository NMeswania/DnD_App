###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import json
import jsonschema

###################################################################################################
###################################################################################################
###################################################################################################

class JSONParser:

  def __init__(self, file):
    self.file = file

###################################################################################################
  
  def ParseData(self) -> dict:
    with open(self.file, 'r') as reader:
      return json.load(reader)

###################################################################################################
###################################################################################################
###################################################################################################