###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from dnd_app.core.config import Config
from dnd_app.request_handler.response import Response
from dnd_app.utilities.container_utils import FlattenDict
from dnd_app.utilities.text_utils import StrFieldToReadable, AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class AbilityScoresRenderer(BoxLayout):

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
    self.add_widget(self._AddTitle())
    self.add_widget(self._AddInspirationAndProficiencyBonus())
    main_layout = BoxLayout(orientation="horizontal")
    main_layout.add_widget(self._AddAbilityScores())
    main_layout.add_widget(self._AddSaves())
    main_layout.add_widget(self._AddSkills())
    self.add_widget(main_layout)

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    for widget in self.walk():
      if hasattr(widget, "id"):
        if isinstance(widget, Label):
          widget.text = ""
        elif isinstance(widget, CheckBox):
          widget.active = False

###################################################################################################

  def DisplayResponse(self, response: Response):
    self.Update(response.data())

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    flattened_data = FlattenDict(data)
    for k, v in flattened_data.items():
      for child in self.walk():
        if hasattr(child, "id") and child.id == k:
          if isinstance(child, Label):
            logging.debug(f"Set key {k} with value {v}")
            child.text = str(v)
          elif isinstance(child, CheckBox):
            logging.debug(f"Set key {k} with value {v}")
            child.active = v

###################################################################################################

  def _AddTitle(self) -> Label:
    return Label(text="Ability Scores & Skills", font_size="20sp", size_hint=(1, 0.05))

###################################################################################################

  def _AddInspirationAndProficiencyBonus(self) -> BoxLayout:
    layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))
    checkbox = CheckBox(active=False, size_hint=(0.1, 1))
    checkbox.id = "inspiration"

    proficiency_bonus_modifer_label = Label(text="", size_hint=(0.2, 1), font_size="20sp")
    proficiency_bonus_modifer_label.id = "proficiency_bonus"
    AlignWidgetLabelChildren(proficiency_bonus_modifer_label, valign="center")

    layout.add_widget(checkbox)
    layout.add_widget(Label(text="Inspiration", size_hint=(0.4, 1), font_size="18sp"))
    layout.add_widget(proficiency_bonus_modifer_label)
    layout.add_widget(Label(text="Proficiency Bonus", size_hint=(0.3, 1), font_size="18sp"))

    return layout

###################################################################################################

  def _AddAbilityScores(self) -> BoxLayout:
    layout = BoxLayout(orientation="vertical")
    layout.add_widget(Label(text="Ability Scores", size_hint=(1, 0.05), font_size="15sp"))
    grid_layout = GridLayout(rows=len(self._ability_score_names()),
                             cols=1,
                             col_default_width=50,
                             row_default_height=35,
                             row_force_default=True)

    for ability_score in self._ability_score_names():
      grid_layout.add_widget(self._AddAbilityScore(ability_score))

    layout.add_widget(grid_layout)

    return layout

###################################################################################################

  def _AddAbilityScore(self, ability_score) -> BoxLayout:
    layout = BoxLayout(orientation="vertical")
    layout.add_widget(
        Label(text=StrFieldToReadable(ability_score), size_hint=(1, 0.1), font_size="12sp"))

    modifier = Label(text="", size_hint=(1, 0.6), font_size="18sp")
    modifier.id = f"ability_scores_{ability_score}_modifier"

    base_number = Label(text="", size_hint=(1, 0.3), font_size="12sp")
    base_number.id = f"ability_scores_{ability_score}_base_number"

    layout.add_widget(modifier)
    layout.add_widget(base_number)

    return layout

###################################################################################################

  def _AddSaves(self) -> BoxLayout:
    layout = BoxLayout(orientation="vertical")
    layout.add_widget(Label(text="Saving Throws", size_hint=(1, 0.05), font_size="15sp"))
    grid_layout = GridLayout(rows=len(self._ability_score_names()),
                             cols=1,
                             col_default_width=50,
                             row_default_height=35,
                             row_force_default=True)

    for ability_score in self._ability_score_names():
      grid_layout.add_widget(self._AddSkillSave(ability_score, "saving_throws"))

    layout.add_widget(grid_layout)

    return layout

###################################################################################################

  def _AddSkills(self) -> BoxLayout:
    layout = BoxLayout(orientation="vertical")
    layout.add_widget(Label(text="Skills", size_hint=(1, 0.05), font_size="15sp"))
    grid_layout = GridLayout(rows=len(self._skill_names()), cols=1, col_default_width=50)

    for skill in self._skill_names():
      grid_layout.add_widget(self._AddSkillSave(skill, "skills"))

    layout.add_widget(grid_layout)

    return layout

###################################################################################################

  def _AddSkillSave(self, skill_save_name: str, id_prefix: str) -> BoxLayout:
    layout = BoxLayout(orientation="horizontal")

    proficiency_box = CheckBox(active=False, size_hint=(0.1, 1))
    proficiency_box.id = f"{id_prefix}_{skill_save_name}_proficiency"

    modifier = Label(text="", size_hint=(0.2, 1), font_size="13sp")
    modifier.id = f"{id_prefix}_{skill_save_name}_modifier"

    label = Label(text=StrFieldToReadable(skill_save_name), size_hint=(0.7, 1), font_size="12sp")
    AlignWidgetLabelChildren(label)

    layout.add_widget(proficiency_box)
    layout.add_widget(modifier)
    layout.add_widget(label)

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
