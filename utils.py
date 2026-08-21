from os import getenv
from dotenv import load_dotenv
import psycopg2 as psql

load_dotenv()

# Подгружаем конфиг из .env
class Config:
    DB_NAME = getenv('DB_NAME')
    DB_USER = getenv('DB_USER')
    DB_HOST = getenv('DB_HOST')
    DB_PASSWORD = getenv('DB_PASSWORD')
    DB_PORT = getenv('DB_PORT')

# Получаем подключение к БД
def get_connection():
    print(Config.__dict__)
    return psql.connect(
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
        )

# Получаем курсор
def get_cursor(conn):
    return conn.cursor()

# Удобная объединенная функция
def get_cursor_and_connection():
    conn = get_connection()
    cursor = get_cursor(conn)
    return cursor, conn

# Удобное закрывание
def close_connection(cursor, conn):
    cursor.close()
    conn.close()

# Декоратор, чтобы не писать лишний раз весь этот дежурный код при выполнении запроса
def query(func):
    def wrapper(*args, **kwargs):
        result = None  
        try:
            cursor, conn = get_cursor_and_connection()
            print('Подлючились к базе данных')
            result = func(cursor, conn, *args, **kwargs)
        except Exception as e:
            print(f"Ошибка при подключении к БД: {e}")
        finally:
            print('Все хорошо, сейчас закроем подключение')
            if conn:
                close_connection(cursor, conn)
        return result
    return wrapper
