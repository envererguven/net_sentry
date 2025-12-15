import sqlite3
import json
import logging
from datetime import datetime

DB_PATH = "/app/data/packets.db"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("db")

def init_db():
    logger.info(f"Initializing Database at {DB_PATH}")
    try:
        conn = sqlite3.connect(DB_PATH)
        # Enable Write-Ahead Logging for better concurrency
        conn.execute("PRAGMA journal_mode=WAL;")
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
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize DB: {e}")

def save_packet(packet_data):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10) # 10s timeout for lock
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
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            logger.warning("Table 'packets' missing. Re-initializing...")
            init_db()
            # Retry once
            save_packet(packet_data)
        else:
            logger.error(f"DB Error: {e}")
    except Exception as e:
        logger.error(f"Error saving packet: {e}")

def get_recent_packets(limit=50):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM packets ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Error reading DB: {e}")
        return []
