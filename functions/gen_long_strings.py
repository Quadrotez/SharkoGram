import functions
from pyrogram import types

def button_text_recent_messages(i):
    return ((((f'{i.chat.first_name}{" " + i.chat.last_name if i.chat.last_name else ""}\n'
               f'{i.chat.username if i.chat.username else ""}') if i.chat.first_name else (i.chat.title if i.chat.title
                                                                                           else "Удалённый аккаунт")) + f'\n')
            + functions.method.first_chars(
                i.top_message.text if i.top_message.text else (i.top_message.caption
                                                               if i.top_message.caption else ""), 100))


def label_name(app):
    return f'''Sess_Name: {functions.data.get("SESSION_NOW")}
    Username: {app.get_me().username}
    Name: {app.get_me().first_name} {app.get_me().last_name if app.get_me().last_name else ""}'''

def name_interlocutor(app, name):
    chat = app.get_chat(name)
    return chat.first_name if chat.first_name else chat.title


def name_sender_in_chat(message: types.Message, me):
    if message.from_user and (message.from_user.id == me.id):
        return "Вы"
    elif message.from_user:
        return (f"{message.from_user.first_name}"
                f"{' ' + message.from_user.last_name if message.from_user.last_name else ''}")
    else:
        return message.chat.title
