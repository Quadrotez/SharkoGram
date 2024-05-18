import os
from pathlib import Path
import sqlite3
import functions
import pyrogram.errors.exceptions
from pyrogram import Client

db = sqlite3.connect('bases/base.db')
cursor = db.cursor()


class Sessions:
    def __init__(self):
        self.path = functions.path

    def count(self):
        return len([i for i in os.listdir(f'{self.path}/sessions') if (len(i.split('.')) > 1 and
                                                                       i.split('.')[1] == 'session') and
                    Path(f'{self.path}/sessions/{i}').is_file()])

    def blit(self):
        return [i for i in os.listdir(f'{self.path}/sessions') if (len(i.split('.')) > 1 and
                                                                   i.split('.')[1] == 'session') and
                Path(f'{self.path}/sessions/{i}').is_file()]


def get_image_country(code):
    for i in list(reversed(sorted([i[0] for i in tuple(cursor.execute('SELECT PHONE_CODE FROM COUNTRIES'))]))):
        if code[1:].startswith(str(i)):
            return (f"images/flags/" + str(tuple(cursor.execute(
                'SELECT COUNTRY_CODE FROM COUNTRIES WHERE PHONE_CODE = ?', (i,)))[0][0]) + ".png")

    return False


def check_valid_user(app: Client, user):
    try:
        app.get_chat(user)
        return True
    except (KeyError, pyrogram.errors.exceptions.bad_request_400.UsernameNotOccupied,
            pyrogram.errors.exceptions.bad_request_400.UsernameInvalid):
        return False


def first_chars(string, limit=20):
    r = ''
    dots = '...'
    string = string.replace('\n', '')
    if limit + 1 > len(string):
        limit = len(string) - 1
        dots = ''
    for i in range(limit + 1):
        r += string[i]

    return r + dots


def mkdir_weakly(*paths):
    [os.mkdir(i) for i in paths if not os.path.exists(i)]
