from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
	connection = sqlite3.connect('wishlist.db')
	connection.row_factory = sqlite3.Row
	return connection

@app.route("/")
def home():
	return "Welcome to your wishlist!"

@app.route("/wishlist")
def index():
	connection = get_db_connection()
	items = connection.execute('SELECT * FROM items').fetchall()
	connection.close()
	return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
	itemName = request.form['itemName']
	source = request.form['source']
	category = request.form['category']
	connection = get_db_connection()
	connection.execute('INSERT INTO items (itemName, source, category, obtained) VALUES (?, ?, ?, ?)', (itemName, source, category, 0))
	connection.commit()
	connection.close()
	return redirect('/wishlist')

@app.route('/obtained', methods=['POST'])
def markObtained():
	item_id = request.form['item_id']

	connection = get_db_connection()
	connection.execute('UPDATE items SET obtained = 1 WHERE id = ?', (item_id))
	connection.commit()
	connection.close()
	return redirect('/wishlist')

@app.route('/delete', methods=['POST'])
def delete():
	item_id = request.form['item_id']
	connection = get_db_connection()
	connection.execute('DELETE FROM items WHERE id =?', (item_id))
	connection.commit()
	connection.close()
	return redirect('/wishlist')



if __name__ == "__main__":

	connection = get_db_connection()
	connection.execute('''
					 CREATE TABLE IF NOT EXISTS items (
					 id INTEGER PRIMARY KEY AUTOINCREMENT,
					 itemName TEXT NOT NULL,
					 source TEXT NOT NULL,
					 category TEXT NOT NULL,
					 obtained INTEGER NOT NULL DEFAULT 0)
					 ''')
	connection.commit()
	connection.close()
	app.run(debug=True, port=5003, use_reloader=False)
