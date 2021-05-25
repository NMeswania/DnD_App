###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

###################################################################################################
###################################################################################################
###################################################################################################

class SpellTag(BoxLayout):

  def __init__(self, key: str):
    super().__init__(orientation="horizontal")
    self._key = Label(text=key, size_hint=(0.3, 1))
    self._value = Label(text="", size_hint=(0.7, 1))
    self.add_widget(self._key)
    self.add_widget(self._value)

###################################################################################################

  def Update(self, value: str):
    self._value.text = value

###################################################################################################

  def Clear(self):
    self._value.text = ""


###################################################################################################
###################################################################################################
###################################################################################################

class SpellRenderer(BoxLayout):

  def __init__(self):
    super().__init__(orientation="vertical")
    spell_tag_names = ["Name", "Range", "Casting time", "Components", "Duration"]
    self._spell_tags = {}
    for name in spell_tag_names:
      self._spell_tags[name] = SpellTag(name)
      self.add_widget(self._spell_tags[name])

###################################################################################################

  def Update(self, new_data: dict):
    data = self._TransformNewDataLabels(new_data)
    if self._ValidateNewData(data):
      for k, v in data.items():
        self._spell_tags[k].Update(v)

###################################################################################################

  def Clear(self):
    for v in self._spell_tags.values():
      v.Clear()

###################################################################################################

  def _TransformNewDataLabels(self, new_data: dict) -> dict:
    data = {}
    for k in new_data.keys():
      new_key = k.replace('_', ' ').capitalize()
      data[new_key] = new_data[k]
    return data

###################################################################################################

  def _ValidateNewData(self, new_data: dict):
    n_same_keys = len(set(new_data.keys()).intersection(set(self._spell_tags.keys())))
    expected_same_keys = len(self._spell_tags.keys())
    if expected_same_keys != n_same_keys:
      logging.critical(
          f"New data mismatch:\n\tNew keys = {new_data.keys()}"
          f"\n\tExpected: {self._spell_tags.keys()}"
          f"\n\tMismatch: {set(new_data.keys()).difference(set(self._spell_tags.keys()))}")
      return False
    return True


###################################################################################################
###################################################################################################
###################################################################################################
