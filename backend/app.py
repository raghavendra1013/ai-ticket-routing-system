from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText

from database import init_db
from model import predict_ticket
from router import assign_agent

from router import get_agent_queue, get_all_queues
from router import can_agent_take_ticket, get_next_ticket_for_agent

app = Flask(__name__)
CORS(app)

init_db()

otp_store = {}

@app.route("/")
def home():
    return "AI Ticket Router Running"

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500


# ================= OTP =================
@app.route("/send_otp", methods=["POST"])
def send_otp():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("../database/tickets.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, email FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    user_email = user[1]

    otp = str(random.randint(100000, 999999))
    otp_store[username] = otp

    sender_email = "aiticketrouter@gmail.com"
    sender_password = "hnpysyfslvovtjix"

    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "Login OTP"
    msg["From"] = sender_email
    msg["To"] = user_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()
    except Exception as e:
        return jsonify({"error": f"Email failed: {str(e)}"}), 500

    return jsonify({"message": "OTP sent to email"})


@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.json
    username = data.get("username")
    otp = data.get("otp")

    if otp_store.get(username) != otp:
        return jsonify({"error": "Invalid OTP"}), 400

    conn = sqlite3.connect("../database/tickets.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, email FROM users WHERE username=?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()

    otp_store.pop(username, None)

    return jsonify({
        "role": user[0],
        "email": user[1]
    })


# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("../database/tickets.db")
    cursor = conn.cursor()

    if username == "admin" and password == "admin123":
        conn.close()
        return jsonify({"role": "admin", "email": "admin@system.com"})

    cursor.execute(
        "SELECT role, email FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "role": user[0],
            "email": user[1]
        })
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# ================= SIGNUP =================
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not password or not email:
        return jsonify({"error": "All fields required"}), 400

    if "@" not in email:
        return jsonify({"error": "Invalid email"}), 400

    conn = sqlite3.connect("../database/tickets.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    cursor.execute(
        "INSERT INTO users (username,email,password,role) VALUES (?,?,?,?)",
        (username, email, password, "customer")
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Signup successful"})


# ================= CUSTOMER DASHBOARD =================
@app.route("/customer_stats", methods=["POST"])
def customer_stats():
    data = request.json
    email = data.get("email")

    conn = sqlite3.connect("../database/tickets.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE email=?", (email,))
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE email=? AND status='Resolved'", (email,))
    resolved = cursor.fetchone()[0]

    cursor.execute("SELECT category, COUNT(*) FROM tickets WHERE email=? GROUP BY category", (email,))
    categories = cursor.fetchall()

    cursor.execute("SELECT priority, COUNT(*) FROM tickets WHERE email=? GROUP BY priority", (email,))
    priorities = cursor.fetchall()

    cursor.execute("SELECT status, COUNT(*) FROM tickets WHERE email=? GROUP BY status", (email,))
    status_data = cursor.fetchall()

    conn.close()

    return jsonify({
        "total": total,
        "resolved": resolved,
        "categories": categories,
        "priorities": priorities,
        "status": status_data
    })


# ================= ADMIN DASHBOARD =================
@app.route("/ticket_stats", methods=["GET"])
def ticket_stats():
    try:
        conn = sqlite3.connect("../database/tickets.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM tickets")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='Open'")
        open_tickets = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tickets WHERE status='Resolved'")
        resolved_tickets = cursor.fetchone()[0]

        cursor.execute("SELECT category, COUNT(*) FROM tickets GROUP BY category")
        categories = cursor.fetchall()

        cursor.execute("SELECT priority, COUNT(*) FROM tickets GROUP BY priority")
        priorities = cursor.fetchall()

        cursor.execute("SELECT agent_assigned, COUNT(*) FROM tickets GROUP BY agent_assigned")
        agents = cursor.fetchall()

        cursor.execute("""
            SELECT agent_assigned, COUNT(*) 
            FROM tickets 
            WHERE status='Resolved'
            GROUP BY agent_assigned
        """)
        agent_performance = cursor.fetchall()

        cursor.execute("""
            SELECT AVG(
                CASE 
                    WHEN resolved_at IS NOT NULL 
                    THEN (julianday(resolved_at) - julianday(created_at)) * 24
                END
            ) FROM tickets
        """)
        avg_resolution_time = cursor.fetchone()[0] or 0

        conn.close()

        return jsonify({
            "total": total,
            "open": open_tickets,
            "resolved": resolved_tickets,
            "categories": categories,
            "priorities": priorities,
            "agents": agents,
            "agent_performance": agent_performance,
            "avg_resolution_time": avg_resolution_time
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= QUEUE STATUS =================
@app.route("/full_queue_status", methods=["GET"])
def full_queue_status():
    try:
        return jsonify(get_all_queues())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= PROCESS NEXT =================
@app.route("/process_next/<agent>", methods=["POST"])
def process_next(agent):
    try:
        if not can_agent_take_ticket(agent):
            return jsonify({"error": "Agent at max capacity"}), 400

        ticket_id = get_next_ticket_for_agent(agent)

        if not ticket_id:
            return jsonify({"message": "No tickets in queue"})

        return jsonify({"message": f"Ticket {ticket_id} moved to In Progress"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= ✅ NEW: MY TICKETS =================
@app.route("/my_tickets", methods=["POST"])
def my_tickets():
    try:
        data = request.json
        email = data.get("email")

        if not email:
            return jsonify({"error": "Email required"}), 400

        conn = sqlite3.connect("../database/tickets.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, subject, category, priority, status, created_at
            FROM tickets
            WHERE email=?
            ORDER BY created_at DESC
        """, (email,))

        rows = cursor.fetchall()
        conn.close()

        return jsonify(rows)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= TICKETS =================
@app.route("/tickets", methods=["GET"])
def get_tickets():
    try:
        conn = sqlite3.connect("../database/tickets.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM tickets
        ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return jsonify([dict(row) for row in rows])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= UPDATE =================
@app.route("/update_status", methods=["POST"])
def update_status():
    valid_status = ["Open", "In Progress", "Resolved", "Escalated"]

    data = request.json
    ticket_id = data.get("id")
    status = data.get("status")

    if status not in valid_status:
        return jsonify({"error": "Invalid status"}), 400

    conn = sqlite3.connect("../database/tickets.db")
    cursor = conn.cursor()

    if status == "Resolved":
        cursor.execute("""
            UPDATE tickets 
            SET status=?, resolved_at=CURRENT_TIMESTAMP 
            WHERE id=?
        """, (status, ticket_id))
    else:
        cursor.execute("UPDATE tickets SET status=? WHERE id=?", (status, ticket_id))

    cursor.execute("""
    INSERT INTO ticket_history (ticket_id, status)
    VALUES (?,?)
    """, (ticket_id, status))

    conn.commit()
    conn.close()

    return jsonify({"message": "Updated"})


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)