import datetime
import time
import xmlrpc
from xmlrpc import client
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = SimpleXMLRPCServer(("localhost", 8008),
                            requestHandler=RequestHandler,
                            allow_none=False)
server.register_introspection_functions()

proxy = xmlrpc.client.ServerProxy("http://localhost:8018")


def collect_stat(f):
    def tmp(*args, **kwargs):
        start_time = time.time()
        res = f(*args, **kwargs)
        add_log(f.__name__, time.time() - start_time)
        print("Время выполнения функции: %s" % (time.time() - start_time))
        return res
    return tmp


# Добавление в лог через сервер
def add_log(log_line, func_duration):
    proxy.add_log(log_line, func_duration)
    return True


# Тест
@collect_stat
def ping():
    return True


server.register_function(ping, 'ping')


# Время сервера
@collect_stat
def now():
    return datetime.datetime.now()


server.register_function(now, 'now')


# Отображение строкового вида, типа и значений
@collect_stat
def show_type(arg):
    return str(arg), str(type(arg)), arg


server.register_function(show_type, 'operation_type')


# Сумма
@collect_stat
def two_sum(a, b):
    return a + b


server.register_function(two_sum, 'sum')


# Степень
@collect_stat
def two_pow(a, b):
    return a ** b


server.register_function(two_pow, 'pow')

print("Listening on port 8008...")
server.serve_forever()
