import pyglet
from ant_sim.agents.ant import AntAgent
from ant_sim.atractors import PheromoneManager

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

MAP_SIZE = 500

MAIN_BATCH = pyglet.graphics.Batch()

ant_agent1 = AntAgent(x=100, y=100, batch=MAIN_BATCH, speed=100)
ant_agent2 = AntAgent(x=150, y=100, batch=MAIN_BATCH, speed=100)

ANTS = [ant_agent1, ant_agent2]

game_objects = ANTS

PherManager = PheromoneManager(batch=MAIN_BATCH)


def update(dt):
    PherManager.update(dt)

    for obj in game_objects:
        x, y = obj.update(dt)
        PherManager.add_pheromone(x, y, lifetime=2)


pyglet.clock.schedule_interval(update, 1/60.0)
game_window = pyglet.window.Window(MAP_SIZE, MAP_SIZE)


@game_window.event
def on_draw():
    game_window.clear()
    MAIN_BATCH.draw()


if __name__ == '__main__':
    pyglet.app.run()
