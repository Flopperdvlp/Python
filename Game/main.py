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
    create_player_table  = """
        CREATE TABLE IF NOT EXISTS Players (
            PlayerId INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
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
    
    print("Таблиці створені успішно.")

    def register_player(connection):
        username = input("Введіть ім'я користувача: ")
        password = input("Введіть пароль: ")
if __name__ == "__main__":
    main()
