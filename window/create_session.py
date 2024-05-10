import dynamic_config
import functions
import concurrent.futures
import threading
import tkinter as tk
import asyncio
import pyrogram.errors
from pyrogram import Client
from PIL import Image, ImageTk
import window.load


def run(root: tk.Tk, b_create_sess: tk.Button):
    b_create_sess.destroy()

    def back():
        root.destroy()

        window.run()

    b_back = functions.create.button(text='Назад', font=('Noto Sans', 20), command=back)
    b_back.place(relx=0.5, rely=1.0, anchor="s", bordermode="outside", y=-100)

    def get_api_data(force=False):
        if force:
            functions.config.remove_option('GENERAL', 'API_ID')
            functions.config.remove_option('GENERAL', 'API_HASH')
            functions.config.write(open(f'{functions.path}/config.ini', 'w', encoding='UTF-8'))

        def ready_to_save_api_id_and_api_hash():
            b_ready.destroy()
            functions.config['GENERAL']['API_ID'] = EntryApi_Id.get()
            functions.config['GENERAL']['API_HASH'] = EntryApi_Hash.get()
            functions.config.write(open(f'{functions.path}/config.ini', 'w', encoding='UTF-8'))

            LabelApi_Id.destroy()
            LabelApi_Hash.destroy()
            EntryApi_Id.destroy()
            EntryApi_Hash.destroy()

            ready.set(1)

        def check_data():
            if EntryApi_Id.get() != '' and not (' ' in EntryApi_Id.get()) and EntryApi_Hash.get() != '' and not (
                    ' ' in EntryApi_Hash.get()):
                return 1

            return 0

        if (not functions.config.has_option('GENERAL', 'API_ID') or
                not functions.config.has_option('GENERAL', 'API_HASH')):
            (LabelApi_Id := tk.Label(text='Введите ваш API_ID')).pack()
            (EntryApi_Id := tk.Entry()).pack()
            (LabelApi_Hash := tk.Label(text='Введите ваш API_HASH: ')).pack()
            (EntryApi_Hash := tk.Entry()).pack()

        if (not functions.config.has_option('GENERAL', 'API_HASH') and
                not functions.config.has_option('GENERAL', 'API_ID')):
            while True:
                if check_data():
                    break

                root.update()

            ready = tk.IntVar(value=0)
            b_ready = tk.Button(text='Готово', background="#242424",
                                foreground="white", font=('Arial', 10),
                                command=ready_to_save_api_id_and_api_hash)
            b_ready.pack()

            root.wait_variable(ready)

    get_api_data()

    def get_phone_and_name_data():
        # Определение имени сессии
        LabelNameSess = tk.Label(text='Введите имя для вашей сессии')
        LabelNameSess.pack(pady=(50, 0))
        EntryNameSess = tk.Entry()
        EntryNameSess.pack()

        # Определение номера телефона
        LabelPhoneNumber = tk.Label(text='Введите ваш номер телефона')
        LabelPhoneNumber.pack(pady=(50, 0))
        EntryPhoneNumber = tk.Entry()
        EntryPhoneNumber.pack()

        def check_name():
            if len(EntryNameSess.get()) != 0:
                LabelNameSess.configure(text='Всё ок')
                return 1
            return 0

        def check_phone():

            if len(EntryPhoneNumber.get()) >= 12 and EntryPhoneNumber.get().startswith('+'):
                LabelPhoneNumber.configure(text='Номер похож на валидный')
                return 1
            return 0

        ready = tk.IntVar(value=0)

        l_country_icon = functions.create.label(master=root, bg=dynamic_config.bg)
        l_country_icon.pack(before=EntryPhoneNumber)

        while True:
            if functions.method.get_image_country(EntryPhoneNumber.get()):
                image = Image.open(functions.method.get_image_country(EntryPhoneNumber.get()))
                image = image.resize((image.width // 5, image.height // 5))
                photo = ImageTk.PhotoImage(image)

                l_country_icon.configure(image=photo)

            else:
                l_country_icon.configure(image=None)

            if check_name() and check_phone():
                break
            root.update()

        bReady = tk.Button(text='Готово', background="#242424",
                           foreground="white", font=('Arial', 10),
                           command=lambda: ready.set(1))
        bReady.pack()

        root.wait_variable(ready)

        bReady.destroy()

        x = EntryPhoneNumber.get(), EntryNameSess.get()
        LabelPhoneNumber.destroy()
        EntryPhoneNumber.destroy()
        LabelNameSess.destroy()
        EntryNameSess.destroy()

        return x

    phone_and_name_data = get_phone_and_name_data()
    phone = phone_and_name_data[0]
    name_sess = phone_and_name_data[1]

    app = functions.create.client(name_sess)

    app.connect()

    while True:
        try:
            sent_code_info = app.send_code(phone).phone_code_hash
            break
        except pyrogram.errors.exceptions.bad_request_400.ApiIdInvalid:
            (LabelApi_IdIsInvalid := tk.Label(text='API_ID или API_HASH некорректные! Введите их ещё раз')).pack()
            get_api_data(force=True)
            LabelApi_IdIsInvalid.destroy()

        except pyrogram.errors.exceptions.not_acceptable_406.PhoneNumberInvalid:
            (LabelPhoneNumberIsInvalid := tk.Label(text='Номера телефона не обнаружено в базе данных Telegram!')).pack()
            phone_and_name_data = get_phone_and_name_data()
            phone = phone_and_name_data[0]
            name_sess = phone_and_name_data[1]
            LabelPhoneNumberIsInvalid.destroy()

    try:

        while True:
            try:
                LabelCodeWasSent = tk.Label(text='Код был выслан!')
                LabelCodeWasSent.pack()
                EntryYourCode = tk.Entry()
                EntryYourCode.pack()
                bReady = tk.Button(text='Готово', background="#242424",
                                   foreground="white", font=('Arial', 10), command=lambda: ready.set(1))
                bReady.pack()
                ready = tk.IntVar(value=0)

                root.wait_variable(ready)
                code = EntryYourCode.get()
                app.sign_in(phone, sent_code_info, code)

                break
            except pyrogram.errors.exceptions.bad_request_400.PhoneCodeInvalid:
                if 'LabelCodeIsInvalid' in locals():
                    LabelCodeIsInvalid.destroy()
                else:
                    (LabelCodeIsInvalid := tk.Label(text='Код неверный!')).pack()

            finally:
                EntryYourCode.destroy()
                LabelCodeWasSent.destroy()
                bReady.destroy()

    except pyrogram.errors.exceptions.bad_request_400.PhoneNumberInvalid:
        (LabelPhoneNumberIsInvalid := tk.Label(text='Номер телефона неверный! Введите его ещё раз')).pack()
        get_phone_and_name_data()

    except pyrogram.errors.exceptions.unauthorized_401.SessionPasswordNeeded:
        (LabelPasswordRequired := tk.Label(text='У вас есть пароль! Введите его')).pack()
        EntryPassword = tk.Entry()
        EntryPassword.pack()

        LabelPasswordIsInvalid = tk.Label(text='Пароль неверный')
        bReady = tk.Button(text='Готово', background="#242424",
                           foreground="white", font=('Arial', 10), command=lambda: ready.set(1))
        bReady.pack()
        while True:
            try:
                ready = tk.IntVar(value=0)
                LabelPasswordIsInvalid.destroy()
                root.wait_variable(ready)
                app.check_password(EntryPassword.get())
                break
            except pyrogram.errors.exceptions.bad_request_400.PasswordHashInvalid:
                (LabelPasswordIsInvalid := tk.Label(text='Пароль неверный')).pack()

    (LabelCodeSuccess := tk.Label(text='Успешно!')).pack()
    app.disconnect()
