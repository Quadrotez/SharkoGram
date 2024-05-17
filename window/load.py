import os
import tkinter as tk

import PIL
import cryptography.fernet
import pyrogram.errors.exceptions.all
from pyrogram import Client, types
import pyrogram.errors.exceptions.not_acceptable_406
import functions
import window
from functions import data, ciph


def main_menu(root: tk.Tk, label_notification: tk.Button = None):
    app = functions.create.client(data.get('SESSION_NOW'))

    try:
        app.connect()
        (label_name := functions.create.label(text=functions.gen_long_strings.label_name(app))).pack(anchor='nw',
                                                                                                     padx=5, pady=5)
    except pyrogram.errors.exceptions.unauthorized_401.AuthKeyUnregistered:
        app.disconnect()
        try:
            os.remove(f'{functions.path}/sessions/{data.get("SESSION_NOW")}.session')
        except PermissionError:
            pass
        root.destroy()
        window.run()
    label_notification.destroy() if label_notification else ''
    (b_go_to_session_menu := functions.create.button(text='В меню выбора сессий',
                                                     command=lambda: (root.destroy(),
                                                                      app.disconnect(),
                                                                      window.run()))).pack(anchor='nw')

    b_add_contacts = functions.create.button(text='Добавить контакт',
                                             command=lambda: (add_contact_directly(app),
                                                              ready.set(1)))

    if not app.get_contacts():
        ready = tk.IntVar(value=0)
        (label_you_dont_have_any_contacts := functions.create.label(text='У вас нет контактов:(\n'
                                                                         'Но вы можете добавить новые')).pack(pady=(0,
                                                                                                                    10))
        b_add_contacts.pack()

        root.wait_variable(ready)

        label_you_dont_have_any_contacts.destroy()

    b_add_contacts.configure(command=lambda: (add_contact_directly(app),
                                              contacts_list()))

    b_add_contacts.pack(anchor='nw')

    contacts, recent_messages = [], []

    (frame_contacts := functions.create.frame(master=root)).pack(side=tk.RIGHT)
    (l_desc_contacts := functions.create.label(master=frame_contacts, text='Контакты',
                                               font=('System', 15))).pack(side=tk.TOP)
    frame_contacts_slider = functions.create.scroll_slider(args_for_frame={'master': frame_contacts}, width_canvas=400,
                                                           height_canvas=500, side=tk.TOP)

    (frame_recent_messages := functions.create.frame(master=root)).pack(side=tk.RIGHT)
    (l_desc_recent_messages := functions.create.label(master=frame_recent_messages, text='Недавние сообщения',
                                                      font=('System', 15))).pack(side=tk.TOP)

    frame_recent_messages_slider = functions.create.scroll_slider(args_for_frame={'master': frame_recent_messages},
                                                                  width_canvas=400,
                                                                  height_canvas=500, side=tk.TOP)

    def recent_messages_list():
        functions.create.local_destroy(recent_messages)
        try:
            for i in app.get_dialogs():
                button = functions.create.button(master=frame_recent_messages_slider[0],
                                                 text=functions.gen_long_strings.button_text_recent_messages(i),
                                                 font=('Arial', 15),
                                                 wraplength=frame_recent_messages_slider[0].winfo_vrootwidth() // 5,
                                                 command=lambda name=i.chat.id:
                                                 (functions.create.local_destroy(local_destroy),
                                                  root.unbind('<Return>'),
                                                  select_contact(name, app, root, label_name=label_name)))
                button.pack()
                recent_messages.append(button)
        except pyrogram.errors.exceptions.not_acceptable_406.ChannelPrivate:
            (l_something_went_wrong := functions.create.label(master=frame_recent_messages_slider[0],
                                                              text='Что-то пошло не так...')).pack()
            recent_messages.append(l_something_went_wrong)

    def contacts_list():
        functions.create.local_destroy(contacts)
        for i in sorted(list(app.get_contacts()), key=lambda x: x.first_name):
            button = functions.create.button(master=frame_contacts_slider[0],
                                             text=f'{i.first_name}{(" " + i.last_name) if i.last_name else ""}\n'
                                                  f'{i.username if i.username else ""}',
                                             font=('Arial', 15),
                                             wraplength=frame_contacts_slider[0].winfo_vrootwidth() // 5,
                                             command=lambda name=i.id:
                                             (functions.create.local_destroy(local_destroy),
                                              root.unbind('<Return>'),
                                              select_contact(name, app, root, label_name=label_name)))
            button.pack()
            contacts.append(button)

    contacts_list()
    recent_messages_list()

    root.bind_all("<MouseWheel>",
                  lambda e: (frame_contacts_slider[2].yview_scroll(-1 * int((e.delta / 120)), "units"),
                             frame_recent_messages_slider[2].yview_scroll(-1 * int((e.delta / 120)), "units")))

    (e_search := functions.create.entry()).pack(anchor='se', side=tk.LEFT, fill=tk.X, expand=True, pady=(0, 50),
                                                padx=(50, 0))

    def command_search(e):
        ((e_search_get := e_search.get(),
          functions.create.local_destroy(local_destroy),
          root.unbind('<Return>'),
          select_contact(e_search_get, app, root,
                         label_name=label_name)) if
         functions.method.check_valid_user(app, e_search.get()) else (
            (l_this_contact_does_not_exists := functions.create.label(text='Не найдено',
                                                                      bg='red',
                                                                      fg='white',
                                                                      )).pack(side=tk.BOTTOM, before=e_search),
            root.after(1000, l_this_contact_does_not_exists.destroy)

        ))

    (b_search := functions.create.button(text='Поиск', command=lambda: command_search(''))).pack(anchor='sw',
                                                                                                 side=tk.RIGHT,
                                                                                                 pady=(0, 50),
                                                                                                 padx=(0, 50))

    local_destroy = (b_add_contacts,
                     b_go_to_session_menu,
                     e_search,
                     b_search,
                     l_desc_contacts,
                     frame_contacts,
                     frame_recent_messages)
    root.bind('<Return>', command_search)


