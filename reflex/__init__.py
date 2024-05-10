import reflex.errors
import reflex.interpretator


class Reflex:
    def __init__(self, file_path=None, strings: str | list[str] = None, encoding='UTF-8',
                 string: str = None):

        if (int(bool(file_path)) + int(bool(strings)) + int(bool(string))) > 1:
            raise reflex.errors.ArgsInfoScriptError

        if string:
            string = string.split('\n')


        self.string = string
        self.file_path = file_path
        self.encoding = encoding
        self.strings = strings

    def run(self, app=None):
        reflex.interpretator.run(
            [i for i in (open(self.file_path, 'r', encoding=self.encoding))] if self.file_path else (self.strings if
                                                                                                     self.strings else
                                                                                                     self.string),
            app=app if app else None)
