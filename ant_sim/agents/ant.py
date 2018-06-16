import numpy as np
from ant_sim.agents.base import Actor

WORLD_SIZE = 500


class AntAgent(Actor):

    IMGAGE_NAME = 'ant.png'
    MAX_SPEED = 200

    def __init__(self, speed, *args, **kwargs):
        super(AntAgent, self).__init__(*args, **kwargs)

        self.state = 'wandering'
        """Current state of the agent, determines behavior"""

        self._turn_angle = 5.0
        """Angle by which ant will change its move vector"""

        self._turn_likehood = .07
        """Probability ant will rotate its move vector (computed each frame)"""

        self._dir_change_likehood = .3
        """Probability ant will change its turn angle to opposite
           (computed on each turn event)"""

        self._mov_vec = self.normalize([np.random.rand() - .5,
                                        np.random.rand() - .5])

        self.set_speed(speed)

    def update_move_vector(self, dt):
        # do we change traverse direction?
        if np.random.rand() < self._turn_likehood:
            if np.random.rand() < self._dir_change_likehood:
                self._turn_angle *= -1
            self._mov_vec = self.normalize(
                self.rotate(
                    self._mov_vec, self._turn_angle))

    def handle_collisions(self, x, y):
        if x <= 0 or x >= WORLD_SIZE:
            x = np.clip(x, 0, WORLD_SIZE)
            self._mov_vec[0] *= -1

        if y <= 0 or y >= WORLD_SIZE:
            y = np.clip(y, 0, WORLD_SIZE)
            self._mov_vec[1] *= -1

        return x, y
