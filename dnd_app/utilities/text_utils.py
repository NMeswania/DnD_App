###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.uix.label import Label

###################################################################################################
###################################################################################################
###################################################################################################

def StrFieldToReadable(input: str, title_case: bool=False) -> str:
  """Converts string fields like 'dispell_magic' to 'Dispell Magic' or 'Dispell magic'
    input: str
      string field to convert
    all_words_upper_case: bool=True
      converts to readable, but all words start with capital letters, otherwise use sentence case
  """
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
      w.text_size = w.size
      w.halign = halign
      w.valign = valign

###################################################################################################
###################################################################################################
###################################################################################################
