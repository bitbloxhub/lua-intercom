import sys
import copy
import json
import lupa
import sanic

__version__ = '0.1.0'

lenv = lupa.LuaRuntime(unpack_returned_tuples=True, register_builtins=False, register_eval=False)
lenv.execute("""
os = nil
io = nil
dofile = nil
require = nil
""")

db = {}
with open(sys.argv[2], "r") as f:
    db = json.load(f)

intercom_functions = {}

luaify = lenv.eval("function(nm, f) _G[nm] = f end")

def add_function(name, function):
    intercom_functions[name] = function

def run_function(name, arguments):
    return intercom_functions[name](arguments)

def list_functions():
    return list(intercom_functions.keys())

def save_db():
    with open(sys.argv[2], "w") as f:
        json.dump(db, f)

def get_db(key):
    return db[key]

def set_db(key, value):
    db[key] = value
    save_db()


luaify("add_function", add_function)
luaify("run_function", run_function)
luaify("list_functions", list_functions)
luaify("get_db", get_db)
luaify("set_db", set_db)

intercom_src = ""
with open(sys.argv[1], "r") as f:
    intercom_src = "\n".join(f.readlines())
lenv.execute(intercom_src)

app = sanic.Sanic("Lua intercom server")

app.config.DEBUG = False

@app.get("/", error_format="json")
async def rq_list(request):
    return sanic.response.json(list_functions())

@app.post("/function/<name:slug>", error_format="json")
async def rq_call(request, name):
    return sanic.response.json(run_function(name, request.json))