from pyrogram import Client, types
import reflex.errors
import re


def get_value_from_brackets(string, index):
    if index < len(matches := re.findall(r'\((.*?)\)', string)):
        return matches[index]
    else:
        return False


def get_word(string: str, index: int):
    return string.split(' ')[index - 1] if len(string.split(' ')) > index - 1 else ''


def _print(var, *args):
    if (var[0] == '"') & (var[-1] == '"'):
        print(var[1:-1])
        return

    for i in args:
        if var == i[0]:
            print(i[1])
            return




def run(strings: tuple | list, app: Client):
    commands = {
        'reply_text': lambda m_id, m_c_id, l_string=string: (app.send_message(chat_id=m_c_id,
                                                                              text=get_value_from_brackets(
                                                                                  l_string, 2),
                                                                              reply_to_message_id=m_id)),
        'send_text': lambda m_id, m_c_id, l_string=string: (app.send_message(chat_id=m_c_id,
                                                                             text=get_value_from_brackets(l_string,
                                                                                                          2)))}
    reflex_dict = dict({})
    counter = 0
    for string in strings:
        string: str
        counter += 1
        if not string or string[0] == '#':
            continue

        elif get_word(string, 1) == 'print':
            _print(' '.join(string.split(' ')[1:]), ('session', 'session'))

        elif get_word(string, 1) == 'connect':
            app.connect()

        elif get_word(string, 1) == 'disconnect':
            app.disconnect()

        elif get_word(string, 1) == 'reflex_on_text':

            try:
                reflex_dict[get_value_from_brackets(string, 0).lower()] = {
                    'COMMAND': commands[get_value_from_brackets(string, 1).lower()]

                }
            except AttributeError:
                raise reflex.errors.BadReflexCommandError(message='Bad Reflex Command "'
                                                                  f'{get_value_from_brackets(string, 1)}"')

        elif get_word(string, 1) == 'run':
            @app.on_message()
            def main_text(client: Client, message: types.Message):

                try:
                    reflex_dict[message.text.lower()]['COMMAND'](m_id=message.id, m_c_id=message.chat.id)
                except KeyError:
                    pass

            app.run()


        else:
            raise reflex.errors.BadStringError(message=f'Bad string: "{string}" on line {counter}')
