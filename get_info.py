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

@query
def get_all_purchases(cursor, conn):
    cursor.execute(
        """
        SELECT p.id, p.date, p.payer, s.name AS shop_name, l.name AS location_name,
               pr.name AS product_name, pr.price, pr.amount, pr.flag
        FROM purchase p
        JOIN shop s ON s.id = p.shop_id
        JOIN location l ON l.name = s.location
        LEFT JOIN product pr ON pr.purchase_id = p.id
        ORDER BY p.id DESC, pr.id ASC;
        """
    )
    rows = cursor.fetchall()

    purchases = {}
    for row in rows:
        purchase_id, purchase_date, payer, shop_name, location_name, product_name, price, amount, flag = row

        if purchase_id not in purchases:
            purchases[purchase_id] = {
                'id': purchase_id,
                'date': purchase_date.isoformat() if purchase_date else None,
                'payer': payer,
                'shop': shop_name,
                'location': location_name,
                'products': []
            }

        if product_name is not None:
            purchases[purchase_id]['products'].append({
                'name': product_name,
                'price': float(price) if price is not None else None,
                'amount': float(amount) if amount is not None else None,
                'flag': flag
            })

    return list(purchases.values())
 