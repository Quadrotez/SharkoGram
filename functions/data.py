import functions


def save():
    with open(f'{functions.path}/config_dyn.ini', 'w', encoding='UTF-8') as f:
        functions.config_dyn_2.write(f)


def add(name, var):
    functions.config_dyn_2['DYN'][str(name)] = str(var)
    save()


def get(name):
    return functions.config_dyn_2['DYN'][str(name)]
