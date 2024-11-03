import sqlite3
import random
from datetime import datetime, timedelta

def main():
    connection_string = "database.db"
    try:
        with sqlite3.connect(connection_string) as connection:
            create_tables(connection)
            insert_data(connection)
            insert_expenses(connection)
            analyze_data(connection)
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
def create_tables(connection):
    create_country_tables = """
        CREATE TABLE IF NOT EXISTS Country(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL            
        );
    """
    create_cities_tables = """
        CREATE TABLE IF NOT EXISTS City(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL
        );
    """

    create_budget_table = """
        CREATE TABLE IF NOT EXISTS Country (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Budget DECIMAL NOT NULL,
            CountryId INTEGER,
            FOREIGN KEY (CountryId) REFERENCES Country(Id)
        );
    """
    connection.execute("DROP TABLE IF EXISTS Expenses;")
    create_expense_table = """
        CREATE TABLE IF NOT EXISTS Expenses(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            CityId INTEGER,
            Date TEXT NOT NULL,
            Category TEXT NOT NULL,
            Amount DECIMAL NOT NULL,
            IsLoss INTEGER NOT NULL DEFAULT 0,  -- Новый столбец для отметки убытков
            FOREIGN KEY (CityId) REFERENCES City(Id)
        );
    """
    with connection:
        connection.execute(create_country_tables)
        connection.execute(create_cities_tables)
        connection.execute(create_budget_table)
        connection.execute(create_expense_table)
def insert_data(connection):
    country_name = ("Украина",)
    insert_country_query = "INSERT INTO Country (Name) VALUES (?);"
    connection.execute(insert_country_query, country_name)
    country_id = connection.execute("SELECT Id FROM Country WHERE Name = ?", country_name).fetchone()[0]
    cities = [
        "Киев", "Львов", "Одесса", "Харьков", "Днепр", "Запорожье", "Винница", 
        "Полтава", "Чернигов", "Житомир", "Ивано-Франковск", "Ужгород", 
        "Черновцы", "Херсон", "Николаев", "Мариуполь", "Луцк", "Ровно", 
        "Тернополь", "Сумы", "Кривой-Рог", "Кременчуг", "Белая-Церковь", 
        "Мелитополь", "Бердянск", "Черкассы", "Измаил", "Умань", "Борисполь", 
        "Краматорск", "Конотоп", "Бровары", "Славянск", "Буча", "Энергодар",
        "Константиновка", "Калуш", "Коломыя", "Александрия", "Тростянец", 
        "Шостка", "Северодонецк", "Нежин", "Коростень", "Ирпень", "Никополь", 
        "Первомайск", "Дрогобыч", "Болехов", "Камянец-Подольский", "Чортков",
        "Староконстантинов", "Ковель", "Лубны", "Золотоноша", "Ладыжин",
        "Вознесенск", "Долина", "Бурштын", "Глухов", "Лохвица", "Жмеринка",
        "Коростышев", "Каховка", "Павлоград", "Васильков", "Миргород", "Каменское",
        "Новомосковск", "Смела", "Вараш", "Горишние Плавни", "Чугуев", "Изюм", 
        "Новая-Каховка", "Лисичанск", "Токмак", "Геническ", "Южный", "Ильичевск"
    ]
    city_data = []
    for city in cities:
        budget = round(random.uniform(100000, 10000000), 2)  
        city_data.append((city, budget, country_id))
    insert_city_query = "INSERT INTO City (Name, Budget, CountryId) VALUES (?, ?, ?);"
    connection.executemany(insert_city_query, city_data)
def insert_expenses(connection):
    categories = ["Транспорт", "Продукты", "Жилищные расходы", "Оборудование", "Развлечения"]
    cities = connection.execute("SELECT Id FROM City").fetchall()
    
    expense_data = []
    for city in cities:
        city_id = city[0]
        for _ in range(random.randint(1, 10)):  
            date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            category = random.choice(categories)
            amount = round(random.uniform(1000, 50000), 2)
            is_loss = random.choice([0, 1]) 
            expense_data.append((city_id, date, category, amount, is_loss))
    
    insert_expense_query = "INSERT INTO Expenses (CityId, Date, Category, Amount, IsLoss) VALUES (?, ?, ?, ?, ?);"
    connection.executemany(insert_expense_query, expense_data)

def analyze_data(connection):
    print("Общая статистика по расходам и убыткам в каждом городе:")
    query = """
        SELECT City.Name,
            Expenses.Category,
            SUM(CASE WHEN Expenses.IsLoss = 0 THEN Expenses.Amount ELSE 0 END) as TotalExpenses,
            SUM(CASE WHEN Expenses.IsLoss = 1 THEN Expenses.Amount ELSE 0 END) as TotalLosses
        FROM Expenses
        JOIN City ON Expenses.CityId = City.Id
        GROUP BY City.Name, Expenses.Category
        ORDER BY City.Name, TotalExpenses DESC;
    """
    results = connection.execute(query).fetchall()
    for row in results:
        print(f"Город: {row[0]}, Категория: {row[1]}, Всего расходов: {row[2]:.2f}, Всего убытков: {row[3]:.2f}")

    print("\nНа что больше всего уходит бюджет во всех городах (учет убытков):")
    query = """
        SELECT Category,
            SUM(CASE WHEN IsLoss = 0 THEN Amount ELSE 0 END) as TotalExpenses,
            SUM(CASE WHEN IsLoss = 1 THEN Amount ELSE 0 END) as TotalLosses
        FROM Expenses
        GROUP BY Category
        ORDER BY TotalExpenses DESC;
    """
    results = connection.execute(query).fetchall()
    for row in results:
        print(f"Категория: {row[0]}, Всего расходов: {row[1]:.2f}, Всего убытков: {row[2]:.2f}")

if __name__ == "__main__":
    main()