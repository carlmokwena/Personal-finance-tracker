from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize DB
conn = sqlite3.connect('finance.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS transactions
             (id INTEGER PRIMARY KEY, type TEXT, category TEXT, amount REAL)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT type, category, amount FROM transactions")
    transactions = c.fetchall()
    conn.close()

    income = sum([t[2] for t in transactions if t[0] == 'Income'])
    expenses = sum([t[2] for t in transactions if t[0] == 'Expense'])

    return render_template('index.html', transactions=transactions, income=income, expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        t_type = request.form['type']
        category = request.form['category']
        amount = float(request.form['amount'])

        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        c.execute("INSERT INTO transactions (type, category, amount) VALUES (?, ?, ?)", (t_type, category, amount))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)