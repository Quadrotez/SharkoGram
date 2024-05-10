class ArgsInfoScriptError(Exception):
    def __init__(self, message="Please give only one argument"):
        self.message = message
        super().__init__(self.message)


class BadStringError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(self.message)


class BadReflexCommandError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(self.message)
