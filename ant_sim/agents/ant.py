import math
import random
from ant_sim.agents.base import Actor


class AntAgent(Actor):

    MAX_VELOCITY = 10

    def __init__(self, img, *args, **kwargs):
        super(AntAgent, self).__init__(img, *args, **kwargs)

        self.state = 'wandering'
        self.speed = 40.0

        # start with random velocity
        self.vel_x = random.randint(0, 10) - 5
        self.vel_y = random.randint(0, 10) - 5

        self._random_walk_factor = .8

    def start_wandering(self):
        self.state = 'wandering'
        self.speed = 10.0

    def update_velocity(self, dt):
        r = random.randint(0, 100) / 100

        if self.state != 'wandering' or r < 0.9:
            return

        ox, oy = 0.0, 0.0
        px, py = self.vel_x, self.vel_y
        angle = random.randint(-90, 90) * self._random_walk_factor * dt

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

        self.vel_x = qx
        self.vel_y = qy
