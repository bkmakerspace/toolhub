import ast

import environ


class Env(environ.Env):
    def __init__(self, path=None, **schema):
        super(Env, self).__init__(**schema)
        if path:
            self.read_env(path)

    def eval(self, var, cast=None, default=environ.Env.NOTSET):
        value = self.str(var, default=None)
        if value is None:
            value = default
        else:
            value = ast.literal_eval(value)
        if cast:
            value = cast(value)
        return value
