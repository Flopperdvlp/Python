import sqlite3

def main():
    connection_string = "NovaPosta.db"
    try:
        with sqlite3.connect(connection_string) as connection:
            create_tables(connection)
            insert_data(connection)
    except sqlite3.Error as e:
        print(f"Помилка бази даних: {e}")

def create_tables(connection):
    create_user_table  = """
        CREATE TABLE IF NOT EXISTS User (
            UserId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Email TEXT,
            Password TEXT
        );
    """
    create_message_table = """
        CREATE TABLE IF NOT EXISTS messages  (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            receiver_id INTEGER,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(sender_id) REFERENCES users(id),
            FOREIGN KEY(receiver_id) REFERENCES users(id)
        );
    """
    print("Таблиці створені успішно.")
    with connection:
        connection.execute(create_user_table)
        connection.execute(create_message_table)
def insert_data(connection):
    insert_users = """
        INSERT INTO User (Name, Email, Password) 
        VALUES
            ('John Doe', 'john@example.com', 'password1'),
            ('Jane Smith', 'jane@example.com', 'password2'),
            ('Bob Johnson', 'bob@example.com', 'password3');
    """
    insert_messages = """""
        INSERT INTO messages (sender_id, receiver_id, subject, body)
        VALUES
            (1, 2, 'Hello', 'How are you?'),
            (2, 1, 'Hi', 'I am fine, thank you!'),
            (1, 3, 'Hey', 'What are you up to?');
    """""
    with connection:
        connection.execute(insert_users)
        connection.execute(insert_messages)
if __name__ == "__main__":
    main()
