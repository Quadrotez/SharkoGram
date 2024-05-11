import time

from reflex.methods import *


def reply_text(m_id, m_c_id, l_string=None, app=None):
    if ((get_value_from_brackets(l_string, 4) and
            len([i for i in get_value_from_brackets(l_string, 4).split(',') if int(i) == m_c_id]) == 0) or
            (get_value_from_brackets(l_string, 5) and
             len([j for j in get_value_from_brackets(l_string, 5).split(',') if int(j) == m_c_id]) > 0)):
        return

    time.sleep(int(get_value_from_brackets(l_string, 3))) if get_value_from_brackets(l_string, 3) else ''
    time.sleep(int(get_value_from_brackets(l_string, 3))) if get_value_from_brackets(l_string, 3) else ''
    return app.send_message(chat_id=m_c_id, text=get_value_from_brackets(l_string, 2),
                            reply_to_message_id=m_id)


def send_text(m_c_id, l_string=None, app=None):
    if ((get_value_from_brackets(l_string, 4) and
            len([i for i in get_value_from_brackets(l_string, 4).split(',') if int(i) == m_c_id]) == 0) or
            (get_value_from_brackets(l_string, 5) and
             len([j for j in get_value_from_brackets(l_string, 5).split(',') if int(j) == m_c_id]) > 0)):
        return

    time.sleep(int(get_value_from_brackets(l_string, 3))) if get_value_from_brackets(l_string, 3) else ''

    return app.send_message(chat_id=m_c_id, text=get_value_from_brackets(l_string, 2))
