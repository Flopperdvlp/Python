import sqlite3

def main():
    connection_string = "Library.db"
    try:
        with sqlite3.connect(connection_string) as connection:
            create_tables(connection)
            insert_data(connection)
            #add_book(connection)
    except sqlite3.Error as e:
        print(f"Помилка бази даних: {e}")

def create_tables(connection):
    create_book_table = """
        CREATE TABLE IF NOT EXISTS books  (
            BookId INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT,
            Author TEXT,
            Genre TEXT,
            YearPublished INTEGER,
            IsAvailable BOOLEAN DEFAULT 1
        );
    """
    create_readers_table  = """
        CREATE TABLE IF NOT EXISTS Readers (
            ReaderId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Email TEXT,
            phone TEXT
        );
    """
    create_loans_table = """
        CREATE TABLE IF NOT EXISTS Loans (
            LoanId INTEGER PRIMARY KEY AUTOINCREMENT,
            BookId INTEGER,
            ReaderId INTEGER,
            LoanDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ReturnDate TIMESTAMP,
            IsReturned BOOLEAN DEFAULT 0,
            FOREIGN KEY(BookId) REFERENCES Books(BookId),
            FOREIGN KEY(ReaderId) REFERENCES Readers(ReaderId)
        );
    """
    print("Таблиці створені успішно.")
    with connection:
        connection.execute(create_book_table)
        connection.execute(create_readers_table)
        connection.execute(create_loans_table)
        print("Таблиці створені успішно.")
def insert_data(connection):
    insert_books = """
        INSERT INTO Books (Title, Author, Genre, YearPublished) 
        VALUES
            ('1984', 'George Orwell', 'Dystopian', 1949),
            ('Brave New World', 'Aldous Huxley', 'Science Fiction', 1932),
            ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 1960);
    """
    insert_readers = """
        INSERT INTO Readers (Name, Email, Phone) 
        VALUES
            ('John Doe', 'john@example.com', '123-456-7890'),
            ('Jane Smith', 'jane@example.com', '098-765-4321'),
            ('Bob Johnson', 'bob@example.com', '555-555-5555');
    """
    with connection:
        connection.execute(insert_books)
        connection.execute(insert_readers)

def add_book(connection, title, author, genre, year_published):
    query = "INSERT INTO Books (Title, Author, Genre, YearPublished) VALUES (?, ?, ?, ?)"
    with connection:
        connection.execute(query, (title, author, genre, year_published))
    print(f"Книга '{title}' успішно додана.")

if __name__ == "__main__":
    main()
