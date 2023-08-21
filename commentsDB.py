import sqlite3


def insert(usr_id, post_id, comment):
    conn = sqlite3.connect('blog.db')
    conn.execute('INSERT INTO comments (user_id, blog_id, comment) VALUES (?, ?, ?)', (usr_id[0], post_id, comment))
    conn.commit()
    conn.close()
