import functions
import reflex

try:
    reflex.Reflex(f'{functions.path}/reflex/main.rx').run(app=functions.create.client(input('Введите имя сессии: ')))
except Exception as e:
    print(f'{e}\nView documentation on https://github.com/Quadrotez/SharkoGram/blob/master/doc/reflex.MD')
finally:
    input()