import kivy.uix.button as kb
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.pagelayout import PageLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from Project import Main
from kivy.clock import Clock
from functools import partial
from kivy.uix.popup import Popup


Builder.load_file('graphics.kv')


class Graphics(Screen):
    pass


class Loading(Screen):

    def start_program(self, police, view):
        # Fingerprint all the mp3's in the directory we give it
        police.fingerprint_directory("Audio_files", [".mp3"])
        App.get_running_app().view = False


class Working(Screen):
    sound_text = StringProperty()

    def run_program(self, police, view):
        if not view:
            police.recognize()
            App.get_running_app().sound = police.sound
            self.sound_text = App.get_running_app().sound

    def change_text(self):
        App.get_running_app().counter += 1
        if (not App.get_running_app().view) and App.get_running_app().counter <= 3:
            self.parent.transition.direction = "up"
            self.parent.current = 'working_2'
        else:
            App.get_running_app().sound = "Are you still there?"
            self.sound_text = App.get_running_app().sound

    def stop_program(self):
        App.get_running_app().view = True


class Working2(Screen):
    pass


class Pop(Popup):
    pass


class MyApp(App):
    police = Main()
    view = True
    sound = ""
    counter = 0
    screen_manager = ScreenManager()

    def build(self):
        MyApp.screen_manager.add_widget(Graphics(name='graphics'))
        MyApp.screen_manager.add_widget(Working(name='working'))
        MyApp.screen_manager.add_widget(Working2(name='working_2'))
        MyApp.screen_manager.add_widget(Loading(name='loading'))
        return MyApp.screen_manager


if __name__ == '__main__':
    MyApp().run()
