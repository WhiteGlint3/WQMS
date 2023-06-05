from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class new_user(Screen):

    def __init__(self, **kwargs):
        super(new_user, self).__init__(**kwargs)

        # Create box layout
        layout = BoxLayout(orientation='vertical')

        # Create labels and text inputs for user information
        name_label = Label(text='Name:')
        self.name_input = TextInput(multiline=False)

        password_label = Label(text='Password:')
        self.password_input = TextInput(multiline=False, password=True)

        email_label = Label(text='Email Address:')
        self.email_input = TextInput(multiline=False)

        cellphone_label = Label(text='Cellphone Number:')
        self.cellphone_input = TextInput(multiline=False)

        # Create submit button
        submit_button = Button(text='Submit', size_hint_y=None, height=100)
        submit_button.bind(on_press=self.submit)

        # Add widgets to layout
        layout.add_widget(name_label)
        layout.add_widget(self.name_input)
        layout.add_widget(password_label)
        layout.add_widget(self.password_input)
        layout.add_widget(email_label)
        layout.add_widget(self.email_input)
        layout.add_widget(cellphone_label)
        layout.add_widget(self.cellphone_input)
        layout.add_widget(submit_button)

        # Add layout to screen
        self.add_widget(layout)

    def submit(self, instance):
        # Get user information from text inputs
        name = self.name_input.text
        password = self.password_input.text
        email = self.email_input.text
        cellphone = self.cellphone_input.text