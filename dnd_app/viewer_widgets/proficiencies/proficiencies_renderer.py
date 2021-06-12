###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from dnd_app.core.config import Config
from dnd_app.request_handler.response import Response
from dnd_app.utilities.text_utils import StrFieldToReadable, AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class ProficienciesRenderer(BoxLayout):

  def __init__(self, config: Config, widget):
    super().__init__(orientation="vertical")
    self._dnd_config = config
    self._widget = widget
    self.add_widget(self._AddTitle())
    self.add_widget(self._AddContent())

###################################################################################################

  def Terminate(self):
    self._widget = None

###################################################################################################

  def Clear(self):
    self._main_layout.clear_widgets()

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    for k, v in data.items():
      if isinstance(v, list) and len(v) > 0:
        self._main_layout.add_widget(self._AddProficiencyGroup(k, v))

###################################################################################################

  def _AddTitle(self) -> Label:
    return Label(text="Proficiencies", font_size="20sp", size_hint=(1, 0.05))

###################################################################################################

  def _AddContent(self) -> BoxLayout:
    self._main_layout = BoxLayout(orientation="horizontal")
    return self._main_layout

###################################################################################################

  def _AddProficiencyGroup(self, group_name: str, group_content: list) -> GridLayout:
    n_rows = len(group_content) + 1
    layout = GridLayout(cols=1,
                        rows=n_rows,
                        row_default_height=40,
                        row_force_default=True,
                        padding=5)
    layout.add_widget(Label(text=StrFieldToReadable(group_name), font_size="15sp", bold=True))
    for item in group_content:
      layout.add_widget(Label(text=StrFieldToReadable(item), font_size="13sp"))
    layout.id = group_name
    AlignWidgetLabelChildren(layout)
    return layout

###################################################################################################
###################################################################################################
###################################################################################################
