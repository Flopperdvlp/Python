import sqlite3

def main():
    connection_string = "university.db"
    try:
        with sqlite3.connect(connection_string) as connection:
            create_tables(connection)
            insert_data(connection)
            print("База данных для университета успешно создана и заполнена.")
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")

def create_tables(connection):
    create_students_table = """
        CREATE TABLE IF NOT EXISTS Students (
            StudentId INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            DateOfBirth TEXT,
            EnrollmentDate TEXT
        );
    """
    create_teachers_table = """
        CREATE TABLE IF NOT EXISTS Teachers (
            TeacherId INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Subject TEXT NOT NULL
        );
    """
    create_course_table = """
        CREATE TABLE IF NOT EXISTS Courses (
            CourseId INTEGER PRIMARY KEY AUTOINCREMENT,
            CourseName TEXT NOT NULL,
            Credits INTEGER NOT NULL,
            TeacherId INTEGER,
            FOREIGN KEY (TeacherId) REFERENCES Teachers(TeacherId)
        );
    """
    create_exams_table = """
        CREATE TABLE IF NOT EXISTS Exams (
            ExamId INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentId INTEGER,
            CourseId INTEGER,
            ExamDate TEXT,
            Grade INTEGER,
            FOREIGN KEY (StudentId) REFERENCES Student(StudentId),
            FOREIGN KEY (CourseId) REFERENCES Courses(CourseId)
        );
    """
    
    with connection:
        connection.execute(create_students_table)
        connection.execute(create_teachers_table)
        connection.execute(create_course_table)
        connection.execute(create_exams_table)
    
    print("Таблицы для университета созданы.")

def insert_data(connection):
    insert_students = """
        INSERT INTO Students (FirstName, LastName, DateOfBirth, EnrollmentDate)
        VALUES 
            ('Іван', 'Коваленко', '2001-05-10', '2019-09-01'),
            ('Марія', 'Петренко', '2000-08-15', '2018-09-01'),
            ('Олександр', 'Сидоренко', '1999-12-05', '2017-09-01'),
            ('Олена', 'Іваненко', '2002-02-20', '2020-09-01'),
            ('Дмитро', 'Шевченко', '2001-11-25', '2019-09-01');
    """
    
    insert_teachers = """
        INSERT INTO Teachers (FirstName, LastName, Subject)
        VALUES 
            ('Олександр', 'Коваль', 'Математика'),
            ('Ольга', 'Мельник', 'Фізика'),
            ('Ірина', 'Гриненко', 'Інформатика'),
            ('Петро', 'Захаренко', 'Хімія'),
            ('Валерія', 'Кравченко', 'Біологія');
    """
    insert_courses = """
        INSERT INTO Courses (CourseName, Credits, TeacherId)
        VALUES 
            ('Алгебра', 4, 1),
            ('Механіка', 3, 2),
            ('Програмування', 5, 3),
            ('Органічна хімія', 4, 4),
            ('Мікробіологія', 3, 5);
    """
    
    insert_exams = """
        INSERT INTO Exams (StudentId, CourseId, Grade, ExamDate)
        VALUES 
            (1, 1, 'A', '2023-06-15'),
            (2, 3, 'B', '2023-06-20'),
            (3, 2, 'A', '2023-06-25'),
            (4, 5, 'C', '2023-07-01'),
            (5, 4, 'B', '2023-07-10');
    """
    with connection:
        connection.execute(insert_students)
        connection.execute(insert_teachers)
        connection.execute(insert_courses)
        connection.execute(insert_exams)
    
    print("Данные для университета добавлены.")

if __name__ == "__main__":
    main()