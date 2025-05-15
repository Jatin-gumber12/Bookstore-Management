# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

def connect_db():
    return sqlite3.connect("bookstore.db")

def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            author TEXT,
            quantity INTEGER,
            price REAL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book TEXT,
            quantity INTEGER,
            customer TEXT,
            customer_number TEXT,
            sell_price REAL,
            date TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            emp_id INTEGER PRIMARY KEY,
            name TEXT,
            salary REAL,
            join_date TEXT,
            address TEXT,
            mobile TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/add_book", methods=["POST"])
def add_book():
    data = request.json
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO books (name, author, quantity, price) VALUES (?, ?, ?, ?)",
                (data['name'], data['author'], data['quantity'], data['price']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Book added successfully!"})

@app.route("/sell_book", methods=["POST"])
def sell_book():
    data = request.json
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT quantity, price FROM books WHERE name = ?", (data['name'],))
    row = cur.fetchone()
    if not row or row[0] < data['quantity']:
        return jsonify({"message": "Not enough books in stock."})

    new_qty = row[0] - data['quantity']
    book_price = row[1]
    sell_price = data['quantity'] * book_price * 1.5
    cur.execute("UPDATE books SET quantity = ? WHERE name = ?", (new_qty, data['name']))

    cur.execute("INSERT INTO sales (book, quantity, customer, customer_number, sell_price, date) VALUES (?, ?, ?, ?, ?, ?)",
                (data['name'], data['quantity'], data['customer'], data['customer_number'],
                 sell_price, datetime.today().strftime('%Y-%m-%d')))

    conn.commit()
    conn.close()
    return jsonify({"message": "Book sold successfully!"})

@app.route("/profit")
def profit():
    conn = connect_db()
    cur = conn.cursor()
    today = datetime.today().strftime('%Y-%m-%d')
    month = datetime.today().strftime('%Y-%m')

    def calc_profit(filter_date):
        cur.execute("SELECT quantity, sell_price, book FROM sales WHERE date LIKE ?", (f"{filter_date}%",))
        total_profit = 0
        for qty, sell_price, book in cur.fetchall():
            cur.execute("SELECT price FROM books WHERE name = ?", (book,))
            cost = cur.fetchone()
            if cost:
                total_profit += (sell_price - qty * cost[0])
        return round(total_profit, 2)

    profit_today = calc_profit(today)
    profit_month = calc_profit(month)
    conn.close()
    return jsonify({"today": profit_today, "month": profit_month})

@app.route("/add_staff", methods=["POST"])
def add_staff():
    data = request.json
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO staff (emp_id, name, salary, join_date, address, mobile) VALUES (?, ?, ?, ?, ?, ?)",
                (data['emp_id'], data['name'], data['salary'], data['date'], data['address'], data['mobile']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Staff added successfully!"})

@app.route("/delete_staff/<int:emp_id>", methods=["DELETE"])
def delete_staff(emp_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM staff WHERE emp_id = ?", (emp_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Staff deleted successfully!"})

@app.route("/search_book")
def search_book():
    name = request.args.get("name", "")
    author = request.args.get("author", "")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT name, author, quantity, price FROM books WHERE name LIKE ? AND author LIKE ?",
                (f"%{name}%", f"%{author}%"))
    results = [{"name": r[0], "author": r[1], "quantity": r[2], "price": r[3]} for r in cur.fetchall()]
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
