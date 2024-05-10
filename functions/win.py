import pyautogui


def gen_window_geometry():
    screen_width, screen_height = pyautogui.size()
    return (f'{round(screen_width / 1.3)}x{round(screen_height / 1.2)}'
            f'+{round(screen_width / 20)}+{round(screen_width / 100)}')


def gen_child_window_geometry():
    screen_width, screen_height = pyautogui.size()
    return (f'{round(screen_width / 4)}x{round(screen_height / 2.3)}'
            f'+{round(screen_width / 3)}+{round(screen_width / 10)}')


def gen_sub_window_geometry():
    screen_width, screen_height = pyautogui.size()
    return (f'{round(screen_width / 2)}x{round(screen_height / 1.9)}'
            f'+{round(screen_width / 3)}+{round(screen_width / 10)}')
