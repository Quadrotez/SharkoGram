from pyrogram import Client, types
import reflex.errors
import re

def get_value_from_brackets(string, index):
    if index < len(matches := re.findall(r'\((.*?)\)', string)):
        return matches[index]
    else:
        return 'Индекс вне диапазона'

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
    session = app
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
            commands = {
                'reply_text': lambda m_id, m_c_id, l_string=string: (app.send_message(chat_id=m_c_id,
                                                                                      text=' '.join(
                                                                                          l_string),
                                                                                      reply_to_message_id=m_id)),
                'send_text': lambda m_id, m_c_id, l_string=string: (app.send_message(chat_id=m_c_id,
                                                                                     text=' '.join(
                                                                                         l_string[l_string.index(
                                                                                             ')') + 2:].split(' ')[1:]))
                                                                    )

            }

            try:
                reflex_dict[string[string.index('(') + 1:string.index(')')].lower()] = {
                    'COMMAND': commands[string[string.index(')') + 2:].split(' ')[0]]

                }
            except KeyError:
                raise reflex.errors.BadReflexCommandError(message='Bad Reflex Command "'
                                                                  f'{string[string.index(")") + 2:].split(" ")[0]}"')

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
