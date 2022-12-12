import sqlite3


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


def get_stats_by_type(operation_type):
    query = """select * from log where OPERATION_TYPE is ?;"""
    return execute_db_query(query, (operation_type,))


def get_stats_by_duration(first_dur, second_dur):
    query = """select * from log WHERE OPERATION_DURATION between ? AND ?;"""
    return execute_db_query(query, (first_dur, second_dur,))
