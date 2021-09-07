from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
import model

app = Flask(__name__)

app.secret_key = "tasklistapp"

def authorized():
    return 'username' in session

@app.route("/", methods=['GET'])
def dashboard():
    if authorized():
        username=session['username']
        current=model.read_current(username)
        overdue=model.read_overdue(username)
        upcoming=model.read_upcoming(username)
        done=model.read_done(username)
        return render_template('dashboard.html',current=current,overdue=overdue,upcoming=upcoming,done=done)
    else:
        return redirect(url_for('signin'))
@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')

@app.route("/terms", methods=['GET'])
def terms():
    return render_template('terms.html')

@app.route("/privacy", methods=['GET'])
def privacy():
    return render_template('privacy.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        message = model.signup(firstname,lastname,username,password)
        if message is None:
            return redirect(url_for('dashboard'))
        else:
            return render_template('signup.html',message=message)

@app.route('/signin',methods=['GET','POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    else:
        session.pop('username',None)
        username = request.form['username']
        password = request.form['password']
        if model.signin(username,password):
            session['username'] = username
            if model.is_admin(username):
                session['admin']=True
            return redirect(url_for('dashboard'))
        else:
            message = 'Oops! Wrong username or password.'
            return render_template('signin.html',message=message)

@app.route('/signout',methods=['GET','POST'])
def signout():
    if authorized():
        session.pop('username',None)
    if is_admin():
        session.pop('admin',None)
    return redirect(url_for('signin'))

@app.route('/createtask',methods=['GET','POST'])
def createtask():
    if authorized():
        if request.method == 'GET':
            return render_template('createtask.html')
        else:
            username=session['username']
            task = request.form['task']
            done = 0
            duedate = datetime.strptime(request.form['duedate'],"%Y-%m-%d")
            model.create_task(task,done,duedate,username)
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('signin'))

@app.route('/readtasks',methods=['GET'])
def readtasks():
    if authorized():
        tasks = model.read_tasks()
        return render_template('readtasks.html',tasks=tasks)
    else:
        return redirect(url_for('signin'))

@app.route('/updatetask/<id>',methods=['GET','POST'])
def updatetask(id):
    if authorized():
        if request.method == 'GET':
            task = model.read_task(id)
            return render_template('updatetask.html',task=task)
        else:
            task = request.form['task']
            if request.form.get('done') != None:
                done = 1
            else:
                done = 0
            duedate = datetime.strptime(request.form['duedate'],"%Y-%m-%d")
            model.update_task(id,task,done,duedate)
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('signin'))

@app.route('/deletetask/<id>',methods=['GET'])
def deletetask(id):
    if authorized():
        model.delete_task(id)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('signin'))

def is_admin():
    return 'admin' in session

@app.route('/admin')
def admin():
    if authorized() and is_admin():
        totalusers = len(model.read_users())
        totalusers24 = len(model.read_users_24())
        totaltasks = len(model.read_tasks())
        totaltasks24 = len(model.read_tasks_24())
        return render_template('admin.html',totalusers=totalusers,totalusers24=totalusers24,totaltasks=totaltasks,totaltasks24=totaltasks24)
    else:
        return redirect(url_for('signin'))

@app.route('/admin/users')
def admin_users():
    if authorized() and is_admin():
        page=1
        limit = 50
        offset = limit * (page-1)
        users = model.read_users_paged(offset,limit)
        return render_template('users.html',users=users,prev=0,next=page+1)
    else:
        return redirect(url_for('signin'))

@app.route('/admin/users/<page>')
def admin_users_paged(page):
    if authorized() and is_admin():
        page = int(page)
        limit = 50
        offset = limit * (page-1)
        users = model.read_users_paged(offset,limit)
        return render_template('users.html',users=users,prev=page-1,next=page+1)
    else:
        return redirect(url_for('signin'))

@app.route('/admin/signout',methods=['GET','POST'])
def admin_signout():
    if authorized() and is_admin():
        session.pop('username',None)
        session.pop('admin',None)
    return redirect(url_for('signin'))

@app.route('/updateuser/<id>',methods=['GET','POST'])
def updateuser(id):
    if authorized() and is_admin():
        if request.method == 'GET':
            user = model.read_user(id)
            return render_template('updateuser.html',user=user)
        else:
            firstname=request.form['firstname']
            lastname=request.form['lastname']
            username=request.form['username']
            password=request.form['password']
            model.update_user(id,firstname,lastname,username,password)
            return redirect(url_for('admin'))
    else:
        return redirect(url_for('admin_signin'))
@app.route('/deleteuser/<id>')
def deleteuser(id):
    if authorized() and is_admin():
        model.delete_user(id)
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('admin_signin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
