import sqlite3
import random

def main():
    connection_string = "Game.db"
    try:
        with sqlite3.connect(connection_string) as connection:
            create_tables(connection)
            insert_data(connection)
            get_analytics(connection)
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")

def create_tables(connection):
    create_cities_table = """
        CREATE TABLE IF NOT EXISTS Cities (
            CityID INTEGER PRIMARY KEY AUTOINCREMENT,
            CityName VARCHAR(100) NOT NULL,
            Population INT
        );
    """
    
    create_events_table = """
        CREATE TABLE IF NOT EXISTS Events (
            EventID INTEGER PRIMARY KEY AUTOINCREMENT,
            EventType VARCHAR(100) NOT NULL,
            CityID INT,
            FOREIGN KEY (CityID) REFERENCES Cities(CityID)
        );
    """
    with connection:
        connection.execute(create_cities_table)
        connection.execute(create_events_table)    
    print("Таблицы успешно созданы.")

def insert_data(connection):
    cities_data = [
        ("Киев", 2950000),
        ("Львов", 720000),
        ("Одесса", 1010000),
        ("Харьков", 1440000),
        ("Днепр", 1000000),
        ("Запорожье", 700000),
        ("Винница", 370000),
        ("Николаев", 490000),
        ("Черновцы", 250000),
        ("Полтава", 290000)
    ]

    with connection:
        connection.executemany("INSERT INTO Cities (CityName, Population) VALUES (?, ?)", cities_data)
    
    event_types = [
        "Землетрус", "Снегопад", "Наводнение", "Ураган", 
        "Лавина", "Засуха", "Гроза", "Шторм", 
        "Солнечное затмение", "Торнадо"
    ]

    events = []
    for _ in range(100):  
        city_id = random.randint(1, len(cities_data))
        event_type = random.choice(event_types)
        events.append((event_type, city_id))
    with connection:
        connection.executemany("INSERT INTO Events (EventType, CityID) VALUES (?, ?)", events)

    print("Данные успешно вставлены.")

def get_analytics(connection):
    query = '''
    SELECT c.CityName, COUNT(e.EventID) AS EventCount
    FROM Cities c
    LEFT JOIN Events e ON c.CityID = e.CityID
    GROUP BY c.CityName
    ORDER BY EventCount DESC
    '''
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    print("\nАналитика событий по городам:")
    for row in results:
        print(f"Город: {row[0]}, Количество событий: {row[1]}")

if __name__ == "__main__":
    main()
