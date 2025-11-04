import sqlite3

connect =  sqlite3.connect('example.db')

cursor = connect.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               position TEXT NOT NULL,
               departament TEXT NOT NULL,
               salary REAL
            )
            ''')

connect.commit()

cursor.execute('''
    INSERT INTO employees (name, position, departament, salary)
    VALUES(?,?,?,?)               
''',('JOHN' , 'DEVELOPER' ,'IT', '700.00'))

connect.commit()

cursor.execute ('SELECT * FROM employees')
rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.execute('''
   UPDATE employees
   SET salary = ?
   WHERE name = ?
''', ('75000.00','JOHN'))


connect.commit()

cursor.execute('''
    DELETE FROM employees
    WHERE name = ?
    ''',('JOHN',))

connect.commit()
cursor.close()
connect.close()