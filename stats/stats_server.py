import sqlite3
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = SimpleXMLRPCServer(("localhost", 8009),
                            requestHandler=RequestHandler,
                            allow_none=False)


# Добавление строки в лог
def add_to_db(sname, date, func_duration):
    try:
        sqlite_connection = sqlite3.connect('/Users/alexeychuyko/PycharmProjects/pythonProject1/db/log.db')
        cursor = sqlite_connection.cursor()
        print("Подключение к SQLite выполнено успешно")
        stats = (sname, date, func_duration)
        cursor.execute("""INSERT INTO log
                              (OPERATION_TYPE, DATE, OPERATION_DURATION)
                              VALUES
                              (?, ?, ?);""", stats)
        sqlite_connection.commit()
        print("Запись успешно вставлена в таблицу log ", cursor.rowcount)
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return True


server.register_function(add_to_db, 'add_to_db')

print("Listening on port 8009...")
server.serve_forever()
