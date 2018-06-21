import pyglet
import logging
from ant_sim.agents.ant import AntAgent
from ant_sim.agents.anthill import Anthill
from ant_sim.agents.apple import Apple
from ant_sim.atractors import PheromoneManager, Pheromone

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

MAP_SIZE = 800

MAIN_BATCH = pyglet.graphics.Batch()

# ant_agent1 = AntAgent(x=100, y=100, batch=MAIN_BATCH, id='Janusz')#, smell=True, vec=[1, 1])
# ant_agent2 = AntAgent(x=250, y=100, batch=MAIN_BATCH, id='Mirek')#, smell=True, vec=[-1, 5])
# ant_agent3 = AntAgent(x=100, y=250, batch=MAIN_BATCH, id='Maciek')
# ant_agent4 = AntAgent(x=250, y=450, batch=MAIN_BATCH, id='Kuba')
# ant_agent5 = AntAgent(x=450, y=350, batch=MAIN_BATCH, id='Brajan')
# ant_agent6 = AntAgent(x=350, y=250, batch=MAIN_BATCH, id='Zygmunt')
# ant_agent7 = AntAgent(x=50, y=150, batch=MAIN_BATCH, id='Dionizy')

APPLES = [
    Apple(x=100, y=700, batch=MAIN_BATCH),
    Apple(x=100, y=100, batch=MAIN_BATCH),
    # Apple(x=700, y=700, batch=MAIgggggN_BATCH),
]
ANTHILL = Anthill(apples=APPLES, x=700, y=100, batch=MAIN_BATCH)

# ANTS = [ant_agent1,
#         ant_agent2,
#         ant_agent3,
#         ant_agent4,
#         ant_agent5,
#         ant_agent6,
#         ant_agent7,
#         ]

PherManager = PheromoneManager(batch=MAIN_BATCH)

# add plenty of pheromone near anthill
import math
queen = AntAgent(x=700, y=100, batch=MAIN_BATCH, id='Dionizy')


def update_pheromones(dt):
    for x in range(-100, 100, 10):
        for y in range(-100, 100, 10):
            d = math.sqrt(x ** 2 + y ** 2)
            s = (150-d)/150
            print(s)
            p = Pheromone(x=700+x,
                          y=100+y,
                          lifetime=10*s,
                          owner=queen.id,
                          flavor='apple',
                          batch=MAIN_BATCH)
            PherManager.pheromones.append(p)


def update(dt):
    ANTHILL.update(dt)
    PherManager.update(dt)

    for ant in ANTHILL.get_ants():
        ant.update(dt)

        if ant.should_drop_pheromone():
            PherManager.add_pheromone(ant, lifetime=4)

        if ant.can_smell:
            pher = PherManager.get_nearby_pheromones(ant)
            if pher:
                # print('%s spotted pheromones: %s' % (ant.id, len(pher)))
                x, y = PherManager.get_pher_centroid(pher)
                ant.attract_to_pheromone(x, y)


pyglet.clock.schedule_interval(update, 1/40.0)
pyglet.clock.schedule_interval(update_pheromones, 5)
game_window = pyglet.window.Window(MAP_SIZE, MAP_SIZE)


@game_window.event
def on_draw():
    game_window.clear()
    MAIN_BATCH.draw()


if __name__ == '__main__':
    LOG.info('Starting main loop')
    pyglet.app.run()
