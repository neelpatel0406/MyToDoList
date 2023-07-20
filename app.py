from flask import Flask, render_template, request, redirect, session
import pyodbc
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

import pyodbc



conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=NKJ;'
                      'Database=MyToDoList;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()  


@app.route('/')



def home():
        return render_template('home.html')


def generate_random_id():
    return random.randint(100, 999)

@app.route('/register', methods=['GET', 'POST'])
def register():
    print("hello")
    if request.method == 'POST':
        
        id = generate_random_id()
        username = request.form['username']
        password = request.form['password']
        
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (ID,Username, Password) VALUES (?,?, ?)", id, username, password)
        conn.commit()
        cursor.close()
        
        return render_template('login.html')
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", username, password)
        user = cursor.fetchone()
        cursor.close()
        print("user",user)
        if user:
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'username' in session : 
        username = session['username']
        cursor.execute("SELECT id,title,description,status FROM dbo.tasks Where username=?",(username,))
        tasks=cursor.fetchall()
        return render_template('Dashboard.html',tasks=tasks)
    else:
        return render_template('Dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)