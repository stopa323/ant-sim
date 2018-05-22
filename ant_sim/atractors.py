from agents.base import Renderable


class Pheromone(Renderable):
    IMGAGE_NAME = 'pheromone.png'

    def __init__(self, x, y, lifetime, *args, **kwargs):
        super(Pheromone, self).__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.lifetime = lifetime

    def update(self, dt):
        self.lifetime -= 1*dt

    def get_strength(self):
        return self.lifetime

    def is_valid(self):
        return self.lifetime > 0


class PheromoneManager(object):

    def __init__(self, batch):
        self.pheromones = dict()
        self.batch = batch

    def add_pheromone(self, x, y, lifetime=10):
        self.pheromones[hash((x, y))] = Pheromone(x, y, lifetime, batch=self.batch)

    def get_pheromone_by_position(self, x, y):
        _id = hash((x, y))
        return self.pheromones.get(_id)

    def update(self, dt):
        keys = self.pheromones.keys()
        for k in keys:
            self.pheromones[k].update(dt)
            if not self.pheromones[k].is_valid():
                del self.pheromones[k]
