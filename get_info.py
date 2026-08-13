from utils import query

@query
def get_all_locations(cursor, conn):
    cursor.execute('SELECT * FROM location;')
    result = cursor.fetchall()
    if result:
        return [row[0] for row in result]
    return None

@query
def get_all_products(cursor, conn):
    cursor.execute('SELECT name, price, amount, purchase_id, flag FROM product;')
    result = cursor.fetchall()
    return result
