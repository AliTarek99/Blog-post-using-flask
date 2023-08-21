from flask import Flask, render_template, request, session, redirect, url_for, flash, Markup
from werkzeug.utils import secure_filename

import blogDB
import commentsDB
import userDB
import os
import imagesDB
from enums import State


app = Flask(__name__, static_folder='static')
app.secret_key = 'cyberus'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'usr_id' in session:
        return redirect(url_for('home'))
    if request.method == "POST":
        if request.form['psw'] != request.form['psw-repeat']:
            flash("Passwords do not match")
            return redirect(url_for('register'))
        done = userDB.insert(request.form['email'], request.form['psw'])
        if done == State.valid:
            session['usr_id'] = userDB.getId(request.form['email'])
            return redirect(url_for('home'))
        else:
            if done == State.duplicate:
                flash("Email already exists")
            elif done == State.short_pass:
                flash('Password must be at least 8 characters')
            return redirect(url_for('register'))
    else:
        return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def login():
    if 'usr_id' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']
        done = userDB.verify(email, password)
        if done == State.valid:
            session['usr_id'] = userDB.getId(email)
            return redirect(url_for('home'))
        elif done == State.notfound:
            flash("Wrong email or password")
        return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('usr_id', None)
    return redirect(url_for('login'))


# Define a route for the home page
@app.route('/home')
def home():
    # Get all the blog posts from the database
    posts = blogDB.getall()
    # Render the 'home.html' template with the blog posts
    return render_template('home.html', posts=posts)


# Define a route for a blog post with comments
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    if 'usr_id' not in session:
        return redirect(url_for('login'))
    # If the request is a POST request, insert a new comment into the database
    if request.method == 'POST':
        comment = Markup(request.form['comment'])
        commentsDB.insert(session['usr_id'], post_id, comment)
        # Redirect the user back to the blog post page
        return redirect(url_for('post', post_id=post_id))
    # If the request is a GET request, get the blog post and its comments from the database
    else:
        post, comments, images = blogDB.getone(post_id)
        # Render the 'post.html' template with the blog post and its comments
        return render_template('post.html', post=post, comments=comments, images=images)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'usr_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        blog = request.form['blog']
        blog_id = blogDB.insert(session['usr_id'], title, blog)
        if 'file' in request.files and len(request.files['file'].filename) > 0:
            file = request.files['file']
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.static_folder, filename))
                imagesDB.insert(filename, blog_id)
            else:
                return redirect(url_for('upload'))
            return redirect(url_for('post', post_id=blog_id))
    return render_template('upload.html')


@app.route('/profile')
def profile():
    if 'usr_id' not in session:
        return redirect(url_for('login'))
    blogs = blogDB.get_all_with_id(session['usr_id'][0])
    return render_template('profile.html', email=userDB.getmail(session['usr_id'][0]), posts=blogs)


app.run(debug=True)
