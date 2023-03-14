import sqlite3
import re

conn = sqlite3.connect('test.db')

c= conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS employees (
            first text,
            last text,
            pay interger
    )""")



# c.execute("INSERT INTO employees VALUES ('Death', 'Ender', 2)")
# c.execute("INSERT INTO employees VALUES ('Nghiem', 'Dat', 2)")
# conn.commit()





c.execute("""UPDATE employees
SET pay=10000
WHERE first='Death'""")

c.execute("SELECT pay FROM employees WHERE first='Death'")
value=c.fetchall()
v=value[0]
v1=v[0]
# t=tuple(value)
# print(t[0])
# a=int(re.search(r'\d+', v).group())
# print(a)

# c.execute("SELECT * FROM employees WHERE last = 'Ender'")
# print(c.fetchall())
conn.commit()
conn.close()

