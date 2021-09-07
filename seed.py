import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='tasklist',
    password='pirple',
    database='tasklist'
)
cursor = connection.cursor();
cursor.execute("""
    INSERT INTO users(firstname,lastname,username,password)
    VALUES('Admin','User','admin','adminpass');
""")
cursor.execute("""
    INSERT INTO admin(username) VALUES('admin');
""")
connection.commit()
cursor.close()
connection.close()
