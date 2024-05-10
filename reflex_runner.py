import functions
import reflex

reflex.Reflex(f'{functions.path}/reflex/main.rx').run(app=functions.create.client(input('Введите имя сессии: ')))
