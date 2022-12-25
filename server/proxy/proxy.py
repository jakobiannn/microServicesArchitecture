import datetime
import time
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import sqlite3


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


proxy = SimpleXMLRPCServer(("localhost", 8000),
                           requestHandler=RequestHandler, allow_none=True)

stats_server = xmlrpc.client.ServerProxy("http://localhost:8009")
server = xmlrpc.client.ServerProxy("http://localhost:8008")


# Добавление в лог через сервер
def add_log(sname, func_duration):
    stats_server.add_to_db(sname, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           "{:.12f}".format(func_duration))
    return True


# декоратор для логирования длительности/названия функции
def collect_stat(f):
    def tmp(*args, **kwargs):
        start_time = time.time()
        res = f(*args, **kwargs)
        add_log(f.__name__, time.time() - start_time)
        print("Время выполнения функции: %s" % (time.time() - start_time))
        return res

    return tmp


# Тест
@collect_stat
def ping():
    return server.ping()


proxy.register_function(ping, 'ping')


# Время сервера
@collect_stat
def now():
    return server.now()


proxy.register_function(now, 'now')


# Отображение строкового вида, типа и значений
@collect_stat
def show_type(arg):
    return server.operation_type(arg)


proxy.register_function(show_type, 'operation_type')


# Сумма
@collect_stat
def two_sum(a, b):
    return server.two_sum(a, b)


proxy.register_function(two_sum, 'sum')


# Степень
# @collect_stat
def two_pow(a, b):
    return server.two_pow(a, b)


proxy.register_function(two_pow, 'pow')


def execute_db_query(query, params):
    result = []
    try:
        sqlite_connection = sqlite3.connect('/Users/alexeychuyko/PycharmProjects/pythonProject1/db/log.db')
        cursor = sqlite_connection.cursor()
        print("Подключение к SQLite выполнено успешно")
        cursor.execute(query, params)
        result = cursor.fetchall()
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return result


def get_stats_by_date(start_date, end_date):
    query = """select * from log WHERE datetime(DATE) between datetime(?) AND datetime(?);"""
    return execute_db_query(query, (start_date, end_date,))


proxy.register_function(get_stats_by_date, 'get_stats_by_date')


def get_stats_by_type(operation_type):
    query = """select * from log where OPERATION_TYPE is ?;"""
    return execute_db_query(query, (operation_type,))


proxy.register_function(get_stats_by_type, 'get_stats_by_type')


def get_stats_by_duration(first_dur, second_dur):
    query = """select * from log WHERE OPERATION_DURATION between ? AND ?;"""
    return execute_db_query(query, (first_dur, second_dur,))


proxy.register_function(get_stats_by_duration, 'get_stats_by_duration')


print("Listening on port 8000...")
proxy.serve_forever()
