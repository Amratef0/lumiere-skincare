from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import datetime
import os

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)
app.secret_key = "lumiere_secret_key_2025"

#  DB CONNECTION
def get_db():
    return mysql.connector.connect(
        host="mysql.railway.internal",
        user="root",
        password="zGQQwYOXBXfkEAEFmYqPcgDXoDbBjqsw",
        database="railway",
        port=3306
    )


#  HELPER: get or create cart
def get_cart_id(db):
    cursor = db.cursor(dictionary=True)

    if "user_id" in session:
        cursor.execute("SELECT cart_id FROM cart WHERE user_id = %s", (session["user_id"],))
        row = cursor.fetchone()
        if row:
            return row["cart_id"]
        cursor.execute("INSERT INTO cart (user_id) VALUES (%s)", (session["user_id"],))
        db.commit()
        return cursor.lastrowid

    else:
        if "guest_id" not in session:
            import uuid
            session["guest_id"] = str(uuid.uuid4())
        guest_id = session["guest_id"]
        cursor.execute("SELECT cart_id FROM cart WHERE guest_id = %s", (guest_id,))
        row = cursor.fetchone()
        if row:
            return row["cart_id"]
        cursor.execute("INSERT INTO cart (user_id, guest_id) VALUES (NULL, %s)", (guest_id,))
        db.commit()
        return cursor.lastrowid


#  HOME
@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
    SELECT p.product_id, p.name, p.price, p.image_url, c.name AS category
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    ORDER BY p.product_id DESC
    LIMIT 6
""")
    products = cursor.fetchall()
    db.close()
    return render_template("index.html", products=products)


#  SHOP
@app.route("/shop")
def shop():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    category_filter = request.args.get("category", "all")

    cursor.execute("SELECT name FROM categories ORDER BY name")
    categories = [row["name"] for row in cursor.fetchall()]

    if category_filter and category_filter != "all":
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, p.image_url, c.name AS category
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE LOWER(c.name) = %s
        """, (category_filter.lower(),))
    else:
        cursor.execute("""
            SELECT p.product_id, p.name, p.price, p.image_url, c.name AS category
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
        """)

    products = cursor.fetchall()
    db.close()
    return render_template("shop.html", products=products, categories=categories)


#  PRODUCT DETAIL
@app.route("/product/<int:product_id>")
def product(product_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.product_id AS id, p.product_id, p.name, p.price, p.description,
               p.image_url AS image, c.name AS category
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        WHERE p.product_id = %s
    """, (product_id,))
    product = cursor.fetchone()
    db.close()
    if not product:
        return redirect(url_for("shop"))
    return render_template("product.html", product=product)


#  ADD TO CART
@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id")
    db = get_db()
    cart_id = get_cart_id(db)
    cursor = db.cursor()

    cursor.execute(
        "SELECT quantity FROM cart_items WHERE cart_id=%s AND product_id=%s",
        (cart_id, product_id)
    )
    row = cursor.fetchone()
    if row:
        cursor.execute(
            "UPDATE cart_items SET quantity = quantity + 1 WHERE cart_id=%s AND product_id=%s",
            (cart_id, product_id)
        )
    else:
        cursor.execute(
            "INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (%s, %s, 1)",
            (cart_id, product_id)
        )
    db.commit()
    db.close()
    return redirect(url_for("cart"))


#  UPDATE CART 
@app.route("/update-cart", methods=["POST"])
def update_cart():
    product_id = request.form.get("product_id")
    action     = request.form.get("action")
    db = get_db()
    cart_id = get_cart_id(db)
    cursor = db.cursor()

    if action == "increase":
        cursor.execute(
            "UPDATE cart_items SET quantity = quantity + 1 WHERE cart_id=%s AND product_id=%s",
            (cart_id, product_id)
        )
    elif action == "decrease":
        cursor.execute(
            "SELECT quantity FROM cart_items WHERE cart_id=%s AND product_id=%s",
            (cart_id, product_id)
        )
        row = cursor.fetchone()
        if row and row[0] > 1:
            cursor.execute(
                "UPDATE cart_items SET quantity = quantity - 1 WHERE cart_id=%s AND product_id=%s",
                (cart_id, product_id)
            )
        else:
            cursor.execute(
                "DELETE FROM cart_items WHERE cart_id=%s AND product_id=%s",
                (cart_id, product_id)
            )
    db.commit()
    db.close()
    return redirect(url_for("cart"))


#  CART PAGE
@app.route("/cart")
def cart():
    db = get_db()
    cart_id = get_cart_id(db)
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT ci.product_id, p.name, p.price, p.image_url AS image, ci.quantity AS qty
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.product_id
        WHERE ci.cart_id = %s
    """, (cart_id,))
    items = cursor.fetchall()
    db.close()

    total = sum(i["price"] * i["qty"] for i in items)
    count = sum(i["qty"] for i in items)
    return render_template("cart.html", items=items, total=total, count=count)


