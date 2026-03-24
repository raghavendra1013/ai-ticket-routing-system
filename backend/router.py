import sqlite3

agent_pools = {
    "technical issue": ["Ram", "Sunny"],
    "billing issue": ["Rishi", "Shashank"],
    "account issue": ["Ankith", "Pavan"],
    "feature request": ["Mani", "Ravi"]
}

def assign_agent(category, priority):

    category = category.lower()
    agents = agent_pools.get(category, ["General Agent"])

    # HIGH priority → assign expert (first agent)
    if priority == "high":
        return agents[0]

    conn = sqlite3.connect("../database/tickets.db")
    cursor = conn.cursor()

    agent_load = {}

    for agent in agents:
        cursor.execute("""
            SELECT COUNT(*) FROM tickets 
            WHERE agent_assigned=? AND status!='Resolved'
        """, (agent,))
        agent_load[agent] = cursor.fetchone()[0]

    conn.close()

    return min(agent_load, key=agent_load.get)

#  QUEUE SYSTEM (EXISTING)

def get_agent_queue(agent):
    conn = sqlite3.connect("../database/tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, subject, priority, status, created_at
        FROM tickets
        WHERE agent_assigned=? AND status!='Resolved'
        ORDER BY 
        CASE priority
            WHEN 'high' THEN 1
            WHEN 'medium' THEN 2
            WHEN 'low' THEN 3
        END,
        created_at ASC
    """, (agent,))

    data = cursor.fetchall()
    conn.close()

    queue = []
    for i, t in enumerate(data, start=1):
        queue.append({
            "position": i,
            "id": t[0],
            "subject": t[1],
            "priority": t[2],
            "status": t[3],
            "created_at": t[4]
        })

    return queue


def get_all_queues():
    all_data = {}

    for category in agent_pools:
        for agent in agent_pools[category]:
            all_data[agent] = get_agent_queue(agent)

    return all_data

# NEW: CAPACITY SYSTEM

MAX_TICKETS_PER_AGENT = 3


def get_active_ticket_count(agent):
    conn = sqlite3.connect("../database/tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM tickets
        WHERE agent_assigned=? AND status='In Progress'
    """, (agent,))

    count = cursor.fetchone()[0]
    conn.close()

    return count


def can_agent_take_ticket(agent):
    return get_active_ticket_count(agent) < MAX_TICKETS_PER_AGENT


def get_next_ticket_for_agent(agent):
    conn = sqlite3.connect("../database/tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM tickets
        WHERE agent_assigned=? AND status='Open'
        ORDER BY 
        CASE priority
            WHEN 'high' THEN 1
            WHEN 'medium' THEN 2
            WHEN 'low' THEN 3
        END,
        created_at ASC
        LIMIT 1
    """, (agent,))

    ticket = cursor.fetchone()

    if not ticket:
        conn.close()
        return None

    ticket_id = ticket[0]

    
    cursor.execute("""
        UPDATE tickets
        SET status='In Progress'
        WHERE id=?
    """, (ticket_id,))

    cursor.execute("""
        INSERT INTO ticket_history (ticket_id, status)
        VALUES (?,?)
    """, (ticket_id, "In Progress"))

    conn.commit()
    conn.close()

    return ticket_id