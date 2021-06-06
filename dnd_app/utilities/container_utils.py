###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

def FlattenDict(input: dict, output: dict=None, parent_key: str=None, sep: str="_") -> dict:
  """Flatten a dictionary structure such that the keys are the parent keys concatenated by sep.
      Call using:
        flattened_dict = FlattenDict(input_dict)
          or
        flattened_dict = FlattenDict(input_dict, sep="-")
  """
  if output is None:
    output = {}

  for k, v in input.items():
    new_k = f"{parent_key}{sep}{k}" if parent_key else k
    if isinstance(v, dict):
      FlattenDict(input=v, output=output, parent_key=new_k)
      continue

    output[new_k] = v

  return output

###################################################################################################
###################################################################################################
###################################################################################################

def FlattenList(input: list, output: list=None) -> list:
  """Flatten a list structure recursively."""

  if output is None:
    output = []
  
  if isinstance(input, list):
    for item in input:
      if isinstance(item, list):
        output.extend(FlattenList(item))
      else:
        output.extend([item])
  
  else:
    output.extend(input)

  return output

###################################################################################################
###################################################################################################
###################################################################################################
