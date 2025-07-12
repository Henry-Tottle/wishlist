from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key_for_flash_message'

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

@app.route('/edit/<int:id>', methods=['GET'])
def editForm(id):

	connection = get_db_connection()
	item = connection.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()
	connection.close()
	return render_template('editForm.html', item=item)

@app.route('/edit/<int:id>', methods=["POST"])
def edit(id):
	itemName = request.form['itemName']
	source = request.form['source']
	category = request.form['category']
	connection = get_db_connection()
	connection.execute('UPDATE items SET itemName = ?, source = ?, category = ? WHERE id = ?', (itemName, source, category, id))
	connection.commit()
	connection.close()
	flash('Item edited.')
	return redirect('/wishlist')
	
	

@app.route('/delete/<int:id>', methods=['GET'])
def deleteForm(id):
	connection = get_db_connection()
	item = connection.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()
	connection.close()
	return render_template('deleteForm.html', item=item)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
	connection = get_db_connection()
	connection.execute('DELETE FROM items WHERE id =?', (id,))
	connection.commit()
	connection.close()
	flash('Item deleted.')
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
