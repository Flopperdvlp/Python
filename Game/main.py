import sqlite3

def main():
    connection_string = "Game.db"
    try:
        with sqlite3.connect(connection_string) as connection:
            create_tables(connection)
            
            while True:
                print("1. Зареєструвати нового гравця")
                print("2. Зберегти прогрес гри")
                print("3. Завантажити прогрес гри")
                print("4. Вийти")
                choice = input("Оберіть опцію: ")
                if choice == '1':
                    register_player(connection)
                elif choice == '2':
                    save_progress(connection)
                elif choice == '3':
                    load_progress(connection)
                elif choice == '4':
                    break
                else:
                    print("Невірний вибір.")
    except sqlite3.Error as e:
        print(f"Помилка бази даних: {e}")

def create_tables(connection):
    create_player_table = """
        CREATE TABLE IF NOT EXISTS Players (
            PlayerId INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
    """
    create_progress_table = """
        CREATE TABLE IF NOT EXISTS Progress (
            ProgressId INTEGER PRIMARY KEY AUTOINCREMENT,
            PlayerId INTEGER,
            level INTEGER,
            score INTEGER,
            FOREIGN KEY(PlayerId) REFERENCES Players(PlayerId)
        );
    """
    connection.execute(create_player_table)
    connection.execute(create_progress_table)

def register_player(connection):
    username = input("Введіть ім'я користувача: ")
    password = input("Введіть пароль: ")

    insert_player = "INSERT INTO Players (username, password) VALUES (?, ?)"
    try:
        connection.execute(insert_player, (username, password))
        connection.commit()
        print(f"Гравця {username} успішно зареєстровано.")
    except sqlite3.Error as e:
        print(f"Помилка реєстрації гравця: {e}")

def save_progress(connection):
    username = input("Введіть ім'я користувача: ")
    level = int(input("Введіть рівень: "))
    score = int(input("Введіть кількість балів: "))

    player_id = get_player_id(connection, username)
    if player_id is not None:
        insert_progress = "INSERT INTO Progress (PlayerId, level, score) VALUES (?, ?, ?)"
        try:
            connection.execute(insert_progress, (player_id, level, score))
            connection.commit()
            print(f"Прогрес гравця {username} успішно збережено.")
        except sqlite3.Error as e:
            print(f"Помилка збереження прогресу: {e}")
    else:
        print("Гравця не знайдено.")

def load_progress(connection):
    username = input("Введіть ім'я користувача: ")

    player_id = get_player_id(connection, username)
    if player_id is not None:
        select_progress = "SELECT level, score FROM Progress WHERE PlayerId = ?"
        cursor = connection.execute(select_progress, (player_id,))
        progress = cursor.fetchone()
        
        if progress:
            print(f"Прогрес гравця {username}: Рівень {progress[0]}, Бали {progress[1]}")
        else:
            print(f"Прогрес для гравця {username} не знайдено.")
    else:
        print("Гравця не знайдено.")

def get_player_id(connection, username):
    select_player = "SELECT PlayerId FROM Players WHERE username = ?"
    cursor = connection.execute(select_player, (username,))
    player = cursor.fetchone()
    
    if player:
        return player[0]
    else:
        return None

if __name__ == "__main__":
    main()
