from configparser import ConfigParser

import os

import functions.method
import functions.create
import functions.win
import functions.data
import functions.gen_long_strings



functions.method.mkdir_weakly(path := f'{os.getenv("APPDATA")}/SharkoGram',
                              f'{path}/sessions', f'{path}/global_cache')


# Создание динамического конфига
open(f'{path}/config_dyn.ini', 'w', encoding='UTF-8').write('') if not os.path.exists(
    f'{path}/config_dyn.ini') else None
(config_dyn_2 := ConfigParser()).read(f'{path}/config_dyn.ini', encoding='UTF-8')

(((lambda cd: (cd.add_section('DYN') if not cd.has_section('DYN') else '',
               cd.write(open(f'{path}/config_dyn.ini', 'w', encoding='UTF-8')))))
 (config_dyn_2))

# Создание статического конфига
open(f'{path}/config.ini', 'w', encoding='UTF-8').write('') if not os.path.exists(f'{path}/config.ini') else None
(config := ConfigParser()).read(f'{path}/config.ini')

(((lambda c: (c.add_section('GENERAL') if not c.has_section('GENERAL') else '',
              c.write(open(f'{path}/config.ini', 'w', encoding='UTF-8')))))(config))

# Инициализация всех файлов для стеганографии
(lambda: (functions.method.mkdir_weakly(f'{path}/stego_cache', f'downloads')))()

# Инициализация Proxy-конфига
open(f'{path}/config_proxy.ini', 'w', encoding='UTF-8').write('') if not os.path.exists(
    f'{path}/config_proxy.ini') else None
(config_proxy := ConfigParser()).read(f'{path}/config_proxy.ini')
(lambda: ((config_proxy.add_section('DEFAULTIO'),
           config_proxy.write(open(f'{path}/config_proxy.ini', 'w',
                                   encoding='UTF-8'))) if not config_proxy.has_section('DEFAULTIO') else '',
          (config_proxy.set('DEFAULTIO', 'MAIN', ''),
           config_proxy.write(open(f'{path}/config_proxy.ini', 'w',
                                   encoding='UTF-8'))) if not config_proxy.has_option(
              'DEFAULTIO', 'MAIN') else ''))()

# Инициализация reflex
functions.method.mkdir_weakly(f'{path}/reflex')
