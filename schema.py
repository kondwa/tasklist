import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='tasklist',
    password='pirple',
    database='tasklist'
)
cursor = connection.cursor();

cursor.execute(
"""
CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(255),
    lastname VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255),
    created TIMESTAMP DEFAULT NOW()
);
""")

cursor.execute(
"""
CREATE TABLE admin(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    created TIMESTAMP DEFAULT NOW()
);
""")

cursor.execute(
"""
CREATE TABLE tasks(
    id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(255),
    duedate DATE,
    done TINYINT,
    username VARCHAR(255),
    created TIMESTAMP DEFAULT NOW()
);
""")
connection.commit()
cursor.close()
connection.close()
