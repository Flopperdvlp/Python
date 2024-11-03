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
    create_accounts_table = """
        CREATE TABLE IF NOT EXISTS Accounts (
        );
    """
    create_transactions_table = """
        CREATE TABLE IF NOT EXISTS Transactions (
        );
    """
    create_loans_table = """
        CREATE TABLE IF NOT EXISTS Loans (
        );
    """
    create_cards_table = """
        CREATE TABLE IF NOT EXISTS Cards (
        );
    """
    
    with connection:
        connection.execute(create_customers_table)
        connection.execute(create_accounts_table)
        connection.execute(create_transactions_table)
        connection.execute(create_loans_table)
        connection.execute(create_cards_table)
    
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
    
    # Заполнение таблицы Accounts
    insert_accounts = """
        INSERT INTO Accounts (CustomerId, AccountNumber, Balance, Type, CreatedDate)
        VALUES 
            (1, '1234567890123456', 12311.00, 'Сберегательный', '2023-01-10'),
            (2, '2345678901234567', 123123.00, 'Текущий', '2023-03-15'),
            (3, '3456789012345678', 12311.00, 'Депозитный', '2023-05-20'),
            (4, '4567890123456789', 12311.00, 'Сберегательный', '2023-07-25'),
            (5, '5678901234567890', 12312.00, 'Текущий', '2023-09-30');
    """
    
    # Заполнение таблицы Transactions
    insert_transactions = """
        INSERT INTO Transactions (AccountId, Amount, TransactionDate, Type, Description)
        VALUES 
            (1, -5000.00, '2023-01-15', 'Снятие', 'Оплата аренды'),
            (2, 10000.00, '2023-03-20', 'Пополнение', 'Зарплата'),
            (3, -20000.00, '2023-05-25', 'Снятие', 'Покупка автомобиля'),
            (4, 15000.00, '2023-07-30', 'Пополнение', 'Возврат долга'),
            (5, -3000.00, '2023-09-10', 'Снятие', 'Оплата коммунальных услуг');
    """
    
    # Заполнение таблицы Loans
    insert_loans = """
        INSERT INTO Loans (CustomerId, LoanAmount, InterestRate, LoanStartDate, LoanEndDate)
        VALUES 
            (1, 500000.00, 5.50, '2022-06-01', '2027-06-01'),
            (3, 1000000.00, 4.75, '2023-02-15', '2028-02-15'),
            (5, 250000.00, 6.00, '2023-09-01', '2026-09-01');
    """
    
    # Заполнение таблицы Cards
    insert_cards = """
        INSERT INTO Cards (CustomerId, CardNumber, ExpiryDate, CVV)
        VALUES 
            (1, '1111222233334444', '2026-01-01', '123'),
            (2, '5555666677778888', '2025-06-30', '456'),
            (3, '9999000011112222', '2024-12-31', '789'),
            (4, '3333444455556666', '2026-03-31', '321'),
            (5, '7777888899990000', '2025-09-30', '654');
    """
    
    with connection:
        connection.execute(insert_customers)
        connection.execute(insert_accounts)
        connection.execute(insert_transactions)
        connection.execute(insert_loans)
        connection.execute(insert_cards)
    
    print("Данные для банка добавлены.")

if __name__ == "__main__":
    main()