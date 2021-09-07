import mysql.connector

def dbconnect():
    connection = mysql.connector.connect(
        host='localhost',
        user='tasklist',
        password='pirple',
        database='tasklist'
    )
    return connection
def read_overdue(username):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE username='{username}' AND done=0 AND duedate < CURDATE() ORDER BY duedate ASC".format(username=username))
    tasks = cursor.fetchall();
    cursor.close()
    connection.close()
    return tasks;
def read_upcoming(username):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE username='{username}' AND done=0 AND duedate > CURDATE() ORDER BY duedate ASC".format(username=username))
    tasks = cursor.fetchall();
    cursor.close()
    connection.close()
    return tasks;
def read_done(username):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE username='{username}' AND done = 1 ORDER BY duedate ASC".format(username=username))
    tasks = cursor.fetchall();
    cursor.close()
    connection.close()
    return tasks;
def read_current(username):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE username='{username}' AND done = 0 AND duedate=CURDATE() ORDER BY duedate ASC".format(username=username))
    tasks = cursor.fetchall();
    cursor.close()
    connection.close()
    return tasks;


def create_task(task,done,duedate,username):
    connection =  dbconnect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks(task,done,duedate,username)VALUES('{task}',{done},'{duedate}','{username}');".format(task=task,done=done,duedate=duedate.date(),username=username))
    connection.commit()
    cursor.close()
    connection.close()
def read_task(id):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id={id}".format(id=id))
    task = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return task;

def read_tasks():
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall();
    cursor.close()
    connection.close()
    return tasks;

def update_task(id,task,done,duedate):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE tasks SET task='{task}',done={done},duedate='{duedate}' WHERE id={id}
    """.format(id=id,task=task,done=done,duedate=duedate.date())
    )
    connection.commit()
    cursor.close()
    connection.close()

def delete_task(id):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id={id}".format(id=id))
    connection.commit()
    cursor.close()
    connection.close()

def signup(firstname,lastname,username,password):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM users WHERE username='{username}'".format(username=username))
    exists = cursor.fetchone()
    if exists is None:
        cursor.execute(
        """
            INSERT INTO users(firstname,lastname,username,password)
            VALUES('{firstname}','{lastname}','{username}','{password}')
        """.format(firstname=firstname,lastname=lastname,username=username,password=password)
        )
        connection.commit()
        cursor.close()
    else:
        return "Oops! User already exists."
    return None

def signin(username,password):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM users WHERE username='{username}'".format(username=username))
    db_password = cursor.fetchone()
    if db_password is None:
        return False
    else:
        return password == db_password[0]

def read_users_paged(offset,limit):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users LIMIT {limit} OFFSET {offset}".format(offset=offset,limit=limit))
    users = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return users;
def read_users():
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return users;

def read_users_24():
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE created > DATE_SUB(NOW(),INTERVAL 24 HOUR)")
    users = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return users;

def read_tasks_24():
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE created > DATE_SUB(NOW(),INTERVAL 24 HOUR)")
    tasks = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return tasks;

def read_user(id):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id={id}".format(id=id))
    user = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return user;

def update_user(id,firstname,lastname,username,password):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute(
        """
            UPDATE users
            SET firstname='{firstname}',lastname='{lastname}',username='{username}',password='{password}'
            WHERE id={id}
        """.format(id=id,firstname=firstname,lastname=lastname,username=username,password=password)
        )
    connection.commit()
    cursor.close()

def delete_user(id):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id={id}".format(id=id))
    connection.commit()
    cursor.close()
    connection.close()

def is_admin(username):
    connection = dbconnect()
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM admin WHERE username='{username}'".format(username=username))
    admin = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return admin;
