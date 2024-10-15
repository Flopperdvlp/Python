import sqlite3

def main():
    connection_string = "----.db"
    try:
        with sqlite3.connect(connection_string) as connection:
            create_tables(connection)
            insert_data(connection)
            print("База данных для ------ успешно создана и заполнена.")
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")

def create_tables(connection):
    create_customers_table = """
        CREATE TABLE IF NOT EXISTS Customers (
        );
    """
    with connection:
        connection.execute(create_customers_table)
    
    print("Таблицы для банка созданы.")

def insert_data(connection):
    # Заполнение таблицы Customers
    insert_customers = """
        INSERT INTO Customers (FirstName, LastName, Address, Phone, Email)
        VALUES 
            ('Иван', 'И', 'г. 1, ул. Пушкина, д.1', '1234567890', '1234@mail.com'),
            ('Анна', 'П', 'г. 2, ул. Ленина, д.2', '0987654321', '123@mail.com'),
            ('Дмитрий', 'С', 'г. 3, ул. Горького, д.3', '1122334455', '12@mail.com'),
            ('Екатерина', 'К', 'г. 4, ул. Лермонтова, д.4', '6677889900', '1@mail.com'),
            ('Алексей', 'С', 'г. 5, ул. Чехова, д.5', '5544332211', '2@mail.com');
    """
    with connection:
        connection.execute(insert_customers)
    
    print("Данные для ---- добавлены.")

if __name__ == "__main__":
    main()