import kivy.uix.button as kb
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


Builder.load_file('graphics.kv')


class Graphics(Widget):
    def __init__(self, **kwargs):
        super(Graphics, self).__init__(**kwargs)

    def say_hello(self):
        print("hello")


class MyApp(App):
    def build(self):
        return Graphics()


if __name__ == '__main__':
    MyApp().run()
