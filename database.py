import sqlite3


def create():
    conn = sqlite3.connect("Attendance.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS student (roll_no INT, name VARCHAR(100))")
    conn.commit()
    conn.close()


def insert(roll, name):
    conn = sqlite3.connect("Attendance.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO student VALUES (?, ?)", (roll, name))
    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect("Attendance.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM student ORDER BY roll_no")
    rows = cur.fetchall()
    conn.close()
    return rows

create()
