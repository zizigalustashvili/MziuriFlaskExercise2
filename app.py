from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
import sqlite3
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/posts/')
def index():
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts')
    posts = c.fetchall()
    conn.close()
    return render_template('posts.html', posts_in = posts)

@app.route('/posts/<int:post_id>/')
def post_detail(post_id):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = c.fetchone()
    conn.close()
    return render_template('post_detail.html', post = post)


class PostForm(FlaskForm):
    title = TextAreaField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])

@app.route('/posts/create/', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()
        c.execute("""
        INSERT INTO posts (title, description)
        VALUES(?,?)
        """, (form.title.data, form.description.data))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create_post.html', form = form)

app.secret_key = 'your_secret_key'
app.run(debug=True)




