import sqlite3
import random

def main():
    connection_string = "----1.db"
    try:
        with sqlite3.connect(connection_string) as connection:
            create_tables(connection)
            insert_tables(connection)
            get_sales_by_age_group(connection)
            get_sales_by_product(connection)
            get_sales_by_region(connection)
            get_average_check(connection)
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
def create_tables(connection):
    create_tables = """
        CREATE TABLE IF NOT EXISTS Products(
            ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProductName VARCHAR(100),
            Description TEXT,
            Category VARCHAR(50),
            StockQuantity INT,
            SalesQuantity INT
        );
    """
    create_sales = """
        CREATE TABLE IF NOT EXISTS Sales(
            SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProductID INT,
            Region VARCHAR(100),
            AgeGroup VARCHAR(20),  
            Gender CHAR(1),        
            SaleDate DATE,
            QuantitySold INT,
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        );
    """
    cursor = connection.cursor()
    cursor.execute(create_tables)
    cursor.execute(create_sales)
    connection.commit()

#*---------------------------------------------------------------------------------------------

def insert_tables(connection):
    insert_tables = """
        INSERT INTO Products (ProductName, Description, Category, StockQuantity, SalesQuantity)
        VALUES
            ('Корм для собак', 'Сухий корм для собак', 'Корм', 100, 10),
            ('Іграшка для котів', 'яка іграшка для котів', 'Іграшки', 200, 15),
            ('Клітка для птахів', 'Клітка для канарок', 'Обладнання', 150, 5),
            ('Корм для риб', 'Гранули для риб', 'Корм', 300, 20),
            ('Набір для догляду за собакою', 'Щітка та шампунь', 'Гігієна', 250, 30),
            ('Акваріум', 'Скляний акваріум на 50 літрів', 'Обладнання', 50, 12),
            ('Наповнювач для котячого туалету', 'Натуральний деревний наповнювач', 'Гігієна', 400, 100),
            ('Лакомства для гризунів', 'Засоби для догляду за гризунами', 'Корм', 100, 8),
            ('Одяг для собак', 'Курточка зимова для маленьких собак', 'Одяг', 30, 5),
            ('Переноска для котів', 'Пластикова переноска для котів', 'Обладнання', 80, 12),
            -- Повтори та зміни дані для ще 1990 товарів.
            ('Товар N', 'Опис товару N', 'Категорія N', 120, 25);  
    """
    insert_sales = """
        INSERT INTO Sales (ProductID, Region, AgeGroup, Gender, SaleDate, QuantitySold)
        VALUES
            (1, 'Київ', '18-25', 'M', '2024-10-01', 5),
            (2, 'Львів', '26-35', 'F', '2024-10-02', 3),
            (3, 'Одеса', '36-45', 'M', '2024-10-03', 2),
            (4, 'Харків', '18-25', 'F', '2024-10-04', 4),
            (5, 'Дніпро', '46-55', 'M', '2024-10-05', 6),
            -- Повтори для ще 1995 записів про продажі.
            (2000, 'Київ', '26-35', 'F', '2024-10-21', 2);
    """
    cursor = connection.cursor()
    cursor.execute(insert_tables)
    cursor.execute(insert_sales)
    connection.commit()

#*---------------------------------------------------------------------------------------------

def get_sales_by_region(connection):
    query = """
        SELECT Region, SUM(QuantitySold) as TotalSold
        FROM Sales
        GROUP BY Region;
    """
    with connection:
        results = connection.execute(query).fetchall()
        print("Аналіз продажів за регіонами:")
        for row in results:
            print(f"Регіон: {row[0]}, Кількість проданих одиниць: {row[1]}")

def get_sales_by_product(connection):
    query = """
        SELECT P.ProductName, SUM(S.QuantitySold) as TotalSold
        FROM Sales S
        JOIN Products P ON S.ProductID = P.ProductID
        GROUP BY P.ProductName;
    """
    with connection:
        results = connection.execute(query).fetchall()
        print("Аналіз продажів за товарами:")
        for row in results:
            print(f"Товар: {row[0]}, Кількість проданих одиниць: {row[1]}")

def get_sales_by_age_group(connection):
    query = """
        SELECT AgeGroup, SUM(QuantitySold) as TotalSold
        FROM Sales
        GROUP BY AgeGroup;
    """
    with connection:
        results = connection.execute(query).fetchall()
        print("Аналіз продажів за віковими групами:")
        for row in results:
            print(f"Вікова група: {row[0]}, Кількість проданих одиниць: {row[1]}")

#*---------------------------------------------------------------------------------------------

def get_average_check(connection):
    query = """
        SELECT AVG(S.QuantitySold * P.Price) as AverageCheck
        FROM Sales S
        JOIN Products P ON S.ProductID = P.ProductID;
    """
    with connection:
        average_check = connection.execute(query).fetchone()[0]
        print(f"Середній чек: {average_check:.2f} грн")


#*---------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()