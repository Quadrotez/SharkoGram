import os.path
import threading
import tkinter
import tkinter as tk
import webbrowser

import functions
import reflex


def run():
    root = functions.create.window(title='reflex Editor')

    main_text = functions.create.text(master=root, )
    main_text.pack()

    if os.path.exists(f'{functions.path}/reflex/main.rx'):
        [main_text.insert(tkinter.END, i) for i in open(f'{functions.path}/reflex/main.rx', 'r',
                                                        encoding='UTF-8').readlines()]

    (functions.create.button(master=root, text='Сохранить',
                             command=lambda: (open(f'{functions.path}/reflex/main.rx', 'w',
                                                   encoding='UTF-8').write(main_text.get("1.0", "end")),
                                              root.update(),
                                              (l_saved := functions.create.label(master=root,
                                                                                 text='Сохранено')).pack(),
                                              root.update(),
                                              root.after(1000, l_saved.destroy())))).pack()

    ((b_view_doc := functions.create.button(master=root, text='Документация',
                                            command=lambda: webbrowser.open(
                                                'https://github.com/Quadrotez/SharkoGram/blob/master/doc/reflex.MD')))
     .pack(anchor='ne', side=tk.LEFT, before=main_text))

    (b_start := functions.create.button(master=root, text='Запустить', font=('Arial', 20),
                                        command=lambda: os.startfile('reflex_runner.py'))).pack()

    root.mainloop()
