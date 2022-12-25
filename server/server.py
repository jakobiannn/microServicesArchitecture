import datetime
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = SimpleXMLRPCServer(("localhost", 8008),
                            requestHandler=RequestHandler,
                            allow_none=True)
server.register_introspection_functions()


# Тест
def ping():
    return True


server.register_function(ping, 'ping')


# Время сервера
def now():
    return datetime.datetime.now()


server.register_function(now, 'now')


# Отображение строкового вида, типа и значений
def show_type(arg):
    return str(arg), str(type(arg)), arg


server.register_function(show_type, 'operation_type')


# Сумма
def two_sum(a, b):
    return a + b


server.register_function(two_sum, 'two_sum')


# Степень
def two_pow(a, b):
    return a ** b


server.register_function(two_pow, 'two_pow')

print("Listening on port 8008...")
server.serve_forever()
