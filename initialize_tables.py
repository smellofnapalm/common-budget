from utils import query

@query
def create_enums(cursor, conn):
    cursor.execute("CREATE TYPE product_status AS ENUM ('common', 'mine', 'other');")
    cursor.execute("CREATE TYPE person AS ENUM ('Misha', 'Masha');")
    conn.commit()

@query
def create_location_table(cursor, conn):
    cursor.execute("CREATE TABLE IF NOT EXISTS location (name VARCHAR(50) PRIMARY KEY);")
    conn.commit()

@query
def create_shop_table(cursor, conn):
    cursor.execute("CREATE TABLE IF NOT EXISTS shop (id SERIAL PRIMARY KEY, name VARCHAR(50), location VARCHAR(50) REFERENCES location(name));")
    conn.commit()

@query
def create_purchase_table(cursor, conn):
    cursor.execute("CREATE TABLE IF NOT EXISTS purchase (id SERIAL PRIMARY KEY, shop_id INTEGER REFERENCES shop(id), date DATE, payer person);")
    conn.commit()

@query
def create_product_table(cursor, conn):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS product (id SERIAL PRIMARY KEY, " \
        "name VARCHAR(50), price FLOAT, amount FLOAT, " \
        "purchase_id INTEGER REFERENCES purchase(id), flag product_status);"
    )
    conn.commit()

def initialize():
    create_enums()
    create_location_table()
    create_shop_table()
    create_purchase_table()
    create_product_table()
    print("База данных инициализирована")
