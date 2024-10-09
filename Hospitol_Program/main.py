import sqlite3

def main():
    connection_string = "hospital.db"
    try:
        with sqlite3.connect(connection_string) as connection:
            create_tables(connection)
            insert_data(connection)
            print("База данных для больницы успешно создана и заполнена.")
            insert_logins_and_passwords(connection)
            print("Логины и пароли успешно добавлены.")
            insert_numbers(connection)  # Insert sample numbers
            print("Числа успешно добавлены.")

            # Perform calculations
            numbers = fetch_numbers(connection)
            if numbers:
                total, product, average, sorted_asc, sorted_desc = calculate_statistics(numbers)
                print(f"Сумма: {total}")
                print(f"Произведение: {product}")
                print(f"Среднее значение: {average}")
                print(f"Сортировка по возрастанию: {sorted_asc}")
                print(f"Сортировка по убыванию: {sorted_desc}")
            else:
                print("Числа не найдены.")
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")

def create_tables(connection):
    create_departments_table = """
        CREATE TABLE IF NOT EXISTS Departments (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Building INT NOT NULL,
            Financing DECIMAL(10, 2) NOT NULL DEFAULT 0,
            Name NVARCHAR(100) NOT NULL UNIQUE
        );
    """
    create_logins_table = """
        CREATE TABLE IF NOT EXISTS Logins (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Login NVARCHAR(100) NOT NULL UNIQUE,
            Password NVARCHAR(100) NOT NULL
        );
    """
    create_numbers_table = """
        CREATE TABLE IF NOT EXISTS Numbers (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Value DECIMAL(10, 2) NOT NULL
        );
    """
    
    with connection:
        connection.execute(create_departments_table)
        connection.execute(create_logins_table)
        connection.execute(create_numbers_table)  # Create numbers table
    
    print("Таблицы созданы.")

def insert_data(connection):
    insert_departments = """
        INSERT INTO Departments (Building, Financing, Name)
        VALUES 
            (1, 50000, 'Отделение хирургии'),
            (2, 30000, 'Терапевтическое отделение');
    """
    
    with connection:
        connection.execute(insert_departments)
    
    print("Данные отделений добавлены.")

def insert_logins_and_passwords(connection):
    insert_logins = """
        INSERT INTO Logins (Login, Password)
        VALUES 
            ('user001', 'aB1x2Yz!'),
            ('user002', '4Jk3lMn9'),
            ('user003', 'Qr8x7Lp0'),
            ('user004', 'mNbV2F!3'),
            ('user005', 'kL7y#Zm4'),
            ('user006', 'oPq5rT6s'),
            ('user007', 'Xn3dW1!2'),
            ('user008', 'pLk8H#y9'),
            ('user009', 'bG5k!2Mn'),
            ('user010', 'P2xT1kV3'),
            ('user011', 'zQ3l#9Pm'),
            ('user012', 'dX7u2!Vw'),
            ('user013', 'aK4v!8xY'),
            ('user014', '1Kl2nZ6p'),
            ('user015', 'Ht5Wz!9Q'),
            ('user016', 'iJ7x!Y4b'),
            ('user017', 'Wq3Lp#9V'),
            ('user018', 'Jk6tP2#N'),
            ('user019', 'R1oMz!7w'),
            ('user020', '5Vu3jK!1'),
            ('user021', 'xL8#4KtY'),
            ('user022', 'fO7n!P9v'),
            ('user023', 'Bk3#2TrM'),
            ('user024', '1Pm9xRz!'),
            ('user025', 'hL7oK!4G'),
            ('user026', 'N8!r2ZqL'),
            ('user027', 'sK5T3!pW'),
            ('user028', 'vJ4P!1Mz'),
            ('user029', 'Qk2!9LtX'),
            ('user030', 'bR7fK!5T');
    """
    
    with connection:
        connection.execute(insert_logins)
    
    print("Логины и пароли добавлены.")

def insert_numbers(connection):
    # Example of inserting numbers into the Numbers table
    insert_numbers = """
        INSERT INTO Numbers (Value)
        VALUES 
            (10.5),
            (20.3),
            (5.7),
            (8.0),
            (12.2);
    """
    
    with connection:
        connection.execute(insert_numbers)
    
    print("Числа добавлены.")

def fetch_numbers(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT Value FROM Numbers;")
    numbers = [row[0] for row in cursor.fetchall()]
    return numbers

def calculate_statistics(numbers):
    total = sum(numbers)
    product = 1
    for num in numbers:
        product *= num
    average = total / len(numbers) if numbers else 0
    sorted_asc = sorted(numbers)
    sorted_desc = sorted(numbers, reverse=True)
    return total, product, average, sorted_asc, sorted_desc

if __name__ == "__main__":
    main()
