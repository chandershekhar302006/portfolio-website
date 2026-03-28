from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# 🏠 HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# 👤 ABOUT PAGE
@app.route('/about')
def about():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()

    conn.close()

    return render_template('about.html', data=data)


# 📞 CONTACT PAGE
@app.route('/contact')
def contact():
    return render_template('contact.html')


# 💾 FORM SUBMIT (SAVE TO DATABASE)
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # connect database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    ''')

    # insert data
    cursor.execute(
        "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )

    conn.commit()
    conn.close()

    return "🔥 Message Saved Successfully! <br><a href='/'>Go Home</a>"


# ▶ RUN APP
if __name__ == '__main__':
    app.run(debug=True)