import sqlite3

def init_db():

    conn = sqlite3.connect("../database/tickets.db")
    cursor = conn.cursor()

    # TICKETS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        subject TEXT,
        description TEXT,
        category TEXT,
        priority TEXT,
        status TEXT,
        agent_assigned TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolved_at TIMESTAMP
    )
    """)

    # HISTORY
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticket_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER,
        status TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # DEFAULT ADMIN
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username,email,password,role) VALUES (?,?,?,?)",
            ("admin", "admin@system.com", "admin123", "admin")
        )

    conn.commit()
    conn.close()