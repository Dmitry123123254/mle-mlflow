import psycopg

# Параметры подключения к первой базе данных (источник)
source_connection = {
    "sslmode": "require",
    "target_session_attrs": "read-write",
    "host": "rc1b-uh7kdmcx67eomesf.mdb.yandexcloud.net",
    "port": "6432",
    "dbname": "playground_common",
    "user": "mle_ro",
    "password": "HI&ykgu6tj"
}

# Параметры подключения ко второй базе данных (назначение)
dest_connection = {
    "sslmode": "require",
    "target_session_attrs": "read-write",
    "host": "rc1b-uh7kdmcx67eomesf.mdb.yandexcloud.net",
    "port": "6432",
    "dbname": "playground_mle_20250130_d1608e0ec6",
    "user": "mle_20250130_d1608e0ec6",
    "password": "99cb8518297b4f07b5e878da37beafc5"
}

# SQL-запрос для получения первых 10 строк таблицы users_churn
users_churn_data_query = """
SELECT * FROM users_churn LIMIT 10;
"""

# Функция для получения первых 10 строк таблицы users_churn
def show_users_churn_data(db_connection, db_name):
    print(f"\nПервые 10 строк витрины users_churn в базе данных {db_name}:")
    try:
        with psycopg.connect(**db_connection) as conn:
            with conn.cursor() as cur:
                cur.execute(users_churn_data_query)
                rows = cur.fetchall()
                # Получаем имена колонок
                col_names = [desc[0] for desc in cur.description]
                # Печатаем заголовки
                print(" | ".join(col_names))
                print("-" * len(" | ".join(col_names)))
                # Печатаем данные
                for row in rows:
                    print(" | ".join(str(value) for value in row))
    except Exception as e:
        print(f"Ошибка при подключении к базе данных {db_name}: {e}")

# Получаем первые 10 строк витрины users_churn из обеих баз данных
show_users_churn_data(source_connection, "source")
show_users_churn_data(dest_connection, "destination")