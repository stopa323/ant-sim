import math
import numpy as np
from ant_sim.agents.base import Actor
from ant_sim.agents.ant import AntAgent


class Anthill(Actor):
    IMGAGE_NAME = 'anthill.png'

    def __init__(self, apples, x, y, *args, **kwargs):
        super(Anthill, self).__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.scale = .2

        self.spawn_interval = 1
        """Time (s) between consecutive ant spawns"""

        self.capacity = 50
        """Maximum number of ants"""

        self.spawn_timer = self.spawn_interval

        self.ants = list()

        self.apples = apples
        self.apple_size = 30
        self.anthill_size = 30

    def get_ants(self):
        return self.ants

    def spawn_ant(self):
        ant = AntAgent(x=self.x, y=self.y, batch=self.batch)
        self.ants.append(ant)

    def update(self, dt):
        for idx, ant in enumerate(self.ants):
            if not ant.has_apple:
                for a in self.apples:
                    dist = math.sqrt((ant.x - a.x)**2 +
                                     (ant.y - a.y)**2)
                    if dist <= self.apple_size:
                        ant.pick_up_apple()
            else:
                dist = math.sqrt((ant.x - self.x) ** 2 +
                                 (ant.y - self.y) ** 2)
                if dist <= self.anthill_size:
                    del self.ants[idx]

        if len(self.ants) < self.capacity:
            self.spawn_timer = np.clip(self.spawn_timer - dt, 0, self.spawn_timer)
            if self.spawn_timer == 0:
                self.spawn_timer = self.spawn_interval
                self.spawn_ant()
