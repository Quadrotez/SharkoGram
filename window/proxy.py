import configparser
import tkinter as tk

import functions


def run():
    root = functions.create.window(functions.win.gen_sub_window_geometry())

    b_add_first_proxy = functions.create.button(master=root, text='+', font=('Arial', 20),
                                                command=lambda: (add(),
                                                                 root.destroy(),
                                                                 run()))

    def set_default(section):
        functions.config_proxy['DEFAULTIO']['MAIN'] = section
        functions.config_proxy.write(open(f'{functions.path}/config_proxy.ini', 'w', encoding='UTF-8'))
        root.destroy(),
        run()

    if len(functions.config_proxy.sections()) == 0:
        l_add_first_proxy = functions.create.label(master=root, text='У вас ещё нет прокси. Нажмите "+", чтобы '
                                                                     'добавить')
        l_add_first_proxy.pack()

        b_add_first_proxy.pack()

    else:
        (scrollbar := tk.Scrollbar(root, command=(slider_proxies := tk.Canvas(root, bg='#141414')).yview,
                                   bg='#141414')).pack(side="right", fill="y")

        slider_proxies.pack(expand=True, fill='y')

        slider_proxies.create_window((0, 0), window=(frame := tk.Frame(slider_proxies, bg='#141414')))
        slider_proxies.configure(yscrollcommand=scrollbar.set)

        for i in functions.config_proxy.sections():
            if i == 'DEFAULTIO':
                continue

            b_proxy = functions.create.button(master=frame, text=i,
                                              command=lambda name=i: (set_default(name)),
                                              bg='red' if functions.config_proxy['DEFAULTIO']['MAIN'] == i else None)
            b_proxy.pack()

        b_add_first_proxy.pack(pady=20)

        frame.update_idletasks()

        slider_proxies.config(scrollregion=slider_proxies.bbox("all"))

        root.bind_all("<MouseWheel>", lambda e: slider_proxies.yview_scroll(-1 * int((e.delta / 120)), "units"))

        b_delete_proxy = functions.create.button(master=root, text='Удалить (Выделенный) прокси',
                                                 command=lambda:
                                                 (functions.config_proxy.remove_section(
                                                     functions.config_proxy['DEFAULTIO']['MAIN']
                                                 ),
                                                  set_default('')))
        b_delete_proxy.pack()

        b_no_proxy = functions.create.button(master=root, text='Без прокси',
                                             command=lambda: set_default(''))
        b_no_proxy.pack()

    root.mainloop()


def add():
    root = functions.create.window(geometry=functions.win.gen_child_window_geometry())

    (functions.create.label(master=root, text='Адрес')).pack()
    (entry_address := functions.create.entry(master=root)).pack()
    (functions.create.label(master=root, text='Порт')).pack()
    (entry_port := functions.create.entry(master=root)).pack()
    (functions.create.label(text='Логин', master=root)).pack()
    (entry_login := functions.create.entry(master=root)).pack()
    (functions.create.label(text='Пароль', master=root)).pack()
    (entry_password := functions.create.entry(master=root)).pack()

    l_connection_type = functions.create.label(master=root, text='Тип соединения')
    l_connection_type.pack()

    def show_connection_type():
        if b_socks5.cget('bg') == 'red':
            return 'SOCKS5'
        elif b_http.cget('bg') == 'red':
            return 'HTTP'
        elif b_mt_proto.cget('bg') == 'red':
            return 'MTPROTO'

    def select_connection_type(b: tk.Button):
        b_http.configure(bg='gray')
        b_mt_proto.configure(bg='gray')
        b_socks5.configure(bg='gray')

        b.config(bg="red")

    b_socks5 = functions.create.button(master=root, text='SOCKS5', bg='gray',
                                       command=lambda: select_connection_type(b_socks5))
    b_socks5.pack()
    b_http = functions.create.button(master=root, text='HTTP', bg='gray',
                                     command=lambda: select_connection_type(b_http))
    b_http.pack()
    b_mt_proto = functions.create.button(master=root, text='MT PROTO', bg='gray',
                                         command=lambda: select_connection_type(b_mt_proto))
    b_mt_proto.pack()

    def check_data():
        return True if (entry_login.get() and entry_password.get() and entry_port.get() and entry_address.get() and
                        (b_socks5.cget('bg') == 'red' or b_http.cget('bg') == 'red' or b_mt_proto.cget('bg') == 'red'))\
                        else False

    while True:
        if check_data():
            break

        root.update()

    ready = tk.IntVar(value=0)

    def add_data():
        try:
            functions.config_proxy.add_section(entry_address.get())
            functions.config_proxy.write(open(f'{functions.path}/config_proxy.ini', 'w', encoding='UTF-8'))
            functions.config_proxy[entry_address.get()]['PORT'] = entry_port.get()
            functions.config_proxy[entry_address.get()]['LOGIN'] = entry_login.get()
            functions.config_proxy[entry_address.get()]['PASSWORD'] = entry_password.get()
            functions.config_proxy[entry_address.get()]['CONNECTION_TYPE'] = show_connection_type()
            functions.config_proxy.write(open(f'{functions.path}/config_proxy.ini', 'w', encoding='UTF-8'))
            ready.set(1)

        except configparser.DuplicateSectionError:
            pass

    b_ready = functions.create.button(master=root, text='Готово', command=add_data)
    b_ready.pack()

    while not ready.get():
        root.update()

    else:
        root.destroy()
