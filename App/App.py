import kivy.uix.button as kb
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.pagelayout import PageLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('graphics.kv')


class Graphics(Screen):
    pass


class NewScreen(Screen):
    pass


screen_manager = ScreenManager()
screen_manager.add_widget(Graphics(name='graphics'))
screen_manager.add_widget(NewScreen(name='new_screen'))


class MyApp(App):
    def build(self):
        return screen_manager


if __name__ == '__main__':
    MyApp().run()