def add_contact_directly(app: Client):
    root = functions.create.window(geometry=functions.win.gen_child_window_geometry())

    (functions.create.label(master=root, text='Имя')).pack()
    (entry_first_name := functions.create.entry(master=root)).pack()
    (functions.create.label(master=root, text='Фамилия (Необязательно)')).pack()
    (entry_last_name := functions.create.entry(master=root)).pack()
    (functions.create.label(text='Юзернейм (Или чат-id)',
                            master=root)).pack()

    (entry_chat_id := functions.create.entry(master=root)).pack()

    def check_data():
        try:
            return True if entry_first_name.get() and entry_chat_id.get() else False
        except:
            return 'END'

    while True:
        if cd := check_data():
            break

        elif cd == 'END':
            return

        root.update()

    def add():
        try:
            app.add_contact(entry_chat_id.get(),
                            entry_first_name.get(),
                            entry_last_name.get())

            label_success = functions.create.label(master=root, text='Успешно добавлен контакт!')
            label_success.pack()
            root.destroy()

        except:
            label_error = functions.create.label(master=root, text='Что-то не так!')
            label_error.pack()

    try:
        b_ready = functions.create.button(master=root, text='Готово', command=add)
        b_ready.pack()
        while True and root.winfo_exists():
            root.update()

    except:
        return


