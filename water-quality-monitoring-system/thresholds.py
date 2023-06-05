# thresholds.py
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout


class ThresholdSettingsScreen(Screen, BoxLayout):
    temperature_threshold = NumericProperty(25.0)
    tds_threshold = NumericProperty(500.0)
    level_threshold = NumericProperty(50)
    ph_threshold_min = NumericProperty(6.5)
    ph_threshold_max = NumericProperty(7.5)

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = "threshold_settings"

        self.ids.temp_threshold.bind(text=self.on_temperature_input)
        self.ids.tds_threshold.bind(text=self.on_tds_input)
        self.ids.level_threshold.bind(text=self.on_level_input)
        self.ids.ph_threshold_min.bind(text=self.on_ph_min_input)
        self.ids.ph_threshold_max.bind(text=self.on_ph_max_input)

    def on_temperature_input(self, instance, value):
        try:
            self.temperature_threshold = float(value)
        except ValueError:
            pass

    def on_tds_input(self, instance, value):
        try:
            self.tds_threshold = float(value)
        except ValueError:
            pass

    def on_level_input(self, instance, value):
        try:
            self.level_threshold = int(value)
        except ValueError:
            pass

    def on_ph_min_input(self, instance, value):
        try:
            self.ph_threshold_min = float(value)
        except ValueError:
            pass

    def on_ph_max_input(self, instance, value):
        try:
            self.ph_threshold_max = float(value)
        except ValueError:
            pass

    def save_thresholds(self):

        self.temperature_threshold = float(self.ids.temp_threshold.text)
        self.tds_threshold = float(self.ids.tds_threshold.text)
        self.level_threshold = int(self.ids.level_threshold.text)
        self.ph_threshold_min = float(self.ids.ph_threshold_min.text)
        self.ph_threshold_max = float(self.ids.ph_threshold_max.text)

        self.app.temperature_threshold = self.temperature_threshold
        self.tds_threshold = self.tds_threshold
        self.app.level_threshold = self.level_threshold
        self.app.ph_threshold_min = self.ph_threshold_min
        self.app.ph_threshold_max = self.ph_threshold_max

        self.app.screen_manager.current = "monitoring_screen"
        self.app.show_monitoring_screen()
