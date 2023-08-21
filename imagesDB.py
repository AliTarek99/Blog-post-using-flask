import sqlite3


def get_images(blogId):
    conn = sqlite3.connect('blog.db')
    images = conn.execute('Select images.filename FROM images JOIN blogs ON blogs.blog_id = images.blog_id and blogs.blog_id = ?', (blogId,))
    ret = images.fetchall()
    conn.close()
    return ret


def insert(filename, blog_id):
    conn = sqlite3.connect('blog.db')
    conn.execute("INSERT INTO images (blog_id, filename) VALUES (?, ?)", (blog_id, filename))
    conn.commit()
    conn.close()