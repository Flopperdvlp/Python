import sqlite3

def main():
    connection_string = "Game.db"
    try:
        with sqlite3.connect(connection_string) as connection:
            create_tables(connection)
            insert_data(connection)
            print("База даних для онлайн ігор успішно створена і заповнена.")
    except sqlite3.Error as e:
        print(f"Помилка бази даних: {e}")

def create_tables(connection):
    create_user_table = """
        CREATE TABLE IF NOT EXISTS USERS (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT UNIQUE,
            register_date TEXT NOT NULL
        );
    """
    
    create_character_table = """
        CREATE TABLE IF NOT EXISTS CHARACTERS  (
            CharacterId INTEGER PRIMARY KEY AUTOINCREMENT,
            userid INTEGER,
            character_name TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            class TEXT NULL,
            FOREIGN KEY (userid) REFERENCES USERS(user_id)
        );
    """
    
    create_game_progress_table = """
        CREATE TABLE IF NOT EXISTS GAME_PROGRESS (
            progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id INTEGER,
            stage INTEGER NOT NULL,
            score INTEGER DEFAULT 0,
            FOREIGN KEY (character_id) REFERENCES CHARACTERS(CharacterId)
        );
    """
    
    with connection:
        connection.execute(create_user_table)
        connection.execute(create_character_table)
        connection.execute(create_game_progress_table)
    
    print("Таблиці створені успішно.")
def insert_data(connection):
    insert_users = """
        INSERT INTO USERS (username, password, email, register_date)
        VALUES 
            ('player1', 'pass1', 'player1@example.com', '2024-10-01'),
            ('player2', 'pass2', 'player2@example.com', '2024-10-02'),
            ('player3', 'pass3', 'player3@example.com', '2024-10-03');
    """
    
    insert_characters = """
        INSERT INTO CHARACTERS (userid, character_name, level, class)
        VALUES 
            (1, 'Warrior', 5, 'Fighter'),
            (2, 'Mage', 3, 'Wizard'),
            (3, 'Archer', 2, 'Ranger');
    """
    
    insert_game_progress = """
        INSERT INTO GAME_PROGRESS (character_id, stage, score)
        VALUES 
            (1, 1, 1000),
            (2, 2, 1500),
            (3, 1, 800);
    """
    
    with connection:
        connection.execute(insert_users)
        connection.execute(insert_characters)
        connection.execute(insert_game_progress)
    
    print("Дані успішно додані.")
if __name__ == "__main__":
    main()