#  CHECKOUT  GET
@app.route("/checkout", methods=["GET"])
def checkout():
    db = get_db()
    cart_id = get_cart_id(db)
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT ci.product_id, p.name, p.price, p.image_url AS image, ci.quantity AS qty
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.product_id
        WHERE ci.cart_id = %s
    """, (cart_id,))
    items = cursor.fetchall()
    db.close()

    subtotal = sum(i["price"] * i["qty"] for i in items)
    shipping = 0 if subtotal >= 700 or subtotal == 0 else 8
    total    = subtotal + shipping

    return render_template("checkout.html",
                           items=items,
                           subtotal=subtotal,
                           shipping=shipping,
                           total=total,
                           error="")


#  CHECKOUT  POST  → place order
@app.route("/checkout", methods=["POST"])
def place_order():
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    phone   = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    city    = request.form.get("city", "").strip()
    zip_    = request.form.get("zip", "").strip()
    country = request.form.get("country", "").strip()

    # ── basic server-side validation ──
    if not all([name, email, phone, address, city, zip_, country]):
        db = get_db()
        cart_id = get_cart_id(db)
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT ci.product_id, p.name, p.price, p.image_url AS image, ci.quantity AS qty
            FROM cart_items ci JOIN products p ON ci.product_id = p.product_id
            WHERE ci.cart_id = %s
        """, (cart_id,))
        items = cursor.fetchall()
        db.close()
        subtotal = sum(i["price"] * i["qty"] for i in items)
        shipping = 0 if subtotal >= 700 else 8
        return render_template("checkout.html",
                               items=items, subtotal=subtotal,
                               shipping=shipping, total=subtotal + shipping,
                               error="Please fill in all required fields.")

    full_address = f"{address}, {city}, {zip_}, {country}"

    db = get_db()
    cart_id = get_cart_id(db)
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT ci.product_id, p.name, p.price, p.image_url AS image, ci.quantity AS qty
        FROM cart_items ci JOIN products p ON ci.product_id = p.product_id
        WHERE ci.cart_id = %s
    """, (cart_id,))
    items = cursor.fetchall()

    subtotal = sum(i["price"] * i["qty"] for i in items)
    shipping = 0 if subtotal >= 700 else 8
    total    = subtotal + shipping

    user_id = session.get("user_id")  

    cursor2 = db.cursor()
    cursor2.execute("""
        INSERT INTO orders (user_id, total_price, address, status)
        VALUES (%s, %s, %s, 'pending')
    """, (user_id, total, full_address))
    order_id = cursor2.lastrowid

    for item in items:
        cursor2.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase)
            VALUES (%s, %s, %s, %s)
        """, (order_id, item["product_id"], item["qty"], item["price"]))

    # ── clear cart ──
    cursor2.execute("DELETE FROM cart_items WHERE cart_id = %s", (cart_id,))
    db.commit()
    db.close()

    order = {
        "id":      order_id,
        "name":    name,
        "email":   email,
        "address": full_address,
        "total":   total,
        "date":    datetime.now().strftime("%B %d, %Y")
    }

    return render_template("thankyou.html", order=order, items=items)


#  REGISTER
@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html", error="")

@app.route("/register", methods=["POST"])
def register():
    name     = request.form.get("name", "").strip()
    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    confirm  = request.form.get("confirm", "").strip()

    if not all([name, email, password, confirm]):
        return render_template("register.html", error="All fields are required.")
    if password != confirm:
        return render_template("register.html", error="Passwords do not match.")
    if len(password) < 6:
        return render_template("register.html", error="Password must be at least 6 characters.")

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        db.close()
        return render_template("register.html", error="Email already registered.")

    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, password)
    )
    db.commit()
    db.close()
    return redirect(url_for("login_page"))


