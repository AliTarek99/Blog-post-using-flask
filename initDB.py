import sqlite3

# Create a new SQLite database file called 'blog.db'
conn = sqlite3.connect('blog.db')

# Create a new table for the users
conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT)')
# Create a new table for the blogs
conn.execute('CREATE TABLE blogs (blog_id INTEGER PRIMARY KEY AUTOINCREMENT, usr_id INTEGER, blog_title TEXT, blog TEXT, FOREIGN KEY (usr_id) REFERENCES users(id))')
# Create a new table for the comments
conn.execute('CREATE TABLE comments (comment_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, blog_id INTEGER, comment TEXT, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (blog_id) REFERENCES blogs(blog_id))')

conn.execute("CREATE TABLE images (id INTEGER PRIMARY KEY AUTOINCREMENT, blog_id INTEGER, filename TEXT, FOREIGN KEY (blog_id) REFERENCES blogs(blog_id))")
# Commit the changes and close the connection
conn.commit()
conn.close()