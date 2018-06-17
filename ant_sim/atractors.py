import math
import numpy as np
from agents.base import Renderable


class Pheromone(Renderable):
    IMGAGE_NAME = 'pheromone.png'

    def __init__(self, x, y, lifetime, owner, *args, **kwargs):
        super(Pheromone, self).__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.lifetime = lifetime
        self.time_left = self.lifetime
        self.opacity = 200
        self.owner = owner

    def update(self, dt):
        self.time_left -= 1 * dt
        self.opacity = int(255 * self.time_left / self.lifetime)

    def get_strength(self):
        return self.time_left / self.lifetime

    def is_valid(self):
        return self.time_left > 0


class PheromoneManager(object):

    def __init__(self, batch):
        self.pheromones = list()
        self.batch = batch

    def add_pheromone(self, x, y, owner, lifetime=10):
        self.pheromones.append(Pheromone(x, y, lifetime, owner, batch=self.batch))

    def get_nearby_pheromones(self, ant):
        ant_id = ant.id
        x = ant.x
        y = ant.y
        smell_range = ant.smell_range
        smell_angle = ant.smell_angle

        # remove pheromones belonging to given ant and outside range
        valid1 = filter(lambda pher:
                       (pher.owner != ant_id) and
                       (x - smell_range < pher.x < x + smell_range) and
                       (x - smell_range < pher.y < y + smell_range),
                       self.pheromones)

        # radius range filter
        valid2 = filter(lambda p: PheromoneManager.length(
            [p.x - x, p.y - y]) < smell_range, valid1)

        # angle filter
        valid3 = filter(lambda p: PheromoneManager.angle_between(
            [x, y], [p.x - x, p.y - y]) < smell_angle, valid2)
        # print("%s\t%s\t%s" % (len(valid1), len(valid2), len(valid3)))
        return valid3

    def get_pher_centroid(self, pheromones):
        """Return weighted centroid from pheromones"""
        tri = map(lambda p: (p.x, p.y, p.get_strength()), pheromones)
        tri = zip(*tri)
        x, y, w = tri[0], tri[1], tri[2]

        # # normalize and raise to power of 2
        w = map(lambda x: x**2, map(lambda v: v/np.linalg.norm(w), w))

        avg_x = np.average(x, weights=w)
        avg_y = np.average(y, weights=w)
        return avg_x, avg_y

    @staticmethod
    def unit_vector(vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

    @staticmethod
    def angle_between(v1, v2):
        """ Returns the angle in degrees between vectors 'v1' and 'v2'"""
        v1_u = PheromoneManager.unit_vector(v1)
        v2_u = PheromoneManager.unit_vector(v2)
        return math.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

    @staticmethod
    def length(v):
        return math.sqrt(v[0] ** 2 + v[1] ** 2)

    def update(self, dt):
        for idx, pher in enumerate(self.pheromones):
            pher.update(dt)
            if not pher.is_valid():
                del self.pheromones[idx]
