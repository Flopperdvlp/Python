import sqlite3

def xor_encrypt_decrypt(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))
def authenticate():
    correct_password = "admin123"  
    password = input("Введіть пароль для доступу до функцій шифрування/дешифрування: ")
    return password == correct_password
def main():
    connection_string = "Data.db"
    key = "secretkey"
    if not authenticate():
        print("Неправильний пароль! Доступ заборонено.")
        return
    try:
        with sqlite3.connect(connection_string) as connection:
            create_tables(connection)
            insert_tables(connection, key)
            read_and_decrypt_users(connection, key)
    except sqlite3.Error as e:
        print(f"Помилка бази даних: {e}")
#*-------------------------------------------------------------------------
def create_tables(connection):
    create_users_table = """
        CREATE TABLE IF NOT EXISTS User(
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        );
    """
    connection.execute(create_users_table)
#*--------------------------------------------------------------------------
def insert_tables(connection, key):
    username = "example_user"
    password = "secure_password"
    encrypted_password = xor_encrypt_decrypt(password, key)

    insert_user = "INSERT INTO User (username, password) VALUES (?, ?)"
    connection.execute(insert_user, (username, encrypted_password))
#*---------------------------------------------------------------------------
def read_and_decrypt_users(connection, key):
    select_users = "SELECT username, password FROM User"
    cursor = connection.execute(select_users)

    for row in cursor.fetchall():
        username = row[0]
        encrypted_password = row[1]
        decrypted_password = xor_encrypt_decrypt(encrypted_password, key)
        print(f"Username: {username}, Password: {decrypted_password}")
#*---------------------------------------------------------------------------
if __name__ == "__main__":
    main()