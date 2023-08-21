import hashlib
import sqlite3
from enums import State


def hash_password(password):
    # Encode the password as UTF-8
    password_bytes = password.encode('utf-8')
    # Create a new SHA-256 hash object
    hash_object = hashlib.sha256()
    # Update the hash object with the password bytes
    hash_object.update(password_bytes)
    # Get the hash digest as a hex string
    hash_hex = hash_object.hexdigest()
    # Return the hashed password
    return hash_hex


def insert(email, password):
    conn = sqlite3.connect('blog.db')
    cursor = conn.execute('Select users.email From users Group By email Having email = ?', (email,))
    cnt = len(cursor.fetchall())
    conn.close()
    if cnt > 0:
        return State.duplicate
    elif len(password) < 8:
        return State.short_pass
    else:
        conn = sqlite3.connect('blog.db')
        hashed_password = hash_password(password)
        conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()
        conn.close()
        return State.valid


def verify(email, password):
    conn = sqlite3.connect('blog.db')
    hashed_password = hash_password(password)
    usr_id = conn.execute('Select users.id From users where users.email = ? and users.password = ?', (email, hashed_password,))
    rows = usr_id.fetchall()
    conn.close()
    if len(rows) == 1:
        return State.valid
    else:
        return State.notfound


def getmail(usr_id):
    conn = sqlite3.connect('blog.db')
    mail = conn.execute('Select users.email From users where users.id = ?', (usr_id,))
    rows = mail.fetchall()
    conn.close()
    if len(rows) == 1:
        return rows[0]
    else:
        return State.notfound


def getId(email):
    conn = sqlite3.connect('blog.db')
    mail = conn.execute('Select users.id From users where users.email = ?', (email,))
    arr = mail.fetchone()
    conn.close()
    return arr
