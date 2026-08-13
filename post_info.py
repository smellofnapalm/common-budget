from utils import query

# Загружаем новую покупку в базу данных
# При необходимости будут вставлены все необходимые промежуточные данные (локация, магазин)
# Для покупки мы перечисляем (name, price, amount, flag)
@query
def post_new_purchase(
        cursor,
        conn,
        payer: str,
        shop_name: str,
        shop_location: str,
        date: str,
        buyings: list[tuple[str, float, float, str]]
):
    # Вставляем локацию, если ее еще нет
    cursor.execute("SELECT * FROM location WHERE name = %s LIMIT 1;", (shop_location,))
    res = cursor.fetchone()
    if not res:
        cursor.execute("INSERT INTO location (name) VALUES (%s);", (shop_location,))
        print(f"Добавили локацию {shop_location}")

    # Вставляем магазин в базу, если его еще нет
    cursor.execute("SELECT id FROM shop WHERE name = %s AND location = %s LIMIT 1;", 
                   (shop_name, shop_location))
    res = cursor.fetchone()
    if not res:
        cursor.execute("INSERT INTO shop (name, location) VALUES (%s, %s) RETURNING id;", (shop_name, shop_location))
        res = cursor.fetchone()
        print(f"Добавили новый магазин {shop_name} в локации {shop_location}")
    res = res[0]

    # Добавляем новую покупку в базу
    cursor.execute("INSERT INTO purchase (shop_id, date, payer) VALUES (%s, to_date(%s,'DD/MM/YYYY'), cast(%s AS person)) RETURNING id;", (res, date, payer))
    res = cursor.fetchone()[0]
    print(f"Добавили новую покупку с id = {res}")

    # Добавляем конкретные продукты теперь
    # Добавим purchase_id к кортежу
    buyings = [(x[0], x[1], x[2], x[3], res) for x in buyings]
    cursor.executemany("INSERT INTO product (name, price, amount, flag, purchase_id) VALUES (%s, %s, %s, %s, %s);", buyings)
    print(f"Добавили новые продукты {buyings}")
    conn.commit()

    return res
