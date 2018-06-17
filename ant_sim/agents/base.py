import math
import numpy as np
import pyglet


class Renderable(pyglet.sprite.Sprite):

    IMGAGE_NAME = 'base.png'

    def __init__(self, *args, **kwargs):
        self._image = pyglet.resource.image(self.IMGAGE_NAME)
        self._center_image()
        super(Renderable, self).__init__(img=self._image, *args, **kwargs)

    def _center_image(self):
        self._image.anchor_x = self._image.width // 2
        self._image.anchor_y = self._image.height // 2


class Actor(Renderable):

    MAX_SPEED = 0

    def __init__(self, *args, **kwargs):
        super(Actor, self).__init__(*args, **kwargs)

        self._mov_vec = np.array([.0, .0])
        """Normalized movement vector"""

        self._speed = .0
        """Current movement speed of the agent"""

    def update(self, dt):
        self.update_move_vector(dt)

        new_x, new_y = self.calculate_new_position(dt)
        new_x, new_y = self.handle_collisions(new_x, new_y)

        # update position
        self.x = new_x
        self.y = new_y

    def calculate_new_position(self, dt):
        new_x = self.x + self._mov_vec[0] * dt * self._speed
        new_y = self.y + self._mov_vec[1] * dt * self._speed
        return new_x, new_y

    def handle_collisions(self, x, y):
        raise NotImplemented()

    def update_move_vector(self, dt):
        raise NotImplemented()

    @staticmethod
    def normalize(vec2):
        """Normalize 2D vector."""
        return np.array(map(lambda row: row/np.linalg.norm(vec2), vec2))

    @staticmethod
    def rotate(vec2, angle):
        """Rotate 2D vector by angle CCW

        :param float angle: angle in degrees
        """
        angle = math.radians(angle)
        ox, oy = 0.0, 0.0
        px, py = vec2[0], vec2[1]

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

        return qx, qy

    def set_speed(self, new_speed):
        self._speed = np.clip(new_speed, 0, self.MAX_SPEED)

