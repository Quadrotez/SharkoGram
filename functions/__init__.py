from configparser import ConfigParser

import os

import functions.method
import functions.create
import functions.win
import functions.data
import functions.gen_long_strings

(lambda x: (os.mkdir(x) if not os.path.exists(x) else '',
            open(f'{x}/config_dyn.ini', 'w', encoding='UTF-8').write('') if not os.path.exists(
                f'{x}/config_dyn.ini') else '',
            open(f'{x}/config.ini', 'w', encoding='UTF-8').write('') if not os.path.exists(f'{x}/config.ini') else '',
            open(f'{x}/config_proxy.ini',
                 'w', encoding='UTF-8').write('') if not os.path.exists(f'{x}/config_proxy.ini') else '',
            os.mkdir(f'{path}/sessions') if not os.path.exists(f'{path}/sessions') else ''))(
    path := f'{os.getenv("APPDATA")}/SharkoGram')

# Создание динамического конфига
(config_dyn_2 := ConfigParser()).read(f'{path}/config_dyn.ini', encoding='UTF-8')

(((lambda cd: (cd.add_section('DYN') if not cd.has_section('DYN') else '',
               cd.write(open(f'{path}/config_dyn.ini', 'w', encoding='UTF-8')))))
 (config_dyn_2))

# Создание статического конфига
(config := ConfigParser()).read(f'{path}/config.ini')

(((lambda c: (c.add_section('GENERAL') if not c.has_section('GENERAL') else '',
              c.write(open(f'{path}/config.ini', 'w', encoding='UTF-8')))))
 (config))

# Инициализация всех файлов для стеганографии
(lambda: (os.mkdir(f'{path}/stego_cache') if not os.path.exists(f'{path}/stego_cache') else '',
          os.mkdir('downloads') if not os.path.exists('downloads') else ''))()

# Инициализация Proxy-конфига
(config_proxy := ConfigParser()).read(f'{path}/config_proxy.ini')
(lambda: ((config_proxy.add_section('DEFAULTIO'),
           config_proxy.write(open(f'{path}/config_proxy.ini', 'w',
                                   encoding='UTF-8'))) if not config_proxy.has_section('DEFAULTIO') else ''))()

# Инициализация reflex
(lambda: (os.mkdir(f'{path}/reflex') if not os.path.exists(f'{path}/reflex') else ''))()