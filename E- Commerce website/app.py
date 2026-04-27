from flask import Flask, render_template_string, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("ecommerce.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER
    )
    """)

    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO products (name, price) VALUES (?, ?)", [
            ("Laptop", 50000),
            ("Phone", 20000),
            ("Headphones", 2000),
            ("Smart Watch", 5000)
        ])

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route('/')
def home():
    conn = sqlite3.connect("ecommerce.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>MyStore</title>

<style>
body {
    margin: 0;
    font-family: Arial;
    background: linear-gradient(-45deg, #1e3c72, #2a5298, #6a11cb, #2575fc);
    background-size: 400% 400%;
    animation: bg 10s ease infinite;
    color: white;
}
@keyframes bg {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.container { padding: 20px; }

.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    padding: 15px;
    margin: 15px;
    border-radius: 15px;
    display: inline-block;
    width: 230px;
    transition: 0.3s;
}
.card:hover {
    transform: scale(1.08);
    box-shadow: 0 0 20px rgba(255,255,255,0.3);
}

button {
    background: #00c6ff;
    border: none;
    padding: 10px;
    border-radius: 10px;
    color: white;
    cursor: pointer;
}

a {
    color: white;
    text-decoration: none;
    margin: 8px;
}
</style>
</head>

<body>
<div class="container">

<div class="nav">
    <h2>🛒 NovaCart</h2>
    <div>
        {% if 'user' in session %}
            Welcome {{ session['user'] }}
            <a href="/logout">Logout</a>
        {% else %}
            <a href="/login">Login</a>
            <a href="/signup">Signup</a>
        {% endif %}
        <a href="/cart">Cart</a>
    </div>
</div>

<hr>

{% for p in products %}
<div class="card">
    <h3>{{ p[1] }}</h3>
    <p>₹{{ p[2] }}</p>
    <a href="/add/{{ p[0] }}"><button>Add to Cart</button></a>
</div>
{% endfor %}

</div>
</body>
</html>
""", products=products)

# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        conn = sqlite3.connect("ecommerce.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pwd))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template_string("""
<style>
body {
    background: linear-gradient(to right, #141e30, #243b55);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.box {
    background: rgba(255,255,255,0.1);
    padding: 30px;
    border-radius: 15px;
}
input, button {
    margin: 10px;
    padding: 10px;
}
</style>

<div class="box">
<h2>Signup</h2>
<form method="POST">
<input name="username" placeholder="Username"><br>
<input type="password" name="password" placeholder="Password"><br>
<button>Signup</button>
</form>
<a href="/login">Already have account?</a>
</div>
""")

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        conn = sqlite3.connect("ecommerce.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        result = cur.fetchone()
        conn.close()

        if result:
            session['user'] = user
            return redirect('/')
        else:
            return "Invalid credentials"

    return render_template_string("""
<style>
body {
    background: linear-gradient(to right, #000428, #004e92);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.box {
    background: rgba(255,255,255,0.1);
    padding: 30px;
    border-radius: 15px;
}
input, button {
    margin: 10px;
    padding: 10px;
}
</style>

<div class="box">
<h2>Login</h2>
<form method="POST">
<input name="username" placeholder="Username"><br>
<input type="password" name="password" placeholder="Password"><br>
<button>Login</button>
</form>
<a href="/signup">Create account</a>
</div>
""")

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------------- CART ----------------
@app.route('/add/<int:id>')
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(id)
    return redirect('/cart')

@app.route('/cart')
def cart():
    conn = sqlite3.connect("ecommerce.db")
    cur = conn.cursor()

    cart_items = []
    total = 0

    for item_id in session.get("cart", []):
        cur.execute("SELECT * FROM products WHERE id=?", (item_id,))
        item = cur.fetchone()
        if item:
            cart_items.append(item)
            total += item[2]

    conn.close()

    return render_template_string("""
<style>
body {
    background: linear-gradient(to right, #141e30, #243b55);
    color: white;
    font-family: Arial;
}
.card {
    background: rgba(255,255,255,0.1);
    padding: 15px;
    margin: 15px;
    border-radius: 10px;
    transition: 0.3s;
}
.card:hover {
    transform: translateY(-5px);
}
button {
    padding: 8px;
    border: none;
    border-radius: 8px;
    background: red;
    color: white;
}
</style>

<h1>🛍️ Cart</h1>
<a href="/">Home</a>
<hr>

{% for item in items %}
<div class="card">
    <h3>{{ item[1] }}</h3>
    <p>₹{{ item[2] }}</p>
    <a href="/remove/{{ item[0] }}"><button>Remove</button></a>
</div>
{% endfor %}

<h2>Total: ₹{{ total }}</h2>
<a href="/checkout"><button>Checkout</button></a>
""", items=cart_items, total=total)

@app.route('/remove/<int:id>')
def remove(id):
    if "cart" in session and id in session["cart"]:
        session["cart"].remove(id)
    return redirect('/cart')

# ---------------- CHECKOUT ----------------
@app.route('/checkout')
def checkout():
    session["cart"] = []
    return "<h1>✅ Order Placed Successfully!</h1><a href='/'>Go Home</a>"

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True) 