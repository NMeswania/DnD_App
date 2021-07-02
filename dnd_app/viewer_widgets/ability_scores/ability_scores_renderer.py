###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.properties import ObjectProperty    #pylint: disable=no-name-in-module
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label

from dnd_app.core.config import Config
from dnd_app.utilities.text_utils import StrFieldToReadable

###################################################################################################
###################################################################################################
###################################################################################################


class AbilityScoresRenderer(BoxLayout):

  ids = {}
  ids['inspiration'] = ObjectProperty("")
  ids['proficiency_bonus'] = ObjectProperty("")
  ids['ability_scores'] = ObjectProperty("")
  ids['saving_throws'] = ObjectProperty("")
  ids['skills'] = ObjectProperty("")

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
    self._AddAbilityScores()
    self._AddSaves()
    self._AddSkills()

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    for value in self.ids.values():
      self._ClearInternal(value)

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    for k, v in data.items():
      if k in self.ids.keys():
        self._UpdateInternal(self.ids[k], v)

###################################################################################################

  def _ClearInternal(self, value):
    if isinstance(value, Label):
      value.text = ""
    elif isinstance(value, CheckBox):
      value.active = False
    elif hasattr(value, "children") and len(value.children) > 0:
      for child in value.children:
        for nested_value in child.ids:
          self._ClearInternal(nested_value)

###################################################################################################

  def _UpdateInternal(self, value, update_value):
    if isinstance(value, Label):
      value.text = str(update_value)
    elif isinstance(value, CheckBox):
      value.active = update_value
    elif hasattr(value, "children") and len(value.children) > 0:
      for k, v in update_value.items():
        for child in value.children:
          if k == child.ids['name']:
            for k_, v_ in v.items():
              if k_ in child.ids:
                self._UpdateInternal(child.ids[k_], v_)
            break

###################################################################################################

  def _AddAbilityScores(self):
    for ability_score in self._ability_score_names():
      self.ids['ability_scores'].add_widget(self._AddAbilityScore(ability_score))

###################################################################################################

  def _AddAbilityScore(self, ability_score: str):
    layout = Factory.AbilityScoresRendererAbilityScore()
    layout.ids['name'] = ability_score
    layout.ids['label'].text = StrFieldToReadable(ability_score)
    return layout

###################################################################################################

  def _AddSaves(self):
    for ability_score in self._ability_score_names():
      self.ids['saving_throws'].add_widget(self._AddSave(ability_score))

###################################################################################################

  def _AddSave(self, save: str):
    layout = Factory.AbilityScoresRendererSkillSave()
    layout.ids['name'] = save
    layout.ids['label'].text = StrFieldToReadable(save)
    return layout

###################################################################################################

  def _AddSkills(self):
    for skill in self._skill_names():
      self.ids['skills'].add_widget(self._AddSkill(skill))

###################################################################################################

  def _AddSkill(self, skill):
    layout = Factory.AbilityScoresRendererSkillSave()
    layout.ids['name'] = skill
    layout.ids['label'].text = StrFieldToReadable(skill)
    return layout

###################################################################################################

  def _ability_score_names(self) -> list:
    return ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]

###################################################################################################

  def _skill_names(self) -> list:
    return [
        "acrobatics", "animal_handling", "arcana", "athletics", "deception", "history", "insight",
        "intimidation", "investigation", "medicine", "nature", "perception", "performance",
        "persuasion", "religion", "slight_of_hand", "stealth", "survival"
    ]


###################################################################################################
###################################################################################################
###################################################################################################
