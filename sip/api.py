from iota.api import Object
from .register import SerialEvalRegister

state = {}

def set_port(newPort):
    state["register"] = SerialEvalRegister.allocate_zero(newPort)

def eval(*e):
    se = Object.from_python_to_expression(list(e))
    i_data = se.to_bytes()
    register = state["register"]
    register.load_i(i_data)
    register.eval()
    r_data = register.retrieve_r()
    (result, rest) = Object.from_bytes(r_data)
    if len(rest) > 0:
        raise Exception("bad decode, %d bytes leftover" % len(rest))
    else:
        return Object.to_python(result)

def evalNoun(*e):
    se = Object.from_python(list(e)[0])
    i_data = se.to_bytes()
    register = state["register"]
    register.load_i(i_data)
    register.eval()
    r_data = register.retrieve_r()
    (result, rest) = Object.from_bytes(r_data)
    if len(rest) > 0:
        raise Exception("bad decode, %d bytes leftover" % len(rest))
    else:
        return Object.to_python(result)
