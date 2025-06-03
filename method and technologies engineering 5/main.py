import sqlite3
import pandas as pd
import os

# Функція для видалення CSV-файлів і бази даних, якщо вони існують
def delete_files():
    files = ['rooms_data.csv', 'filtered_rooms.csv', 'sorted_bookings.csv',
             'grouped_rooms.csv', 'having_rooms.csv', 'rooms_bookings.csv', 'hotel.db']
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f'{file} було видалено.')
        else:
            print(f'{file} не існує, видалення не потрібне.')

# Видалити CSV і базу даних перед виконанням основного коду
delete_files()

# Підключення до бази даних SQLite (або створення нової)
conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()

# 1. Створення таблиць (Rooms і Bookings)
cursor.execute('''CREATE TABLE IF NOT EXISTS Rooms (
                    id INTEGER PRIMARY KEY,
                    type TEXT NOT NULL,
                    price REAL NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Bookings (
                    id INTEGER PRIMARY KEY,
                    room_id INTEGER NOT NULL,
                    check_in_date DATE NOT NULL,
                    check_out_date DATE NOT NULL,
                    FOREIGN KEY (room_id) REFERENCES Rooms(id))''')

# 2. Вставка тестових даних (з деякими типами номерів, які повторюються)
cursor.executemany('INSERT INTO Rooms (id, type, price) VALUES (?, ?, ?)', [
    (1, 'Single', 100.00),
    (2, 'Double', 150.00),
    (3, 'Suite', 300.00),
    (4, 'Single', 100.00),  # Дубльований тип 'Single'
    (5, 'Double', 150.00)   # Дубльований тип 'Double'
])

cursor.executemany('INSERT INTO Bookings (id, room_id, check_in_date, check_out_date) VALUES (?, ?, ?, ?)', [
    (1, 1, '2024-10-14', '2024-10-16'),
    (2, 2, '2024-10-15', '2024-10-18'),
    (3, 3, '2024-10-20', '2024-10-25'),
    (4, 4, '2024-10-14', '2024-10-17'),
    (5, 5, '2024-10-15', '2024-10-20')
])

# Підтвердження змін у базі даних
conn.commit()

# 3. SQL-запити

# Базова операція зчитування
query = "SELECT * FROM Rooms"
df_rooms = pd.read_sql_query(query, conn)

# Оновлення ціни для конкретного номера
cursor.execute('''UPDATE Rooms 
                  SET price = 120.00 
                  WHERE id = 1''')

# Видалення запису про бронювання
cursor.execute('''DELETE FROM Bookings 
                  WHERE id = 1''')

# Фільтрація номерів за ціною
query = "SELECT * FROM Rooms WHERE price < 200"
df_filtered_rooms = pd.read_sql_query(query, conn)

# Сортування бронювань за датою заїзду (в порядку спадання)
query = "SELECT * FROM Bookings ORDER BY check_in_date DESC"
df_sorted_bookings = pd.read_sql_query(query, conn)

# Підрахунок кількості номерів для кожного типу
query = "SELECT type, COUNT(*) FROM Rooms GROUP BY type"
df_grouped_rooms = pd.read_sql_query(query, conn)

# Показати типи номерів, які мають більше одного номера (HAVING)
query = '''SELECT type, COUNT(*) 
           FROM Rooms 
           GROUP BY type 
           HAVING COUNT(*) > 1'''
df_having_rooms = pd.read_sql_query(query, conn)

# Об'єднання таблиць Rooms і Bookings для перегляду деталей номерів з бронюваннями
query = '''SELECT Rooms.id, Rooms.type, Rooms.price, Bookings.check_in_date, Bookings.check_out_date
           FROM Rooms
           JOIN Bookings ON Rooms.id = Bookings.room_id'''
df_joined = pd.read_sql_query(query, conn)


# 4. Збереження результатів у CSV-файли
df_rooms.to_csv('rooms_data.csv', index=False)
df_filtered_rooms.to_csv('filtered_rooms.csv', index=False)
df_sorted_bookings.to_csv('sorted_bookings.csv', index=False)
df_grouped_rooms.to_csv('grouped_rooms.csv', index=False)
df_having_rooms.to_csv('having_rooms.csv', index=False)
df_joined.to_csv('rooms_bookings.csv', index=False)


# Закриття з'єднання з базою даних
conn.close()

print("Дані збережено у CSV-файли.")