#  LOGIN
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html", error="")

@app.route("/login", methods=["POST"])
def login():
    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT user_id, name, email FROM users WHERE email=%s AND password=%s",
        (email, password)
    )
    user = cursor.fetchone()
    db.close()

    if not user:
        return render_template("login.html", error="Invalid email or password.")

    session["user_id"]   = user["user_id"]
    session["user_name"] = user["name"]

    session["is_admin"] = 1 if email == "admin@lumiere.com" else 0

    return redirect(url_for("index"))


#  LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


#  ADMIN — list products
@app.route("/admin")
def admin():
    if not session.get("is_admin"):
        return redirect(url_for("login_page"))

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.product_id AS id, p.name, p.price, p.image_url AS image,
               c.name AS category
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        ORDER BY p.product_id
    """)
    products = cursor.fetchall()
    db.close()
    return render_template("admin.html", products=products)


#  ADMIN — product form  (Add)
@app.route("/product-form", methods=["GET"])
def product_form_add():
    if not session.get("is_admin"):
        return redirect(url_for("login_page"))
    return render_template("product-form.html", product=None)

@app.route("/product-form", methods=["POST"])
def product_form_add_post():
    if not session.get("is_admin"):
        return redirect(url_for("login_page"))

    name        = request.form.get("name", "").strip()
    category    = request.form.get("category", "").strip()
    price       = request.form.get("price", "0")
    image       = request.form.get("image", "").strip()
    description = request.form.get("description", "").strip()

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT category_id FROM categories WHERE name = %s", (category,))
    cat = cursor.fetchone()
    if cat:
        cat_id = cat["category_id"]
    else:
        cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category,))
        db.commit()
        cat_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO products (name, description, price, stock_quantity, category_id, image_url)
        VALUES (%s, %s, %s, 10, %s, %s)
    """, (name, description, float(price), cat_id, image))
    db.commit()
    db.close()
    return redirect(url_for("admin"))


#  ADMIN — product form  (Edit)
@app.route("/product-form/<int:product_id>", methods=["GET"])
def product_form_edit(product_id):
    if not session.get("is_admin"):
        return redirect(url_for("login_page"))

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.product_id AS id, p.name, p.price, p.image_url AS image,
               p.description, c.name AS category
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        WHERE p.product_id = %s
    """, (product_id,))
    product = cursor.fetchone()
    db.close()
    return render_template("product-form.html", product=product)

@app.route("/product-form/<int:product_id>", methods=["POST"])
def product_form_edit_post(product_id):
    if not session.get("is_admin"):
        return redirect(url_for("login_page"))

    name        = request.form.get("name", "").strip()
    category    = request.form.get("category", "").strip()
    price       = request.form.get("price", "0")
    image       = request.form.get("image", "").strip()
    description = request.form.get("description", "").strip()

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT category_id FROM categories WHERE name = %s", (category,))
    cat = cursor.fetchone()
    if cat:
        cat_id = cat["category_id"]
    else:
        cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category,))
        db.commit()
        cat_id = cursor.lastrowid

    cursor.execute("""
        UPDATE products
        SET name=%s, description=%s, price=%s, category_id=%s, image_url=%s
        WHERE product_id=%s
    """, (name, description, float(price), cat_id, image, product_id))
    db.commit()
    db.close()
    return redirect(url_for("admin"))


#  ADMIN — delete product
@app.route("/delete-product", methods=["POST"])
def delete_product():
    if not session.get("is_admin"):
        return redirect(url_for("login_page"))

    product_id = request.form.get("product_id")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
    db.commit()
    db.close()
    return redirect(url_for("admin"))


#  CONTACT
@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")

@app.route("/contact", methods=["POST"])
def contact_post():
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if name and email and message:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO contact_messages (name, email, subject, message)
            VALUES (%s, %s, %s, %s)
        """, (name, email, subject, message))
        db.commit()
        db.close()

    return redirect(url_for("contact"))


#  ABOUT
@app.route("/about")
def about():
    return render_template("about.html")


#  RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
