import tkinter as tk
import functions


def run():
    root = functions.create.window()



    l_you_dont_have_an_internet = functions.create.label(text='Чувак, походу надо проверить своё подключение'
                                                              'к интернету',
                                                         font=('Arial', 20),
                                                         bg='#1f1f1f',
                                                         fg='#e3e3e3')
    l_you_dont_have_an_internet.pack(anchor='center', pady=(100, 40))

    b_retry = functions.create.button(text='Я проверил. Теперь должно работать', command=lambda: b_retry.destroy())
    b_retry.pack()

    while True:
        try:
            if not b_retry.winfo_exists():
                root.destroy()
                return True
            root.update()
        except:
            return False