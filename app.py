from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

def create_table(conn):
    query = '''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    '''
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO entries (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        flash('تم تسجيل البيانات بنجاح', 'success')
    except sqlite3.IntegrityError:
        flash('البريد الإلكتروني موجود مسبقًا', 'error')
    conn.close()
    return redirect(url_for('home'))

@app.route('/entries')
def entries():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries')
    entries = cursor.fetchall()
    conn.close()
    return render_template('entries.html', entries=entries)

if __name__ == '__main__':
    create_table(create_connection())
    app.run(debug=True)
