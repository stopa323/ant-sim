import pyglet
import logging
from ant_sim.agents.ant import AntAgent
from ant_sim.atractors import PheromoneManager

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

MAP_SIZE = 800

MAIN_BATCH = pyglet.graphics.Batch()

ant_agent1 = AntAgent(x=100, y=100, batch=MAIN_BATCH, id='Janusz')#, smell=True, vec=[1, 1])
ant_agent2 = AntAgent(x=250, y=100, batch=MAIN_BATCH, id='Mirek')#, smell=True, vec=[-1, 5])
ant_agent3 = AntAgent(x=100, y=250, batch=MAIN_BATCH, id='Maciek')
ant_agent4 = AntAgent(x=250, y=450, batch=MAIN_BATCH, id='Kuba')
ant_agent5 = AntAgent(x=450, y=350, batch=MAIN_BATCH, id='Brajan')
ant_agent6 = AntAgent(x=350, y=250, batch=MAIN_BATCH, id='Zygmunt')
ant_agent7 = AntAgent(x=50, y=150, batch=MAIN_BATCH, id='Dionizy')

ANTS = [ant_agent1,
        ant_agent2,
        ant_agent3,
        ant_agent4,
        ant_agent5,
        ant_agent6,
        ant_agent7,
        ]

PherManager = PheromoneManager(batch=MAIN_BATCH)


def update(dt):
    PherManager.update(dt)

    for ant in ANTS:
        ant.update(dt)

        if ant.should_drop_pheromone():
            PherManager.add_pheromone(ant.x, ant.y, ant.id, lifetime=5)

        if ant.can_smell:
            pher = PherManager.get_nearby_pheromones(ant)
            if pher:
                # print('%s spotted pheromones: %s' % (ant.id, len(pher)))
                x, y = PherManager.get_pher_centroid(pher)
                ant.attract_to_pheromone(x, y)


pyglet.clock.schedule_interval(update, 1/40.0)
game_window = pyglet.window.Window(MAP_SIZE, MAP_SIZE)


@game_window.event
def on_draw():
    game_window.clear()
    MAIN_BATCH.draw()


if __name__ == '__main__':
    LOG.info('Starting main loop')
    pyglet.app.run()
