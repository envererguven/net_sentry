import sqlite3
import json
from datetime import datetime

DB_PATH = "/app/data/packets.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS packets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            src_ip TEXT,
            dst_ip TEXT,
            protocol TEXT,
            payload TEXT,
            captured_at DATETIME
        )
    """)
    conn.commit()
    conn.close()

def save_packet(packet_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO packets (src_ip, dst_ip, protocol, payload, captured_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        packet_data['src_ip'], 
        packet_data['dst_ip'], 
        packet_data['protocol'], 
        json.dumps(packet_data['payload']),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def get_recent_packets(limit=50):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM packets ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
