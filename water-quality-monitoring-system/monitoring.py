# monitoring.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button


class MonitoringScreen(Screen):

    def __init__(self, **kwargs):
        super(MonitoringScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        temperature_label = Label(text=f"Temperature: {self.read_temp()} °C", font_size=30, halign='center')
        tds_label = Label(text=f"TDS: {self.read_tds()} ppm", font_size=30, halign='center')
        level_label = Label(text=f"Water Level: {self.read_level()}", font_size=30, halign='center')
        ph_label = Label(text=f"pH: {self.read_ph()}", font_size=30, halign='center')

        logout_button = Button(text="Log Out", size_hint_y=None, height=100)

        # widgets
        layout.add_widget(temperature_label)
        layout.add_widget(tds_label)
        layout.add_widget(level_label)
        layout.add_widget(ph_label)
        layout.add_widget(logout_button)
        self.add_widget(layout)
