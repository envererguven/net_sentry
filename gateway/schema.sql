CREATE TABLE IF NOT EXISTS packets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    src_ip TEXT,
    dst_ip TEXT,
    protocol TEXT,
    payload TEXT,
    captured_at DATETIME
);

CREATE INDEX idx_packets_timestamp ON packets(timestamp);
