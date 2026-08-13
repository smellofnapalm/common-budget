from utils import query

@query
def drop_all(cursor, conn):
    cursor.execute("DROP TABLE product;")
    cursor.execute("DROP TABLE purchase;")
    cursor.execute("DROP TABLE shop;")
    cursor.execute("DROP TABLE location;")
    conn.commit()
    