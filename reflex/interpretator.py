from pyrogram import Client, types
import reflex.errors
from reflex.commands_executors import *
import re





def _print(var, *args):
    if (var[0] == '"') & (var[-1] == '"'):
        print(var[1:-1])
        return

    for i in args:
        if var == i[0]:
            print(i[1])
            return




def run(strings: tuple | list, app: Client):

    reflex_dict = dict({})
    counter = 0
    for string in strings:
        commands = {
            'reply_text': lambda m_id, m_c_id, l_string=string: reflex.commands_executors.reply_text(m_id, m_c_id,
                                                                                                     l_string,
                                                                                                     app),
            'send_text': lambda m_id, m_c_id, l_string=string: reflex.commands_executors.send_text(m_c_id, l_string,
                                                                                                   app)}
        string: str
        counter += 1
        if not string or string[0] == '#':
            continue

        elif reflex.methods.get_word(string, 1) == 'print':
            _print(' '.join(string.split(' ')[1:]), ('session', 'session'))

        elif reflex.methods.get_word(string, 1) == 'reflex_on_text':





            try:
                reflex_dict[reflex.methods.get_value_from_brackets(string, 0).lower()] = {
                    'COMMAND': commands[reflex.methods.get_value_from_brackets(string, 1).lower()]

                }
            except AttributeError:
                raise reflex.errors.BadReflexCommandError(message='Bad Reflex Command "'
                                                                  f'{reflex.methods.get_value_from_brackets(string, 1)}"')

        elif reflex.methods.get_word(string, 1) == 'run':
            @app.on_message()
            def main_text(client: Client, message: types.Message):

                try:
                    reflex_dict[message.text.lower()]['COMMAND'](m_id=message.id, m_c_id=message.chat.id)
                except KeyError:
                    pass

            app.run()



        else:
            raise reflex.errors.BadStringError(message=f'Bad string: "{string}" on line {counter}')
