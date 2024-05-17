import functions


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
