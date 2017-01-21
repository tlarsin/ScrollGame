from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ListProperty, NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class SpriteCharacter(Widget):
    distance = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    running = True

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class Block(Widget):
    velocity = NumericProperty(1)

    def __init__(self, **kwargs):
        super(Block, self).__init__(**kwargs)

    def update(self, dt):
        self.x -= self.velocity

class RunGame(Widget):
    sprite = ObjectProperty(None)
    block = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RunGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w' and self.sprite.running:
            self.initiateVel(vel = (0, 1.2))
            self.sprite.running = True
        if keycode[1] == 'p' and self.sprite.running:
            self.sprite.running = False
        if keycode[1] == 's' and not self.sprite.running:
            self.sprite.running = True
        return True

    def initiateVel(self, vel=(0,-1)):
        self.sprite.velocity = vel

    def gravity(self):
        if self.sprite.y > self.block.height:
            vx, vy = self.sprite.velocity
            result = Vector(vx, -.6 * vy)
            vel = result
            self.initiateVel(vel = (vel.x, vel.y))

    def score(self):
        distance = self.sprite.center_x - self.sprite.distance
        return distance

    def restart(self):
        # Reset Sprite
        self.sprite.center_x = self.center_x
        self.sprite.y = self.block.height

        # Reset map
        self.block.center_x = self.center_x
        self.initiateVel(vel = (0, -1))

    def score(self):
        distance = self.sprite.center_x - self.sprite.x
        return distance

    def update(self, dt):
        self.sprite.move()

        if self.sprite.running:
            self.block.update(dt)

        # Fall off of block
        if self.sprite.collide_widget(self.block):
            self.sprite.y = self.block.height

        # Reset if falls out of map
        # Also displays score
        if self.sprite.y < self.y:
            self.sprite.distance = self.score()
            self.restart()

        # Gravity
        if self.sprite.y > self.block.height + 30:
            self.gravity()

class RunApp(App):
    def build(self):
        game = RunGame()
        game.initiateVel()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == "__main__":
    RunApp().run()
