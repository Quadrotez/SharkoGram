import os.path
import threading
import tkinter
import tkinter as tk
import functions
import reflex




def run(session = ''):
    root = functions.create.window(title='reflex Editor')

    main_text = functions.create.text(master=root, )
    main_text.pack()

    if os.path.exists(f'{functions.path}/reflex/main.rx'):
        [main_text.insert(tkinter.END, i) for i in open(f'{functions.path}/reflex/main.rx', 'r',
                                                        encoding='UTF-8').readlines()]

    b_save = functions.create.button(master=root, text='Сохранить',
                                     command=lambda: (open(f'{functions.path}/reflex/main.rx', 'w',
                                                           encoding='UTF-8').write(main_text.get("1.0", "end")),
                                                      root.update(),
                                                      (l_saved := functions.create.label(master=root,
                                                                                         text='Сохранено')).pack(),
                                                      root.update(),
                                                      root.after(1000, l_saved.destroy())))
    b_save.pack()

    root.mainloop()
