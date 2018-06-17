from ant_sim.agents.base import Renderable


class Apple(Renderable):
    IMGAGE_NAME = 'apple.png'

    def __init__(self, x, y, *args, **kwargs):
        super(Apple, self).__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.scale = .2
