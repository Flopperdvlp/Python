import sqlite3

def main():
    connection_string = "Zoo_Store.db"
    with sqlite3.connect(connection_string) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")
        create_tables(connection)
        insert_tables(connection)
        show(connection)
        update_tables(connection)
        show(connection) 

#*----------------------------------
def create_tables(connection):
    create_products_table = """
        CREATE TABLE IF NOT EXISTS Products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            category_id INT,
            price DECIMAL(10, 2),
            stock_quantity INT,
            description TEXT,
            supplier_id INT,
            FOREIGN KEY (category_id) REFERENCES Categories(id),
            FOREIGN KEY (supplier_id) REFERENCES Suppliers(id)
        );
    """
    create_categories_table = """
        CREATE TABLE IF NOT EXISTS Categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            description TEXT
        );
    """
    create_suppliers_table = """
        CREATE TABLE IF NOT EXISTS Suppliers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            phone_number VARCHAR(20),
            email VARCHAR(100),
            address TEXT
        );
    """
    create_customers_table = """
        CREATE TABLE IF NOT EXISTS Customers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            phone_number VARCHAR(20),
            email VARCHAR(100),
            address TEXT
        );
    """
    create_orders_table = """
        CREATE TABLE IF NOT EXISTS Orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INT,
            order_date DATE,
            total_price DECIMAL(10, 2),
            status VARCHAR(50),
            FOREIGN KEY (customer_id) REFERENCES Customers(id)
        );
    """
    with connection:
        connection.execute(create_products_table)
        connection.execute(create_categories_table)
        connection.execute(create_suppliers_table)
        connection.execute(create_customers_table)
        connection.execute(create_orders_table)
#*----------------------------------
def insert_tables(connection):
    try:
        # Включение транзакции
        with connection:
            # Вставка данных для таблицы Categories
            insert_categories = """
                INSERT INTO Categories (name, description)
                VALUES (?, ?);
            """
            categories_data = [
                ("Food", "Продукты для питания животных"),
                ("Toys", "Игрушки для животных"),
                ("Accessories", "Аксессуары для животных, например, поводки и ошейники"),
            ]
            for category in categories_data:
                connection.execute(insert_categories, category)

            # Вставка поставщиков
            insert_suppliers = """
                INSERT INTO Suppliers (name, phone_number, email, address)
                VALUES (?, ?, ?, ?);
            """
            suppliers_data = [
                ("Supplier A", "123-456-7890", "contact@suppliera.com", "123 Supplier St, City"),
                ("Supplier B", "098-765-4321", "contact@supplierb.com", "456 Supplier Ave, City"),
            ]
            for supplier in suppliers_data:
                connection.execute(insert_suppliers, supplier)

            # Вставка продуктов
            insert_products = """
                INSERT INTO Products (name, category_id, price, stock_quantity, description, supplier_id)
                VALUES (?, ?, ?, ?, ?, ?);
            """
            products_data = [
                ("Dog Food", 1, 20.99, 50, "Высококачественный корм для собак.", 1),
                ("Cat Toy", 2, 5.99, 100, "Игрушка для кошек.", 2),
                ("Pet Leash", 3, 10.50, 75, "Прочный поводок для животных.", 1),
            ]
            for product in products_data:
                connection.execute(insert_products, product)

            # Вставка заказов
            insert_orders = """
                INSERT INTO Orders (customer_id, order_date, total_price, status)
                VALUES (?, ?, ?, ?);
            """
            orders_data = [
                (1, "2024-10-17", 26.98, "Completed"),
                (2, "2024-10-16", 16.49, "Pending"),
            ]
            for order in orders_data:
                connection.execute(insert_orders, order)

    except sqlite3.IntegrityError as e:
        print(f"Ошибка целостности данных: {e}")

#*----------------------------------
def show(connection):
    tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")
        
        rows = connection.execute(f"SELECT * FROM {table_name};").fetchall()
        for row in rows:
            print(row)
        print("-" * 50)
#*----------------------------------
def update_tables(connection):
    update_table = """
        UPDATE Products
        SET price = 100.00
        WHERE name = 'Dog Food';
    """
    with connection:
        connection.execute(update_table)
    print("Дані успішно оновлено.")
#*----------------------------------
if __name__ == "__main__":
    main()