def select_contact(name: int, app: Client, root: tk.Tk, label_name=None):
    functions.ciph.path = functions.path
    app.me = me = app.get_me()

    bool_encrypt = tk.BooleanVar()

    def insert_default_key(*args, force=False):
        if force:
            entry_key.delete(0, tk.END)
            entry_key.insert(0, functions.config['GENERAL']['KEY'])

    def send_message(text: str):
        entry_message.delete(0, tk.END)
        root.update()
        if bool_encrypt.get():
            app.send_document(app.get_chat(name).id, ciph.encrypt(text, entry_key.get()), file_name='12345')

        else:
            app.send_message(name, text)

    (button_main_menu := functions.create.button(text='В главное меню', command=lambda: (app.disconnect(),
                                                                                         functions.create.local_destroy(
                                                                                             local_destroy),
                                                                                         root.unbind('<Return>'),
                                                                                         main_menu(root)))).pack(
        anchor='ne', side=tk.LEFT)

    (scrollbar := tk.Scrollbar(root, command=(slider_messages := tk.Canvas(root, bg='#141414')).yview,
                               bg='#141414')).pack(side="right", fill="y")

    toggle_encrypt = tk.Checkbutton(root, text="Зашифровывать/Расшифровывать текст", variable=bool_encrypt)
    toggle_encrypt.pack(anchor='ne')
    label_entry_key = functions.create.label(text='Введите ключ')
    label_entry_key.pack(anchor='ne')
    entry_key = functions.create.entry()
    entry_key.pack(anchor='ne')

    button_generate_key = functions.create.button(text='Сгенерировать ключ',
                                                  command=lambda: (entry_key.delete(0, tk.END),
                                                                   entry_key.insert(0, str(ciph.gen_key()))))
    button_generate_key.pack(anchor='ne')

    (b_add_key_to_default := functions.create.button(text='Запомнить ключ',
                                                     command=lambda: (functions.config.set('GENERAL', 'KEY',
                                                                                           entry_key.get()),
                                                                      functions.config.write(
                                                                          open(f'{functions.path}/config.ini',
                                                                               'w',
                                                                               encoding='UTF-8'))))).pack(anchor='ne')

    l_name_interlocutor = functions.create.label(master=root, text=app.get_chat(name).first_name)
    l_name_interlocutor.pack()

    slider_messages.pack(expand=True, fill='y')
    slider_messages.create_window((0, 0), window=(frame := tk.Frame(slider_messages, bg='#141414')), anchor="ne")
    slider_messages.configure(yscrollcommand=scrollbar.set)

    messages = []

    def blit_messages(message=None):
        (ll := functions.create.label(master=frame, text='_' * 90, bg='#141414', fg='#db51cd')).pack()
        messages.append(ll)
        try:
            chat_history = reversed(list(app.get_chat_history(name, limit=100)))
        except pyrogram.errors.exceptions.bad_request_400.UsernameInvalid:
            return

        for i in chat_history:
            i: types.Message
            message = functions.create.label(master=frame, local_style='label_message',
                                             wraplength=frame.winfo_vrootwidth() // 5)
            if i.document and entry_key.get() != '' and bool_encrypt.get():
                app.download_media(i.document.file_id, file_name='1.png')

                try:
                    message.configure(text=f'{"Вы" if i.from_user.id == me.id else i.chat.first_name} (decrypted): '
                                           f'{ciph.decrypt(str(entry_key.get()), local_path="downloads/1.png")}')
                except cryptography.fernet.InvalidToken:
                    message.configure(text=f'{"Вы" if i.from_user.id == me.id else i.from_user.first_name}: '
                                           f'InvalidFernetToken')

                except PIL.UnidentifiedImageError:
                    message.configure(text=f'{"Вы" if i.from_user.id == me.id else i.from_user.first_name}: '
                                           f'UnidentifiedImageError')

            elif i.text:
                (lb := functions.create.button(master=frame, text='Скопировать',
                                               command=lambda name=i.text: (root.clipboard_clear(),
                                                                            root.clipboard_append(name)))).pack()
                messages.append(lb)

                message.configure(text=f'{"Вы" if i.from_user.id == me.id else i.from_user.first_name}: {i.text}')

            elif i.photo:
                message = functions.create.button(master=frame,
                                                  text=f'{"Вы" if i.from_user.id == me.id else i.from_user.first_name}: '
                                                       f'Фото',
                                                  command=lambda j=i: (
                                                      os.startfile(str(app.download_media(j.photo.file_id,
                                                                                          file_name='photo.png'))),
                                                  ))


            elif i.video:
                message = functions.create.button(master=frame,
                                                  text="Вы" if i.from_user and (
                                                          i.from_user.id == me.id) else i.from_user.first_name + ":"
                                                                                                                 f'Видео',
                                                  command=lambda j=i: (
                                                      os.startfile(str(app.download_media(j.video.file_id,
                                                                                          file_name='video.mp4'))),
                                                  ))

            elif i.voice:
                message = functions.create.button(master=frame,
                                                  text="Вы" if i.from_user and (
                                                          i.from_user.id == me.id) else i.from_user.first_name + ":"
                                                                                                                 f'Голосовое сообщение',
                                                  command=lambda j=i: (
                                                      os.startfile(str(app.download_media(j.voice.file_id,
                                                                                          file_name='voice.mp3'))),
                                                  ))


            else:
                message.configure(text=f'{"Вы" if i.from_user.id == me.id else i.chat.first_name}: '
                                       f'Неизвестный тип данных')

            (message.pack(), messages.append(message)) if message else ''
            (ll := functions.create.label(master=frame, text='_' * 90, bg='#141414', fg='#db51cd')).pack()
            messages.append(ll)

        slider_messages.yview_moveto(1.0)
        frame.update_idletasks()
        slider_messages.config(scrollregion=slider_messages.bbox("all"))

    blit_messages()
    root.bind_all("<MouseWheel>", lambda e: slider_messages.yview_scroll(-1 * int((e.delta / 120)), "units"))

    root.bind('<Return>', lambda e: (root.update(),
                                     send_message(entry_message.get()),
                                     [i.destroy() for i in messages],
                                     blit_messages(),
                                     ))

    (button_update := functions.create.button(text='Обновить', command=lambda: ([i.destroy() for i in messages],
                                                                                blit_messages()))).pack(anchor='sw',
                                                                                                        side=tk.LEFT,
                                                                                                        pady=(0, 50),
                                                                                                        padx=(50, 0))

    (entry_message := functions.create.entry()).pack(anchor='se', side=tk.LEFT, fill=tk.X, expand=True, pady=(0, 50))

    (button_send_message := functions.create.button(text='Отправить',
                                                    command=lambda: (root.update(),
                                                                     send_message(entry_message.get()),
                                                                     [i.destroy() for i in messages],
                                                                     blit_messages(),
                                                                     ))).pack(anchor='sw', side=tk.RIGHT, pady=(0, 50),
                                                                              padx=(0, 50))

    if functions.config.has_option('GENERAL', 'KEY'):
        insert_default_key(force=True)

    local_destroy = (slider_messages, frame, scrollbar, button_main_menu, entry_message, toggle_encrypt,
                     label_entry_key, entry_key, button_generate_key, button_update, button_send_message,
                     label_name if label_name else None, b_add_key_to_default, l_name_interlocutor)
