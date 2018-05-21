import math
from pyglet.sprite import Sprite


class Renderable(Sprite):

    IMGAGE_NAME = 'base.png'

    def __init__(self, img, *args, **kwargs):
        self._image = img
        self._center_image()
        super(Renderable, self).__init__(img=self._image, *args, **kwargs)

    def _center_image(self):
        self._image.anchor_x = self._image.width // 2
        self._image.anchor_y = self._image.height // 2


class Actor(Renderable):

    MAX_VELOCITY = 0

    def __init__(self, img, *args, **kwargs):
        super(Actor, self).__init__(img, *args, **kwargs)

        self.vel_x = 0.0
        self.vel_y = 0.0
        self.speed = 10

    def update(self, dt):
        self.update_velocity(dt)
        self.normalize_velocity()
        self.update_position(dt)

    def update_position(self, dt):
        self.clamp_position()
        self.x += self.vel_x * dt * self.speed
        self.y += self.vel_y * dt * self.speed

    def clamp_position(self):
        if self.x < 0 or self.x > 500:
            self.vel_x *= -1

        if self.y < 0 or self.y > 500:
            self.vel_y *= -1

    def update_velocity(self, dt):
        raise NotImplemented()

    def normalize_velocity(self):
        length = math.sqrt(math.pow(self.vel_x, 2) + math.pow(self.vel_y, 2))
        if length < 1:
            length = 1
        self.vel_x /= length
        self.vel_y /= length
