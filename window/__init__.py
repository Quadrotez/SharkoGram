import tkinter as tk

import functions
import window.load
from window import reflex_editor
import window.no_internet
import window.proxy
import window.create_session


def run():
    root = functions.create.window()

    b_create_sess = functions.create.button(master=root, font=('Arial', 20), text='Создать новую сессию',
                                            command=lambda: window.create_session.run(root, b_create_sess))

    if functions.method.Sessions().count() <= 0:
        (b_create_sess.configure(font=('Arial', 40)), b_create_sess.pack(pady=300))

    else:
        (b_proxy := functions.create.button(text='Прокси', command=window.proxy.run, )).pack(anchor='ne', padx=(0, 50))

        frame = functions.create.scroll_slider()

        (label_select_session := functions.create.label(text='Выберите сессию',
                                                        font=('Arial', 20))).pack(pady=(10, 10))

        buttons = []

        def select_session(file_name: str):
            functions.create.local_destroy(local_destroy)

            functions.data.add('SESSION_NOW', file_name.split('.')[0])
            window.load.main_menu(root, label_notification)

        label_notification = functions.create.label(master=root,
                                                    text='ПРИЛОЖЕНИЕ НЕ ЗАВИСЛО. '
                                                         'ПРОСТО ПОДОЖДИТЕ И НЕ ТЫКАЙТЕ ПО ОКНУ, '
                                                         'КАК 80-ТИ ЛЕТНЯЯ БАБУШКА',
                                                    bg='red',
                                                    fg='white')
        for i in functions.method.Sessions().blit():
            button = functions.create.button(master=frame[0],
                                             text=i.split('.')[0],
                                             font=('Arial', 15),
                                             command=lambda name=i: (label_notification.pack(),
                                                                     root.update(),
                                                                     root.unbind_all('<MouseWheel>'),
                                                                     select_session(name)),
                                             wraplength=frame[0].winfo_vrootwidth() // 5
                                             )
            button.pack(expand=True, fill=tk.X, )
            buttons.append(button)

        b_create_sess.configure(command=lambda: (functions.create.local_destroy(local_destroy),
                                                 root.unbind_all('<MouseWheel>'),
                                                 window.create_session.run(root, b_create_sess)))
        b_create_sess.pack(pady=5)

        root.bind_all("<MouseWheel>", lambda e: frame[2].yview_scroll(-1 * int((e.delta / 120)), "units"))

        b_open_reflex_editor = functions.create.button(text='Рефлекс-эдитор', command=reflex_editor.run)
        b_open_reflex_editor.pack(after=b_proxy, anchor='ne', padx=(0, 50))

        local_destroy = (label_select_session, b_create_sess, b_proxy, b_open_reflex_editor, buttons, frame)

    root.mainloop()
