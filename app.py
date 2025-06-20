from flask import Flask, render_template, request, redirect, session
import mysql.connector
from db_config import db_config

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        instructor = request.form['instructor']
        rating = request.form['rating']
        comments = request.form['comments']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (name, course, instructor, rating, comments) VALUES (%s, %s, %s, %s, %s)",
                       (name, course, instructor, rating, comments))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
    return render_template('feedback.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        if admin:
            session['admin'] = True
            return redirect('/admin')
    return render_template('login.html', error="Invalid credentials")

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/login')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM feedback")
    feedback_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin.html', feedback=feedback_list)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
