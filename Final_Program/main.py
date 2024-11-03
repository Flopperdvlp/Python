import sqlite3

def main():
    connection_string = "CRM.db"
    try:
        with sqlite3.connect(connection_string) as connection:
            create_tables(connection)
            insert_data(connection)
            register(connection, "Alex", "Smith", "alex.smith@example.com", "999888777", "Elm Street 2", "Odesa", "Ukraine", "Новий клієнт")
            items = [
                {"product_id": 1, "quantity": 2, "price": 15000.50},
                {"product_id": 2, "quantity": 1, "price": 8000.00}
            ]
            create(connection, 1, items)
            manage(connection, 1, 1, 'Email', 'Повідомлення про акції')
            segment(connection, city="Kyiv", country="Ukraine")    
    except sqlite3.Error as e:
        print(f"Помилка бази даних: {e}")

def create_tables(connection):
    create_customer_table = """
        CREATE TABLE IF NOT EXISTS Customers (
            CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName VARCHAR(50) NOT NULL,
            LastName VARCHAR(50) NOT NULL,
            Email VARCHAR(100) NOT NULL,
            PhoneNumber VARCHAR(20),
            Address VARCHAR(255),
            City VARCHAR(50),
            Country VARCHAR(50),
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Notes TEXT
        );
    """
    create_products_table = """
        CREATE TABLE IF NOT EXISTS Products(
            ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProductName VARCHAR(100) NOT NULL,
            Description TEXT,
            Price DECIMAL(10, 2) NOT NULL,
            Stock INT DEFAULT 0,
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    create_orders_table = """
        CREATE TABLE IF NOT EXISTS Orders(
            OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INT NOT NULL,
            OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            TotalAmount DECIMAL(10, 2) NOT NULL,
            Status TEXT DEFAULT 'Pending',
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
        );
    """
    create_orderitems_table = """
        CREATE TABLE IF NOT EXISTS OrderItems (
            OrderItemID INTEGER PRIMARY KEY AUTOINCREMENT,
            OrderID INT NOT NULL,
            ProductID INT NOT NULL,
            Quantity INT NOT NULL,
            Price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        );
    """
    create_salesRepresentatives_table = """
        CREATE TABLE IF NOT EXISTS SalesRepresentatives (
            SalesRepID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName VARCHAR(50) NOT NULL,
            LastName VARCHAR(50) NOT NULL,
            Email VARCHAR(100) UNIQUE NOT NULL,
            PhoneNumber VARCHAR(20),
            CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    create_SalesActivities_table = """
        CREATE TABLE IF NOT EXISTS SalesActivities (
            ActivityID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INT NOT NULL,
            SalesRepID INTEGER NOT NULL,
            ActivityType TEXT CHECK(ActivityType IN ('Call', 'Meeting', 'Email')) NOT NULL,
            ActivityDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Notes TEXT,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
            FOREIGN KEY (SalesRepID) REFERENCES SalesRepresentatives(SalesRepID)
        );
    """
    with connection:
        connection.execute(create_customer_table)
        connection.execute(create_products_table)
        connection.execute(create_orders_table)
        connection.execute(create_orderitems_table)
        connection.execute(create_salesRepresentatives_table)
        connection.execute(create_SalesActivities_table)
    print("Таблиці створені успішно.")
#!----------------------------------------------------------------------------------------------------------------------------------------------------
def insert_data(connection):
    insert_customer = """
        INSERT INTO Customers (FirstName, LastName, Email, PhoneNumber, Address, City, Country, Notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    customers = [
        ("Ivan", "Petrenko", "ivan.petrenko@example.com", "123456789", "Main Street 1", "Kyiv", "Ukraine", "Постійний клієнт"),
        ("Olha", "Shevchenko", "olha.shevchenko@example.com", "987654321", "Park Avenue 12", "Lviv", "Ukraine", "Запитує про нові продукти"),
    ]
    with connection:
        for customer in customers:
            connection.execute(insert_customer, customer)
#*----------------------------------------------------------------------------------------------------------------------------------------------------
    insert_product = """
        INSERT INTO Products (ProductName, Description, Price, Stock)
        VALUES (?, ?, ?, ?);
    """
    products = [
        ("Ноутбук", "Ноутбук для роботи та навчання", 15000.50, 10),
        ("Смартфон", "Смартфон із високою роздільною здатністю", 8000.00, 20),
    ]
    with connection:
        for product in products:
            connection.execute(insert_product, product)
#*----------------------------------------------------------------------------------------------------------------------------------------------------
    insert_order = """
        INSERT INTO Orders (CustomerID, TotalAmount, Status)
        VALUES (?, ?, ?);
    """
    orders = [
        (1, 15000.50, 'Completed'),
        (2, 8000.00, 'Pending'),
    ]
    with connection:
        for order in orders:
            connection.execute(insert_order, order)
#*----------------------------------------------------------------------------------------------------------------------------------------------------
    insert_order_item = """
        INSERT INTO OrderItems (OrderID, ProductID, Quantity, Price)
        VALUES (?, ?, ?, ?);
    """
    order_items = [
        (1, 1, 1, 15000.50),
        (2, 2, 1, 8000.00),
    ]
    with connection:
        for order_item in order_items:
            connection.execute(insert_order_item, order_item)
#*----------------------------------------------------------------------------------------------------------------------------------------------------
    insert_sales_rep = """
        INSERT INTO SalesRepresentatives (FirstName, LastName, Email, PhoneNumber)
        VALUES (?, ?, ?, ?);
    """
    sales_reps = [
        ("Anna", "Koval", "anna.koval@example.com", "123123123"),
        ("Pavlo", "Ivanov", "pavlo.ivanov@example.com", "456456456"),
    ]
    with connection:
        for sales_rep in sales_reps:
            connection.execute(insert_sales_rep, sales_rep)
#*----------------------------------------------------------------------------------------------------------------------------------------------------
    insert_sales_activity = """
        INSERT INTO SalesActivities (CustomerID, SalesRepID, ActivityType, Notes)
        VALUES (?, ?, ?, ?);
    """
    sales_activities = [
        (1, 1, 'Call', 'Дзвонили для уточнення деталей'),
        (2, 2, 'Meeting', 'Зустріч з обговорення нових умов'),
    ]
    with connection:
        for sales_activity in sales_activities:
            connection.execute(insert_sales_activity, sales_activity)

#!----------------------------------------------------------------------------------------------------------------------------------------------------
def register(connection, first_name, last_name, email, phone_number, address, city, country, notes):
    check_query = "SELECT 1 FROM Customers WHERE Email = ?"
    insert_query = """
        INSERT INTO Customers (FirstName, LastName, Email, PhoneNumber, Address, City, Country, Notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    try:
        cursor = connection.execute(check_query, (email,))
        if cursor.fetchone():
            print("Помилка: Клієнт з таким email вже існує.")
            return
        with connection:
            connection.execute(insert_query, (first_name, last_name, email, phone_number, address, city, country, notes))
        print("Клієнт зареєстрований успішно.")
    except sqlite3.Error as e:
        print(f"Помилка при реєстрації клієнта: {e}")
#*----------------------------------------------------------------------------------------------------------------------------------------------------
def manage(connection, customer_id, sales_rep_id, activity_type, notes):
    query = """
        INSERT INTO SalesActivities (CustomerID, SalesRepID, ActivityType, Notes)
        VALUES (?, ?, ?, ?);
    """
    try:
        with connection:
            connection.execute(query, (customer_id, sales_rep_id, activity_type, notes))
        print("Продаж успішно додано.")
    except sqlite3.Error as e:
        print(f"Помилка при управлінні продажами: {e}")
#*----------------------------------------------------------------------------------------------------------------------------------------------------
def create(connection, customer_id, items, status="Pending"):
    insert_order = """
        INSERT INTO Orders (CustomerID, TotalAmount, Status)
        VALUES (?, ?, ?);
    """
    order_id = None
    total_amount = sum(item['price'] * item['quantity'] for item in items)

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(insert_order, (customer_id, total_amount, status))
            order_id = cursor.lastrowid #? используется для получения идентификатора последней вставленной строки в базе данных
            insert_order_item = """
                INSERT INTO OrderItems (OrderID, ProductID, Quantity, Price)
                VALUES (?, ?, ?, ?);
            """
            for item in items:
                cursor.execute(insert_order_item, (order_id, item['product_id'], item['quantity'], item['price']))
        print("Замовлення створено успішно.")
    except sqlite3.Error as e:
        print(f"Помилка при створенні замовлення: {e}")
#*----------------------------------------------------------------------------------------------------------------------------------------------------
def segment(connection, city=None, country=None):
    query = "SELECT * FROM Customers WHERE 1=1"
    params = []

    if city:
        query += " AND City = ?"
        params.append(city)
    if country:
        query += " AND Country = ?"
        params.append(country)
    try:
        cursor = connection.execute(query, params)
        customers = cursor.fetchall()
        for customer in customers:
            print(customer)
    except sqlite3.Error as e:
        print(f"Помилка при сегментації клієнтів: {e}")
#!----------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
