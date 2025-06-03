import pandas as pd
import sqlite3

# Перший DataFrame
df1 = pd.DataFrame({
    'ID': [1, 2, 3],
    'Name': ['Alice', 'Bob', 'Charlie']
})

# Другий DataFrame
df2 = pd.DataFrame({
    'ID': [2, 3, 4],
    'Age': [25, 30, 35]
})

print("DataFrame 1:")
print(df1)

print("\nDataFrame 2:")
print(df2)

inner_join = pd.merge(df1, df2, on='ID', how='inner')
print("\nInner Join:")
print(inner_join)

left_join = pd.merge(df1, df2, on='ID', how='left')
print("\nLeft Join:")
print(left_join)

right_join = pd.merge(df1, df2, on='ID', how='right')
print("\nRight Join:")
print(right_join)

# Створення або підключення до бази даних
connection = sqlite3.connect("test.db")

cursor = connection.cursor()

# Створення першої таблиці
# cursor.execute("""
# CREATE TABLE Table1 (
#     ID INTEGER PRIMARY KEY,
#     Name TEXT
# );
# """)

# Створення другої таблиці
# cursor.execute("""
# CREATE TABLE Table2 (
#     ID INTEGER PRIMARY KEY,
#     Age INTEGER
# );
# """)

# Додавання даних у таблиці
# cursor.executemany("INSERT INTO Table1 (ID, Name) VALUES (?, ?);", [
#     (1, "Alice"),
#     (2, "Bob"),
#     (3, "Charlie")
# ])
#
# cursor.executemany("INSERT INTO Table2 (ID, Age) VALUES (?, ?);", [
#     (2, 25),
#     (3, 30),
#     (4, 35)
# ])
#
# connection.commit()

#Iner join
cursor.execute("""
SELECT Table1.ID, Table1.Name, Table2.Age
FROM Table1
INNER JOIN Table2 ON Table1.ID = Table2.ID;
""")
inner_join_result = cursor.fetchall()

print("\n Inner Join Result:")
for row in inner_join_result:
    print(row)

#Left Join
cursor.execute("""
SELECT Table1.ID, Table1.Name, Table2.Age
FROM Table1
LEFT JOIN Table2 ON Table1.ID = Table2.ID;
""")
left_join_result = cursor.fetchall()

print("\nLeft Join Result:")
for row in left_join_result:
    print(row)
