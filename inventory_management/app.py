from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jeden@12",
    database="InventoryDB"
)

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT p.ProductID, p.Name, p.Description, p.Price, c.Name AS Category, s.Name AS Supplier FROM Products p JOIN Categories c ON p.CategoryID = c.CategoryID JOIN Suppliers s ON p.SupplierID = s.SupplierID")
    products = cursor.fetchall()
    cursor.execute("SELECT Name FROM Products")
    all_product_names = cursor.fetchall()
    cursor.close()
    return render_template('index.html', products=products, all_product_names=all_product_names)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    category_id = request.form['category_id']
    supplier_id = request.form['supplier_id']
    cursor = db.cursor()
    cursor.execute("INSERT INTO Products (Name, Description, Price, CategoryID, SupplierID) VALUES (%s, %s, %s, %s, %s)",
                   (name, description, price, category_id, supplier_id))
    db.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    cursor = db.cursor(dictionary=True)
    
    # Fetch products matching the search query
    if query:
        cursor.execute(
            "SELECT p.ProductID, p.Name, p.Description, p.Price, c.Name AS Category, s.Name AS Supplier "
            "FROM Products p "
            "JOIN Categories c ON p.CategoryID = c.CategoryID "
            "JOIN Suppliers s ON p.SupplierID = s.SupplierID "
            "WHERE p.Name LIKE %s", ('%' + query + '%',)
        )
        products = cursor.fetchall()
    else:
        products = []

    # Fetch all products for the full product list
    cursor.execute(
        "SELECT p.ProductID, p.Name, p.Description, p.Price, c.Name AS Category, s.Name AS Supplier "
        "FROM Products p "
        "JOIN Categories c ON p.CategoryID = c.CategoryID "
        "JOIN Suppliers s ON p.SupplierID = s.SupplierID"
    )
    all_products = cursor.fetchall()

    cursor.close()
    
    return render_template('index.html', products=products, all_products=all_products, search_query=query)


if __name__ == '__main__':
    app.run(debug=True)
