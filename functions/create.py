import tkinter as tk, dynamic_config, functions, threading, asyncio
from pyrogram import Client
from tkinter import ttk

style = {
    'button': {
        'bg': '#242424',
        'font': ('Arial', 10),
        'foreground': 'white'
    },
    'label': {
        'bg': '#6e6e6e',
        'fg': '#000'},

    'entry': {'bg': '#919191',
              'fg': '#000'},

    'label_message': {
        'bg': '#1f1f1f',
        'fg': '#e8e8e8',
    },

    'progress_bar':
        {
            'orient': tk.HORIZONTAL

        },

    'text_editor':
        {
            'bg': '#141414',
            'fg': '#c9c9c9',
            'font': ('Terminal', 10),
            'width': 150,
            'height': 60
        },

    'frame':
        {
            'bg': '#141414'
        }

}


# text='Готово', background="",
#                            foreground="white", font=('Arial', 10), command=lambda: ready.set(1)
def button(master=None, **kwargs):
    button = tk.Button(master=master if master else None)
    button.configure(**style['button'])

    button.configure(**kwargs)
    return button


def label(master=None, local_style=None, **kwargs):
    label = tk.Label(master=master if master else None)
    label.configure(**style[local_style if local_style else 'label'])

    label.configure(**kwargs)

    return label


def entry(master=None, **kwargs):
    entry = tk.Entry(master=master if master else None)
    entry.configure(**style['entry'])

    entry.configure(**kwargs)

    return entry


def window(geometry=None, title=None):
    root = tk.Tk()
    root.config(bg=dynamic_config.bg)
    root.title(title if title else dynamic_config.title)
    root.geometry(geometry if geometry else functions.win.gen_window_geometry())
    root.iconbitmap('icon.ico')
    return root


def local_destroy(*args):
    result = []

    def flatten(item):
        [flatten(i) for i in item] if isinstance(item, tuple) | isinstance(item, list) else result.append(item)

    [flatten(arg) for arg in args]

    [j.destroy() if j else None for j in result]


def scroll_slider(master=None, args_for_frame: dict = None, width_canvas=200,
                  height_canvas=200, bg='#1a1a1a',
                  side=None, bind=True):
    if args_for_frame and args_for_frame['master'] and not master:

        root = args_for_frame['master']
    else:
        root = master if master else None

    frame = tk.Frame(root, width=1, height=200, bg=bg)
    frame.pack(side=side)

    canvas = tk.Canvas(frame, width=width_canvas, height=height_canvas,
                       bg=bg)
    canvas.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview,
                             bg=bg)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.config(yscrollcommand=scrollbar.set)

    inner_frame = tk.Frame(canvas, bg=bg)

    canvas.create_window(0, 0, anchor=tk.NW, window=inner_frame)

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner_frame.bind("<Configure>", on_frame_configure)

    root.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * int((e.delta / 120)), "units")
                  ) if bind else None

    return inner_frame, scrollbar, canvas, frame


def client(name_sess):
    return Client(f'{functions.path}/sessions/{name_sess}',
                  api_id=functions.config['GENERAL']['API_ID'],
                  api_hash=functions.config['GENERAL']['API_HASH'],
                  device_model='SharkoGram',
                  proxy={'hostname': (section := functions.config_proxy['DEFAULTIO']['MAIN']),
                         'port': int(functions.config_proxy[section]['PORT']),
                         'username': functions.config_proxy[section]['LOGIN'],
                         'password': functions.config_proxy[section]['PASSWORD'],
                         'scheme': functions.config_proxy[section]['CONNECTION_TYPE']
                         } if (functions.config_proxy.has_section('DEFAULTIO')
                               and functions.config_proxy.has_option('DEFAULTIO', 'MAIN')
                               and functions.config_proxy['DEFAULTIO'][
                                   'MAIN'] != '') else None)


def progress_bar(master=None, **kwargs):
    bar = ttk.Progressbar(master=master if master else None)
    bar.configure(**style['progress_bar'])

    bar.configure(**kwargs)

    return bar


def text(master=None, **kwargs):
    text = tk.Text(master=master if master else None)
    text.configure(**style['text_editor'])

    text.configure(**kwargs)

    return text


def frame(master=None, **kwargs):
    frame = tk.Frame(master=master if master else None)
    frame.configure(**style['frame'])

    frame.configure(**kwargs)

    return frame
