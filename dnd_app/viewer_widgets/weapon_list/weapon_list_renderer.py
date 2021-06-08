###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from dnd_app.core.config import Config
from dnd_app.utilities.text_utils import StrFieldToReadable, AlignWidgetLabelChildren

###################################################################################################
###################################################################################################
###################################################################################################


class WeaponListRenderer(BoxLayout):

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
    self._weapon_layout.clear_widgets()

###################################################################################################

  def Update(self, data: dict):
    self.Clear()
    for v in data.values():
      for weapon in v:
        if isinstance(weapon, list):
          self._weapon_layout.add_widget(self._AddWeapon(weapon))

###################################################################################################

  def _AddTitle(self) -> Label:
    return Label(text="Weapons", font_size="20sp", size_hint=(1, 0.05))

###################################################################################################

  def _AddContent(self) -> GridLayout:
    table_layout = GridLayout(cols=1, row_default_height=40, padding=5)
    self._weapon_layout = GridLayout(cols=1,
                                     row_force_default=True,
                                     row_default_height=40,
                                     padding=5)

    table_headings_layout = BoxLayout(orientation="horizontal")
    table_headings_layout.add_widget(Label(text="Weapon name", size_hint=(0.3, 1)))
    table_headings_layout.add_widget(Label(text="ATK", size_hint=(0.3, 1)))
    table_headings_layout.add_widget(Label(text="DMG", size_hint=(0.3, 1)))
    AlignWidgetLabelChildren(table_headings_layout)

    table_layout.add_widget(table_headings_layout)
    table_layout.add_widget(self._weapon_layout)
    return table_layout

###################################################################################################

  def _AddWeapon(self, weapon_data: dict) -> BoxLayout:
    layout = BoxLayout(orientation="horizontal")
    layout.add_widget(self._AddWeaponButton(weapon_data[0]))
    layout.add_widget(Label(text=weapon_data[1], size_hint=(0.3, 1)))
    layout.add_widget(Label(text=weapon_data[2], size_hint=(0.3, 1)))
    return layout

###################################################################################################

  def _AddWeaponButton(self, weapon_name: str) -> Button:
    btn = Button(text=StrFieldToReadable(weapon_name),
                 size_hint=(0.3, 1),
                 font_size="13sp",
                 padding=(5, 5))
    AlignWidgetLabelChildren(btn)
    btn.bind(on_press=partial(self._widget.RequestWeaponCallback, weapon_name))    # pylint: disable=no-member
    return btn


###################################################################################################
###################################################################################################
###################################################################################################
