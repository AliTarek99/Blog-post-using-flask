import sqlite3
import imagesDB


#returns all posts each post containing blog id, blog title, blog and author email
def getall():
    conn = sqlite3.connect('blog.db')
    cursor = conn.execute('SELECT blogs.blog_id, blog_title, blogs.blog, users.email FROM blogs JOIN users ON blogs.usr_id = users.id')
    posts = cursor.fetchall()
    conn.close()
    return posts


#returns post containing blog id, blog title, blog and author email
def getone(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.execute('SELECT blogs.blog_id, blog_title, blogs.blog, users.email FROM blogs JOIN users ON blogs.usr_id = users.id WHERE blogs.blog_id = ?', (post_id,))
    post = cursor.fetchone()
    cursor = conn.execute('SELECT comments.comment_id, comments.comment, users.email FROM comments JOIN users ON comments.user_id = users.id WHERE comments.blog_id = ?', (post_id,))
    comments = cursor.fetchall()
    conn.close()
    images = imagesDB.get_images(post_id)
    return post, comments, images


def insert(usr_id, blog_title, blog):
    conn = sqlite3.connect('blog.db')
    conn.execute('INSERT INTO blogs (usr_id, blog_title, blog) VALUES (?, ?, ?) ', (usr_id[0], blog_title, blog,))
    rows = conn.execute('Select * From blogs')
    conn.commit()
    arr = rows.fetchall()
    conn.close()
    return len(arr)


#returns cursor containing user blogs
def get_all_with_id(usr_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.execute('SELECT blogs.blog_id, blog_title, blogs.blog, users.email FROM blogs JOIN users ON blogs.usr_id = ?', (usr_id,))
    posts = cursor.fetchall()
    conn.close()
    return posts