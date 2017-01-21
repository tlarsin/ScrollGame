from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ListProperty, NumericProperty, ReferenceListProperty,\
    ObjectProperty

class SpriteCharacter(Widget):
    pass

class RunGame(Widget):
    sprite = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RunGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        return True

class RunApp(App):
    def build(self):
        game = RunGame()
        return game

if __name__ == "__main__":
    RunApp().run()
