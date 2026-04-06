from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

contacts = []

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Contacts Management System</title>
<style>
body{
    font-family: Arial, sans-serif;
    background:#f4f6f8;
    padding:20px;
}
.container{
    max-width:900px;
    margin:auto;
    background:white;
    padding:20px;
    border-radius:10px;
    box-shadow:0 0 10px rgba(0,0,0,0.1);
}
h1{
    text-align:center;
}
form{
    margin-bottom:20px;
}
input{
    padding:10px;
    margin:5px;
    width:28%;
}
button{
    padding:10px 15px;
    border:none;
    background:#007BFF;
    color:white;
    border-radius:5px;
    cursor:pointer;
}
button:hover{
    background:#0056b3;
}
.delete{
    background:red;
}
table{
    width:100%;
    border-collapse:collapse;
    margin-top:20px;
}
th,td{
    padding:10px;
    border-bottom:1px solid #ddd;
    text-align:left;
}
</style>
</head>
<body>

<div class="container">
<h1>Contacts Management System</h1>

<form method="POST" action="/add">
<input type="text" name="name" placeholder="Name" required>
<input type="text" name="phone" placeholder="Phone" required>
<input type="email" name="email" placeholder="Email" required>
<button type="submit">Add Contact</button>
</form>

<table>
<thead>
<tr>
<th>Name</th>
<th>Phone</th>
<th>Email</th>
<th>Action</th>
</tr>
</thead>
<tbody>
{% for c in contacts %}
<tr>
<td>{{c.name}}</td>
<td>{{c.phone}}</td>
<td>{{c.email}}</td>
<td>
<form method="POST" action="/delete/{{loop.index0}}" style="display:inline;">
<button class="delete">Delete</button>
</form>
</td>
</tr>
{% endfor %}
</tbody>
</table>

</div>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, contacts=contacts)

@app.route('/add', methods=['POST'])
def add():
    contact = {
        "name": request.form['name'],
        "phone": request.form['phone'],
        "email": request.form['email']
    }
    contacts.append(contact)
    return redirect(url_for('home'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    if 0 <= index < len(contacts):
        contacts.pop(index)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)