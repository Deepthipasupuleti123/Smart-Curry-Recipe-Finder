from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = "secretkey"

# Load ML model
model = pickle.load(open("model/chatbot_model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

# Database connection
def connect_db():
    conn = sqlite3.connect("chatbot.db")
    return conn

# Home Page
@app.route('/')
def home():
    return render_template("index.html")

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
        """)

        cur.execute("INSERT INTO users(username,password) VALUES(?,?)",
                    (username, password))

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template("register.html")

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                    (username, password))

        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect('/dashboard')

    return render_template("login.html")

# Dashboard
@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    return render_template("dashboard.html",
                           username=session['user'])

# Chat API
@app.route('/chat', methods=['POST'])
def chat():

    user_message = request.json['message']

    data = vectorizer.transform([user_message])

    prediction = model.predict(data)[0]

    return jsonify({
        "response": prediction
    })

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)