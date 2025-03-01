from random import randint
from missile_collection import check_missiles_collision
from units import Tank
from tkinter import NW
import world

_tanks = []
_canvas = None
id_screen_text = 0


def initialize(canv):
    global _canvas, id_screen_text
    _canvas = canv
    player = spawn(False)
    enemy = spawn(True).set_target(player)
    spawn(True).set_target(player)

    id_screen_text = _canvas.create_text(10, 10,
                                         text=_get_screen_text(),
                                         font=('TkDefualFont', 20),
                                         fill='black',
                                         anchor=NW)


def _get_screen_text():
    if get_player().is_destroyed():
        return 'GAME OVER'
    if len(_tanks) == 1:
        return 'YOU WON'
    return 'осталось {}'.format(len(_tanks) - 1)


def _update_screen():
    _canvas.itemconfig(id_screen_text, text=_get_screen_text())


def get_player():
    return _tanks[0]


def update():
    _update_screen()
    start = len(_tanks) - 1
    for i in range(start, -1, -1):
        if _tanks[i].is_destroyed() and i != 0:
            del _tanks[i]
        else:
            _tanks[i].update()
            check_collision(_tanks[i])
            check_missiles_collision(_tanks[i])


def check_collision(tank):
    for other_tank in _tanks:
        if tank == other_tank:
            continue
        if tank.intersect(other_tank):
            return True
    return False


def spawn_enemy():
    pos_x = randint(200, world.WIDTH - 200)
    pos_y = randint(200, world.HEIGHT - 200)
    t = Tank(_canvas, x=pos_x, y=pos_y, speed=1)

    t.set_target(get_player())
    _tanks.append(t)


def spawn(is_bot=True):
    cols = world.get_cols()
    rows = world.get_rows()

    while True:
        col = randint(1, cols - 1)
        row = randint(1, rows - 1)

        if world.get_block(row, col) != world.GROUND:
            continue

        t = Tank(_canvas, row,
                 col, bot=is_bot)

        if not check_collision(t):
            _tanks.append(t)
            return t
