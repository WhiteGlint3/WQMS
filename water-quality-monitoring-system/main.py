import random
import sqlite3
import time
import smtplib
from email.mime.text import MIMEText
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from kivy.core.window import Window

Builder.load_file('templates/label_color.kv')
# uses the create kv styles file
Builder.load_file('templates/create_user.kv')
Builder.load_file('templates/threshold.kv')


# Builder.load_file('background.kv')


# define a custom label class that updates its text when called
class UpdatingLabel(Label):
    def init(self, kwargs):
        super().init(kwargs)
        self.update()

    def update(self):
        self.text = self.get_text()

    def get_text(self):
        # this method should be implemented by a subclass
        return "N/A"


# subclass UpdatingLabel to create a label that displays temperature
class TemperatureLabel(UpdatingLabel):

    def get_text(self):
        return f"Temperature: {self.app.read_temp()} °C"


# subclass UpdatingLabel to create a label that displays water level
class LevelLabel(UpdatingLabel):

    def get_text(self):
        return f"Level: {self.app.read_level()}"


# subclass UpdatingLabel to create a label that displays pH level
class PhLabel(UpdatingLabel):

    def get_text(self):
        return f"pH: {self.app.read_ph()}"


class Tds(UpdatingLabel):

    def get_text(self):
        return f"TDS:{self.app.read_tds()}"


# define the main app class
def get_latest_sensor_values():
    try:
        with sqlite3.connect('data/sensors.db') as conn:
            c = conn.cursor()
            c.execute("SELECT temperature, tds, level, ph FROM sensor_readings ORDER BY timestamp DESC LIMIT 1")
            result = c.fetchone()
            return {"temperature": result[0], "tds": result[1], "level": result[2], "ph": result[3]} if result else None
    except Exception as e:
        print(f"Error getting latest sensor values: {e}")
        return None


def get_thresholds(username):
    try:
        with sqlite3.connect('data/login.db') as conn:
            c = conn.cursor()
            c.execute("SELECT temperature_threshold, tds_threshold, level_threshold, ph_threshold FROM users WHERE "
                      "username=?", (username,))
            result = c.fetchone()
            return {"temperature_threshold": result[0], "tds_threshold": result[1], "level_threshold": result[2],
                    "ph_threshold": result[3]} if result else None
    except Exception as e:
        print(f"Error getting thresholds for user {username}: {e}")
        return None


def get_user_email(username):
    try:
        with sqlite3.connect('data/login.db') as conn:
            c = conn.cursor()
            c.execute("SELECT email FROM users WHERE username=?", (username,))
            result = c.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(F"Error getting email for user {username}: {e}")
        return None


def send_email_notification(subject, message, wqms_email, recipient_email, sender_password):
    msg = MIMEText(message)

    msg['Subject'] = subject
    msg['From'] = wqms_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(wqms_email, sender_password)
            server.send_message(msg)
            server.quit()
            print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", e)


