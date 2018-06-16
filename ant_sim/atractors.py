import math
from agents.base import Renderable


class Pheromone(Renderable):
    IMGAGE_NAME = 'pheromone.png'

    def __init__(self, x, y, lifetime, *args, **kwargs):
        super(Pheromone, self).__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.lifetime = lifetime
        self.time_left = self.lifetime
        self.opacity = 200

    def update(self, dt):
        self.time_left -= 1 * dt
        self.opacity = int(200 * self.time_left / self.lifetime)

    def get_strength(self):
        return self.time_left

    def is_valid(self):
        return self.time_left > 0


class PheromoneManager(object):

    def __init__(self, batch):
        self.pheromones = dict()
        self.batch = batch

    def add_pheromone(self, x, y, lifetime=10):
        self.pheromones[hash((x, y))] = Pheromone(x, y, lifetime, batch=self.batch)

    def is_pheromone_nearby(self, x, y, vx, vy):
        SMELL_RADIUS = 3
        SMELL_ANGLE = 45
        near_pher = list()
        for p in self.pheromones.values():
            dist = math.sqrt(pow(x - p.x, 2) + pow(y - p.y, 2))
            if dist < SMELL_RADIUS:
                near_pher.append(p)

        for p in near_pher:
            _vx, _vy = p.x - x, p.y - y
            angle = self.angle_clockwise((vx, vy), (_vx, _vy))
            if angle < SMELL_ANGLE:
                return True

    def length(self, v):
        return math.sqrt(v[0] ** 2 + v[1] ** 2)

    def dot_product(self, v, w):
        return v[0] * w[0] + v[1] * w[1]

    def determinant(self, v, w):
        return v[0] * w[1] - v[1] * w[0]

    def inner_angle(self, v, w):
        cosx = self.dot_product(v, w) / (self.length(v) * self.length(w))
        print(cosx)
        rad = math.acos(cosx)  # in radians
        return rad * 180 / math.pi  # returns degrees

    def angle_clockwise(self, A, B):
        inner = self.inner_angle(A, B)
        det = self.determinant(A, B)
        if det < 0:  # this is a property of the det. If the det < 0 then B is clockwise of A
            return inner
        else:  # if the det > 0 then A is immediately clockwise of B
            return 360 - inner

    def update(self, dt):
        keys = self.pheromones.keys()
        for k in keys:
            self.pheromones[k].update(dt)
            if not self.pheromones[k].is_valid():
                del self.pheromones[k]
