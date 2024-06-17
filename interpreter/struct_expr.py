from .lambda_expr import *

class StructExpression(InterpretedExpression):
    def __init__(self, body):
        self.body = body

    def eval(self, env):
        env1 = Enviroment()
        env1.set_parent(env)
        for (id, e) in self.body:
            v, env1 = e.eval(env1)
            dict.__setitem__(env1, id, v)  # add value to this level of dict
        return (env1.get_vals(), env)  # return the enviroment WITHOUT parent

class StructMemberAccessExpression(InterpretedExpression):
    def __init__(self, s, dots, id):
        self.s = s
        self.n_dots = len(dots)
        self.id = id

    def eval(self, env):
        env1 = env[self.s]
        for _ in range(self.n_dots-1):
            if env1.get_parent() is None:
                raise Exception(f'Not enough inheritance layers: {self.n_dots}')
            env1 = env1.get_parent()
        m = env1[self.id]
        return (m, env)

class StructExtendExpression(InterpretedExpression):
    def __init__(self, s, body):
        self.s = s
        self.body = body

    def eval(self, env):
        env1 = Enviroment()
        env1.set_parent(env[self.s])
        for (id, e) in self.body:
            v, env1 = e.eval(env1)
            dict.__setitem__(env1, id, v)  # add value to this level of dict
        return (env1, env)  # return the enviroment WITH parent