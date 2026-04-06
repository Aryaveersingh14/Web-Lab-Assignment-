from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

posts = []
post_id = 1

# Home - Read
@app.route('/')
def index():
    return render_template('index.html', posts=posts)

# Create
@app.route('/add', methods=['POST'])
def add():
    global post_id

    title = request.form['title']
    content = request.form['content']

    posts.append({
        'id': post_id,
        'title': title,
        'content': content
    })

    post_id += 1
    return redirect(url_for('index'))

# Delete
@app.route('/delete/<int:id>')
def delete(id):
    global posts
    posts = [p for p in posts if p['id'] != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)