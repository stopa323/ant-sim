import pyglet
from ant_sim.agents.ant import AntAgent

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

MAP_SIZE = 500



MAIN_BATCH = pyglet.graphics.Batch()

ant_img = pyglet.resource.image("ant.png")
ant_agent1 = AntAgent(img=ant_img, x=100, y=100, batch=MAIN_BATCH)
ant_agent2 = AntAgent(img=ant_img, x=150, y=100, batch=MAIN_BATCH)

ANTS = [ant_agent1, ant_agent2]

game_objects = ANTS


def update(dt):
    for obj in game_objects:
        obj.update(dt)


pyglet.clock.schedule_interval(update, 1/120.0)
game_window = pyglet.window.Window(MAP_SIZE, MAP_SIZE)


@game_window.event
def on_draw():
    game_window.clear()
    MAIN_BATCH.draw()


if __name__ == '__main__':
    pyglet.app.run()
