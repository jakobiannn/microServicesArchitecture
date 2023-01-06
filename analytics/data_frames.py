from sqlite3 import connect
import pandas as pd


def load_count_by_type():
    conn = connect('db/log.db')
    df_raw = pd.read_sql(
        'SELECT OPERATION_TYPE as TYPE, count(OPERATION_TYPE) as COUNT FROM log GROUP BY OPERATION_TYPE;',
        con=conn
    )
    return df_raw


def load_count_by_time(df):
    conn = connect('db/log.db')
    operations = [
        'show_type',
        'two_sum',
        'two_pow',
        'ping',
        'now',
    ]
    operation = df['proc_type'][0]
    if operation in operations:
        df_raw = pd.read_sql(
            f'SELECT STRFTIME(\'%H\', DATE) AS HOUR, count(OPERATION_TYPE) as COUNT FROM log WHERE OPERATION_TYPE = \'{operation}\' GROUP BY DATE;',
            con=conn
        )
        df_raw = df_raw.loc[(df_raw['HOUR'].astype(int) < df['interval_width'][0])]
    else:
        df_raw = pd.read_sql(
            f'SELECT STRFTIME(\'%H\', DATE) AS HOUR, count(OPERATION_TYPE) as COUNT FROM log GROUP BY DATE;',
            con=conn
        )
        df_raw = df_raw.loc[(df_raw['HOUR'].astype(int) < df['interval_width'][0])]
    return df_raw


def log_avg_duration():
    conn = connect('db/log.db')
    df_raw = pd.read_sql(
        f'SELECT OPERATION_TYPE AS TYPE, avg(OPERATION_DURATION) as DURATION FROM log GROUP BY OPERATION_TYPE;',
        con=conn
    )
    return df_raw
