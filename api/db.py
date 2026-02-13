import sqlite3

conn = sqlite3.connect("/tmp/music.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tracks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
file TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY
)
""")

conn.commit()

def add_user(uid):
    cur.execute("INSERT OR IGNORE INTO users VALUES(?)",(uid,))
    conn.commit()

def users():
    return [x[0] for x in cur.execute("SELECT id FROM users")]

def add_track(name,file):
    cur.execute("INSERT INTO tracks(name,file) VALUES(?,?)",(name,file))
    conn.commit()

def list_tracks():
    return [dict(id=r[0],name=r[1],file=r[2])
            for r in cur.execute("SELECT * FROM tracks")]
