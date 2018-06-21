import logging
import numpy as np
import uuid
from ant_sim.agents.base import Actor
from collections import namedtuple

LOG = logging.getLogger(__name__)

WORLD_SIZE = 800

ANT_STATE_TUPLE = namedtuple('AntState', ['WANDERING', 'FOLLOW'])
ANT_STATE = ANT_STATE_TUPLE(WANDERING='wandering',
                            FOLLOW='follow')

COL_FOLLOW_SEARCHER = (10, 200, 230)
COL_WANDERING = (190, 150, 90)
COL_FOLLOW_APPLE = (240, 90, 90)


class AntAgent(Actor):

    IMGAGE_NAME = 'ant.png'
    MAX_SPEED = 50

    def __init__(self, id=None, vec=None, smell=True, *args, **kwargs):
        super(AntAgent, self).__init__(*args, **kwargs)

        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())[:10]

        self.color = COL_WANDERING
        self.state = ANT_STATE.WANDERING
        """Current state of the agent, determines behavior"""

        self._turn_angle = 5.0
        """Angle by which ant will change its move vector"""

        self._turn_likehood = .07
        """Probability ant will rotate its move vector (computed each frame)"""

        self._dir_change_likehood = .3
        """Probability ant will change its turn angle to opposite
           (computed on each turn event)"""

        self.pheromone_freq = .18
        """How frequent (s) drop a pheromone"""

        self.smell_range = 20
        """Determines how far ant can detect pheromone"""

        self.smell_angle = 90
        """Determines field of smell, both directions"""

        self.can_smell = smell
        """Determines if ant will use pheromones to compute path"""

        self.follow_time = 2
        """Time (s) ant will not attempt to change direction after loosing track"""

        self.pheromone_timer = self.pheromone_freq
        self.follow_timer = self.follow_time

        self.has_apple = False

        if not vec:
            self.reset_mov_vec()
        else:
            self._mov_vec = self.normalize(vec)
        self.set_speed(self.MAX_SPEED)

    def reset_mov_vec(self):
        self._mov_vec = self.normalize([np.random.rand() - .5,
                                        np.random.rand() - .5])

    def update(self, dt):
        self.pheromone_timer = np.clip(self.pheromone_timer - dt,
                                       0, self.pheromone_freq)
        self.follow_timer = np.clip(self.follow_timer - dt,
                                    0, self.follow_time)
        if self.state == ANT_STATE.FOLLOW and self.follow_timer == 0:
            self.state = ANT_STATE.WANDERING
            self.color = COL_WANDERING
            LOG.info('ANT<%s> State=%s' % (self.id, self.state))

        super(AntAgent, self).update(dt)

    def pick_up_apple(self):
        self.has_apple = True
        self.color = COL_FOLLOW_APPLE

    def attract_to_pheromone(self, x, y):
        if self.state != ANT_STATE.FOLLOW:
            self.state = ANT_STATE.FOLLOW
            if self.has_apple:
                self.color = COL_FOLLOW_APPLE
            else:
                self.color = COL_FOLLOW_SEARCHER
            LOG.info('ANT<%s> State=%s' % (self.id, self.state))
        new_x, new_y = x - self.x, y - self.y
        self._mov_vec = self.normalize(np.array([new_x, new_y]))
        self.follow_timer = self.follow_time

    def should_drop_pheromone(self):
        if self.pheromone_timer == 0:
            self.pheromone_timer = self.pheromone_freq
            return True
        return False

    def update_move_vector(self, dt):
        if self.state == ANT_STATE.WANDERING:
            # do we change traverse direction?
            if np.random.rand() < self._turn_likehood:
                if np.random.rand() < self._dir_change_likehood:
                    self._turn_angle *= -1
                self._mov_vec = self.normalize(
                    self.rotate(
                        self._mov_vec, self._turn_angle))

    def handle_collisions(self, x, y):
        if x <= 0:
            x = WORLD_SIZE
        elif x >= WORLD_SIZE:
            x = 0
        if y <= 0:
            y = WORLD_SIZE
        elif y >= WORLD_SIZE:
            y = 0
        return x, y
