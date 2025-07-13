from flask import Flask, render_template, request, redirect, flash
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = 'secret_key_for_flash_message'

def get_db_connection():
    connection = psycopg2.connect(os.environ['DATABASE_URL'])
    return connection

@app.route("/")
def home():
    return "Welcome to your wishlist!"

@app.route("/wishlist")
def index():
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute('SELECT * FROM items')
    items = cur.fetchall()
    print(items)
    cur.close()
    connection.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    itemName = request.form['itemName']
    source = request.form['source']
    category = request.form['category']
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute('INSERT INTO items (itemName, source, category, obtained) VALUES (%s, %s, %s, %s)',
                (itemName, source, category, False))
    connection.commit()
    cur.close()
    connection.close()
    return redirect('/wishlist')

@app.route('/obtained', methods=['POST'])
def markObtained():
    item_id = request.form['item_id']
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute('UPDATE items SET obtained = %s WHERE id = %s', (True,item_id,))
    connection.commit()
    cur.close()
    connection.close()
    return redirect('/wishlist')

@app.route('/edit/<int:id>', methods=['GET'])
def editForm(id):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute('SELECT * FROM items WHERE id = %s', (id,))
    item = cur.fetchone()
    cur.close()
    connection.close()
    return render_template('editForm.html', item=item)

@app.route('/edit/<int:id>', methods=["POST"])
def edit(id):
    itemName = request.form['itemName']
    source = request.form['source']
    category = request.form['category']
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute('UPDATE items SET itemName = %s, source = %s, category = %s WHERE id = %s',
                (itemName, source, category, id))
    connection.commit()
    cur.close()
    connection.close()
    flash('Item edited.')
    return redirect('/wishlist')

@app.route('/delete/<int:id>', methods=['GET'])
def deleteForm(id):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute('SELECT * FROM items WHERE id = %s', (id,))
    item = cur.fetchone()
    cur.close()
    connection.close()
    return render_template('deleteForm.html', item=item)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute('DELETE FROM items WHERE id = %s', (id,))
    connection.commit()
    cur.close()
    connection.close()
    flash('Item deleted.')
    return redirect('/wishlist')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5003)))
