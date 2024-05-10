import cryptography.exceptions
import requests
from cryptography.fernet import Fernet
from stegano import lsb

path = None


def encrypt(text, key):
    response = requests.get('https://source.unsplash.com/random/200x300')
    with open(f'{path}/stego_cache/base.png', 'wb') as file:
        file.write(response.content)
    try:
        secret = lsb.hide(f'{path}/stego_cache/base.png',
                          str(Fernet(bytes(key[2:-1], 'utf-8')).encrypt(text.encode('UTF-8'))),
                          encoding='UTF-8')
    except Exception:
        secret = lsb.hide(f'{path}/stego_cache/base.png',
                          str(Fernet(bytes(key[2:-1], 'utf-8')).encrypt(f'Текст для шифрования'
                                                                        f'слишком длинный: {len(text)}'.encode('UTF-8')
                                                                        )),
                          encoding='UTF-8')

    secret.save(f"{path}/stego_cache/encrypted.png")

    return f"{path}/stego_cache/encrypted.png"


def decrypt(key, local_path=None):
    try:
        return Fernet(bytes(key[2:-1],
                            'utf-8')).decrypt(eval(lsb.reveal(local_path, encoding='UTF-8'))).decode('UTF-8')
    except cryptography.exceptions.InvalidSignature:
        return 'Не удалось считать данные. Проверьте правильность ключа'


def gen_key():
    return Fernet.generate_key()
