import sqlite3

connection = sqlite3.connect("test.sqlite3")

cursor = connection.cursor()

''' create a table '''
def create_table(instance):
    with connection:
        cursor.execute("""CREATE TABLE test (
                    first text,
                    last text,
                    pay integer
                    )""")
    # connection.commit()

''' add data into a table '''
def update(instance):
    with connection:
        cursor.execute("INSERT INTO test VALUES (':first',':last',:pay)",{"first":instance.first,"last":instance.last,"pay":instance.pay})
        # connection.commit()

''' select/fetch data from a table '''
# cursor.execute("SELECT * FROM test")

''' select/fetch data from a table with condition '''
cursor.execute("SELECT * FROM test WHERE first='Muhammad'")


print(cursor.fetchall())

connection.close()