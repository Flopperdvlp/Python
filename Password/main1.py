import sqlite3
import base64

def xor_encrypt_decrypt(data, key):
    encrypted_data = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))
    return base64.b64encode(encrypted_data.encode()).decode()

def xor_decrypt(encrypted_data, key):
    encrypted_data = base64.b64decode(encrypted_data).decode()
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(encrypted_data))

def authenticate():
    correct_password = "admin123"
    password = input("Введите пароль для доступа к функциям шифрования/дешифрования: ")
    return password == correct_password

def main():
    connection_string = "Data.db"
    key = "secretkey"
    
    if not authenticate():
        print("Неправильный пароль! Доступ запрещен.")
        return

    try:
        with sqlite3.connect(connection_string) as connection:
            create_tables(connection)
            while True:
                choice = input(
                    "\nВыберите действие:\n"
                    "1 - Добавить нового пользователя\n"
                    "2 - Показать и расшифровать данные\n"
                    "3 - Выйти\n")
                if choice == '1':
                    insert_user(connection, key)
                elif choice == '2':
                    read_and_decrypt_users(connection, key)
                elif choice == '3':
                    print("Выход из программы.")
                    break
                else:
                    break
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")

def create_tables(connection):
    create_users_table = """
        CREATE TABLE IF NOT EXISTS User(
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        );
    """
    connection.execute(create_users_table)

def insert_user(connection, key):
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    
    encrypted_password = xor_encrypt_decrypt(password, key)
    print(f"Зашифрованный пароль: {encrypted_password}")
    
    decrypted_password = xor_decrypt(encrypted_password, key)
    print(f"Расшифрованный пароль: {decrypted_password}")
    
    insert_user = "INSERT INTO User (username, password) VALUES (?, ?)"
    connection.execute(insert_user, (username, encrypted_password))
    connection.commit()
    print("Пользователь успешно добавлен!")

def read_and_decrypt_users(connection, key):
    select_users = "SELECT username, password FROM User"
    cursor = connection.execute(select_users)

    for row in cursor.fetchall():
        username = row[0]
        encrypted_password = row[1]
        decrypted_password = xor_decrypt(encrypted_password, key)
        print(f"Username: {username}, Зашифрованный пароль: {encrypted_password}, Расшифрованный пароль: {decrypted_password}")

if __name__ == "__main__":
    main()
