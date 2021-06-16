###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import re

from kivy.uix.label import Label

###################################################################################################
###################################################################################################
###################################################################################################

def StrFieldToReadable(input: str, title_case: bool=False, strip_end_numbers: bool=True) -> str:
  """Converts string fields like 'dispell_magic' to 'Dispell Magic' or 'Dispell magic'. 
    input: str
      string field to convert
    all_words_upper_case: bool=True
      converts to readable, but all words start with capital letters, otherwise use sentence case
    strip_end_numbers: bool=True
      removes '_[0-9]' from the end of the input, e.g. 'silent_dagger_3' to 'silent_dagger'
  """
  if strip_end_numbers:
    input = re.sub('_[0-9]+$', '', input)
  if title_case:
    return input.replace('_', ' ').capitalize()
  return input.replace('_', ' ').capitalize().title()

###################################################################################################
###################################################################################################
###################################################################################################

def AlignWidgetLabelChildren(widget, halign: str="left", valign: str="middle"):
  """Aligns the text of all Label instaces in a kivy widget with the given halign/ valign."""
  for w in widget.walk():
    if isinstance(w, Label):
      w.halign = halign
      w.valign = valign
      w.text_size = w.size
      w.bind(size=w.setter('text_size'))

###################################################################################################
###################################################################################################
###################################################################################################