class WaterMonitoringApp(App):

    # define functions to read temperature and water level
    def __init__(self, **kwargs):
        super().__init__()
        self.current_user = None

    @staticmethod
    def read_temp():
        # replace this with actual code to read temperature
        return round(random.uniform(20, 30), 2)

    @staticmethod
    def read_level():
        # replace this with actual code to read water level
        return random.randint(0, 100)

    @staticmethod
    def read_ph():
        # replace this with actual code to read ph level
        return round(random.uniform(6.0, 8.0), 2)

    @staticmethod
    def read_tds():
        # replace this with actual code to read ph level
        return round(random.uniform(0, 1000))

    # connect to the database and create a table for sensor readings
    with sqlite3.connect('data/sensors.db') as conn:
        c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_readings
                                          (timestamp REAL, temperature REAL, TDS REAL, level INT, ph REAL)''')
    conn.commit()

    # connect to the database and create user credentials
    with sqlite3.connect('data/login.db') as conn:
        c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                      (username TEXT PRIMARY KEY, password TEXT, email TEXT, phone TEXT,
               temperature_threshold REAL, tds_threshold REAL, level_threshold REAL, ph_threshold REAL)''')
    conn.commit()

    # create a box layout to hold the labels and login widgets
    def build(self):
        layout = self.go_to_login_screen()
        Window.clearcolor = (1,1,1,1)
        return layout

    def check_and_send_notifications(self):
        # Get user thresholds
        # Idea try using the current_settings instead of user_threshold since this method is in the class now
        user_thresholds = get_thresholds(self.current_user)
        if user_thresholds is None:
            print("User thresholds not found.")
            return

        # Get latest sensor values
        sensor_values = get_latest_sensor_values()
        if sensor_values is None:
            print("Sensor values not found.")
            return

        # Prepare for sending notifications
        recipient_email = get_user_email(self.current_user)
        if recipient_email is None:
            print("User email not found.")
            return

        messages = []
        print(user_thresholds)
        # check sensor values against user threshold settings
        if sensor_values['temperature'] > user_thresholds['temperature_threshold']:
            messages.append('Temperature has reached the threshold.')
            pass

        if sensor_values['tds'] > user_thresholds['tds_threshold']:
            messages.append('TDS has reached the threshold.')
            pass

        if sensor_values['level'] > user_thresholds['level_threshold']:
            messages.append('Water level has reached the threshold.')
            pass

        if sensor_values['ph'] > user_thresholds['ph_threshold']:
            messages.append('pH has reached the threshold.')
            pass

        if messages:
            print(f"Thresholds reached for user {self.current_user}. Sending email notification...")
            wqms_email = ''
            sender_password = ''
            send_email_notification('Sensor Alert', '\n'.join(messages), wqms_email, recipient_email,
                                    sender_password)

    # adds new user and stores to database
    def add_new_user(self, username, password, email, phone):
        self.c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = self.c.fetchone()
        if user:
            return "Username already exists."
        else:  # Changed (?, ?, ?, ?, NULL, NULL, NULL, NULL) to (?, ?, ?, ?, REAL, REAL, REAL, REAL)
            self.c.execute("INSERT INTO users VALUES (?, ?, ?, ?, NULL, NULL, NULL, NULL)", (username, password, email,
                                                                                             phone))
            self.conn.commit()
            return "User created successfully."

    # Screen for making a new login
    def show_create_user_screen(self):
        create_user_layout = BoxLayout(orientation='vertical')
        create_user_label = Label(text="Please enter a new username and password", font_size=24, halign='center')
        new_username_input = TextInput(multiline=False, hint_text="New Username",
                                       size_hint_x=0.45,
                                       size_hint_y=0.15,
                                       pos_hint={'center_x': 0.5})
        new_password_input = TextInput(multiline=False, password=True, hint_text="New Password",
                                       size_hint_x=0.45,
                                       size_hint_y=0.15,
                                       pos_hint={'center_x': 0.5})
        new_email_input = TextInput(multiline=False, hint_text="Email",
                                    size_hint_x=0.45,
                                    size_hint_y=0.15,
                                    pos_hint={'center_x': 0.5})
        new_phone_input = TextInput(multiline=False, hint_text="Phone Number",
                                    size_hint_x=0.45,
                                    size_hint_y=0.15,
                                    pos_hint={'center_x': 0.5})

        confirm_button = Button(text="Confirm", size_hint_x=0.45, size_hint_y=0.15, pos_hint={'center_x': 0.5})
        confirm_button.bind(
            on_press=lambda instance: self.confirm_create_user(instance, create_user_label, new_username_input,
                                                               new_password_input, new_email_input,
                                                               new_phone_input, create_user_layout))
        back_button = Button(text="Back", size_hint_x=0.45, size_hint_y=0.15, pos_hint={'center_x': 0.5})
        back_button.bind(on_press=lambda instance: self.go_to_login_screen_from_create_user())

        create_user_layout.add_widget(create_user_label)
        create_user_layout.add_widget(new_username_input)
        create_user_layout.add_widget(new_password_input)
        create_user_layout.add_widget(new_email_input)
        create_user_layout.add_widget(new_phone_input)
        create_user_layout.add_widget(confirm_button)
        create_user_layout.add_widget(back_button)
        self.root.clear_widgets()
        self.root.add_widget(create_user_layout)

    def create_user_callback(self):
        # Add code to create a new user here
        self.show_create_user_screen()
        print("Creating a new user...")
        pass

    def confirm_create_user(self, instance, create_user_label, new_username_input, new_password_input,
                            new_email_input, new_phone_input, create_user_layout):
        result = self.add_new_user(new_username_input.text, new_password_input.text,
                                   new_email_input.text, new_phone_input.text)
        create_user_label.text = result
        new_username_input.text = ""
        new_password_input.text = ""
        new_email_input.text = ""
        new_phone_input.text = ""

    def go_to_login_screen_from_create_user(self):
        self.root.clear_widgets()
        login_layout = self.go_to_login_screen()
        self.root.add_widget(login_layout)

    def go_to_login_screen(self):
        # create a new layout containing the login widgets
        login_layout = BoxLayout(orientation='vertical')
        login_label = Label(text="Please enter your username and password", font_size=24, halign='center')
        username_input = TextInput(multiline=False, hint_text="Username",
                                   size_hint_x=0.45,
                                   size_hint_y=0.15,
                                   pos_hint={'center_x': 0.5})

        password_input = TextInput(multiline=False, password=True, hint_text="Password",
                                   size_hint_x=0.45,
                                   size_hint_y=0.15,
                                   pos_hint={'center_x': 0.5})
        login_button = Button(text="Login", size_hint_x=0.45, size_hint_y=0.15, pos_hint={'center_x': 0.5})
        login_button.bind(
            on_press=lambda instance: self.login_callback(instance, login_label, username_input, password_input,
                                                          login_layout))

        # bind the on_text_validate event of the password input to the login_callback function
        password_input.bind(
            on_text_validate=lambda instance: self.login_callback(login_button, login_label, username_input,
                                                                  password_input, login_layout))
        # create new button for creating a new user
        create_user_button = Button(text="Create User", size_hint_x=0.45, size_hint_y=0.15, pos_hint={'center_x': 0.5})
        create_user_button.bind(on_press=lambda instance: self.create_user_callback())

        # Set focus to username input
        username_input.focus = True
        # Bind tab key to switch focus between inputs
        username_input.bind(on_text_validate=lambda x: password_input.focus if password_input else None)

        login_layout.add_widget(login_label)
        login_layout.add_widget(username_input)
        login_layout.add_widget(password_input)
        login_layout.add_widget(login_button)
        login_layout.add_widget(create_user_button)
        return login_layout

    def login_callback(self, instance, login_label, username_input, password_input, login_layout):
        with sqlite3.connect('data/login.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username_input.text, password_input.text))
            user = c.fetchone()

        if user:
            # checks for individual user set data in the thresholds settings
            self.current_user = username_input.text
            self.root.clear_widgets()
            self.show_monitoring_screen()
        else:
            login_label.text = "Invalid username or password"
            username_input.text = ""
            password_input.text = ""

    # Saves threshold setting to the login database
    def save_thresholds(self, temperature, tds, level, ph, confirmation_label, callback=None):
        # Prevents user from deleting current settings on an empty field
        if not temperature or not tds or not level or not ph:
            confirmation_label.text = "Please enter values for all fields"
            confirmation_label.color = [1, 0, 0, 1]
            return

            # Setting default values here to debug email notification REMOVE AFTER FIX
       # temperature = temperature if temperature else 0.0
       # tds = tds if tds else 0.0
       # level = level if level else 0.0
       # ph = ph if ph else 0.0

        with sqlite3.connect('data/login.db') as conn:
            c = conn.cursor()
            c.execute('''UPDATE users
                         SET temperature_threshold=?, tds_threshold=?, level_threshold=?, ph_threshold=?
                         WHERE username=?''', (temperature, tds, level, ph, self.current_user))
            conn.commit()
            confirmation_label.text = 'Settings Saved.'
            # Print out debug information
        print(f'Saved thresholds for {self.current_user}: temperature={temperature}, tds={tds}, level={level}, ph={ph}')

        if callback:
            callback()

    # retrieve user settings

    def show_threshold_screen(self):
        # Create layout
        layout = BoxLayout(orientation='vertical')
        confirmation_label = Label(text='', font_size=20, halign='center', color=[0, 1, 0, 1])  # Green color
        # Retrieve settings
        current_settings = get_thresholds(self.current_user)

        if current_settings is None:
            current_settings = ('N/A', 'N/A', 'N/A', 'N/A')

        # Create input fields
        temperature_input = TextInput(hint_text='Temperature threshold (°C)', input_type='number')
        tds_input = TextInput(hint_text='TDS threshold (ppm)', input_type='number')
        level_input = TextInput(hint_text='Water level threshold', input_type='number')
        ph_input = TextInput(hint_text='pH threshold', input_type='number')

        # Displays current settings
        # debug at print(current_settings) REMOVE WHEN FIXED
        print(current_settings)
        temperature_label = Label(text=f"Current setting: {current_settings['temperature_threshold']} °C", font_size=20, halign='left')
        tds_label = Label(text=f"Current setting: {current_settings['tds_threshold']} ppm", font_size=20, halign='left')
        level_label = Label(text=f"Current setting: {current_settings['level_threshold']} Water Level", font_size=20, halign='left')
        ph_label = Label(text=f"Current setting: {current_settings['ph_threshold']} pH", font_size=20, halign='left')

        # Create submit and cancel buttons
        submit_button = Button(text='Submit', size_hint_y=None, height=100)
        cancel_button = Button(text='Cancel', size_hint_y=None, height=100)

        # Bind button press events
        submit_button.bind(
            on_press=lambda instance: self.save_thresholds(temperature_input.text, tds_input.text, level_input.text,
                                                           ph_input.text, confirmation_label,
                                                           callback=lambda: self.show_threshold_screen()))
        cancel_button.bind(on_press=lambda instance: self.go_to_monitoring_screen_from_threshold())

        # Add input fields and buttons to layout
        layout.add_widget(Label(text='Enter your thresholds:', font_size=30, halign='center'))
        layout.add_widget(temperature_input)
        layout.add_widget(temperature_label)
        layout.add_widget(tds_input)
        layout.add_widget(tds_label)
        layout.add_widget(level_input)
        layout.add_widget(level_label)
        layout.add_widget(ph_input)
        layout.add_widget(ph_label)
        layout.add_widget(submit_button)
        layout.add_widget(cancel_button)
        layout.add_widget(confirmation_label)

        # Clear existing widgets and add the new layout to the root
        self.root.clear_widgets()
        self.root.add_widget(layout)

    def show_monitoring_screen(self):
        layout = BoxLayout(orientation='vertical')

        temperature_label = Label(text=f"Temperature: {self.read_temp()} °C", font_size=30, halign='center')
        tds_label = Label(text=f"TDS: {self.read_tds()} ppm", font_size=30, halign='center')
        level_label = Label(text=f"Water Level: {self.read_level()}", font_size=30, halign='center')
        ph_label = Label(text=f"pH: {self.read_ph()}", font_size=30, halign='center')

        threshold_button = Button(text="User Threshold's", size_hint_y=None, height=100)
        threshold_button.bind(on_press=lambda instance: self.go_to_threshold_screen_from_monitoring())
        logout_button = Button(text="Log Out", size_hint_y=None, height=100)
        logout_button.bind(on_press=lambda instance: self.go_to_login_screen_from_monitoring())

        # Add the labels and the logout button to the layout
        layout.add_widget(temperature_label)
        layout.add_widget(tds_label)
        layout.add_widget(level_label)
        layout.add_widget(ph_label)
        layout.add_widget(threshold_button)
        layout.add_widget(logout_button)

        # Clear existing widgets and add the new layout to the root
        self.root.clear_widgets()
        self.root.add_widget(layout)

        # Schedule updates for the labels every second
        Clock.schedule_interval(lambda dt: self.update_labels(temperature_label, level_label, ph_label), 1)

        # Schedule check_and_send_notifications every 60 seconds
        Clock.schedule_interval(lambda dt: self.check_and_send_notifications(), 30)

        # Schedule updates for the labels every second
        def update_labels(dt):
            temperature = self.read_temp()
            level = self.read_level()
            ph = self.read_ph()
            tds = self.read_tds()
            temperature_label.text = f"Temperature: {temperature:.2f} °C"
            level_label.text = f"Water Level: {level:.2f}"
            ph_label.text = f"pH: {ph:.2f}"
            tds_label.text = f"TDS: {tds:.2f}"

            # Error with sending email starts from here
            with sqlite3.connect('data/sensors.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO sensor_readings VALUES (?, ?, ?, ?, ?)", (time.time(), temperature, tds, level,
                                                                                 ph))
                conn.commit()

            with open('data/sensors_log.txt', 'a') as f:
                f.write(f"{time.time()}, {temperature:.2f}, {level:.2f}, {ph:.2f}\n")

        Clock.schedule_interval(update_labels, 1)

    def go_to_login_screen_from_monitoring(self):
        self.root.clear_widgets()
        login_layout = self.go_to_login_screen()
        self.root.add_widget(login_layout)

    def go_to_threshold_screen_from_monitoring(self):
        self.show_threshold_screen()
        # self.root.clear_widgets()
        # login_layout = self.go_to_login_screen()
        # self.root.add_widget(login_layout)

    def update_labels(self, temperature_label, level_label, ph_label):
        pass

    def go_to_monitoring_screen_from_threshold(self):
        self.show_monitoring_screen()
        pass

    def fetch_user_thresholds(self):
        with sqlite3.connect('data/login.db') as conn:
            c = conn.cursor()
            c.execute('''SELECT temperature_threshold, tds_threshold, level_threshold, ph_threshold 
                         FROM users
                         WHERE username=?''', (self.current_user,))
            thresholds = c.fetchone()
            user_thresholds = {
                'temperature': thresholds[0],
                'tds': thresholds[1],
                'level': thresholds[2],
                'ph': thresholds[3]
            }
            return user_thresholds


# run the app
if __name__ == '__main__':
    WaterMonitoringApp().run()
