# NetSentry // Traffic Monitor

> **Status**: OPERATIONAL  
> **Vibe**: Cyber / Surveillance / Minimalist

NetSentry is a containerized network traffic monitoring system designed to intercept and visualize packet flows between a client and a target server. It acts as a transparent gateway, capturing Ping (ICMP) and HTTP traffic in real-time.

## 🏗 Architecture

### Components
1.  **Client (The Intruder)**:
    -   Generates traffic (ICMP Pings, HTTP GET requests).
    -   Routes all traffic through the Gateway.
    -   IP: `172.20.0.11`
2.  **Gateway (The Sentinel)**:
    -   **Core**: Python FastAPI + Scapy.
    -   **Routing**: Enables IP Forwarding & NAT to bridge networks.
    -   **UI**: specific "Cyber" web dashboard on port `8000`.
    -   IPs: `172.20.0.10` (Client Side), `172.21.0.10` (Server Side).
3.  **Server (The Target)**:
    -   Simple web server hosting a "Target Acquired" page.
    -   IP: `172.21.0.11`

### Flow
`[Client] --(Network A)--> [Gateway] --(Network B)--> [Server]`

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- A terminal with `docker` permissions

### Deployment
1.  **Initialize System**:
    ```bash
    docker-compose up --build
    ```
2.  **Access Surveillance Feed**:
    Open your browser and navigate to:
    > **[http://localhost:8000](http://localhost:8000)**

3.  **Observe**:
    -   The Dashboard will constantly update with live packet captures.
    -   You will see `ICMP` packets (Pings).
    -   You will see `HTTP` packets (Web Requests).

## 🛠 Usage Scenarios

### 1. The Ping Test
The Client container is automatically pinging the server every few seconds.
-   **Look for**: Yellow `ICMP` entries in the log.
-   **Payload**: Standard ping byte patterns.

### 2. The HTTP Intercept
The Client periodically fetches the web page from the Server.
-   **Look for**: Blue `HTTP` entries.
-   **Payload**: You'll see headers like `GET / HTTP/1.1`.

## 📂 Project Structure
```
_net_sentry/
├── client/          # Traffic Generator sources
├── gateway/         # The core logic
│   ├── frontend/    # React "Cyber" UI
│   ├── main.py      # API & WebSocket Server
│   ├── sniffer.py   # Scapy Packet Capture
│   └── entrypoint.sh # Routing setup
├── server/          # Target server sources
└── docker-compose.yaml
```

## 🔒 Security & Performance
-   **Security**: Parameterized SQL queries used for logging. Minimal attack surface on Gateway.
-   **Performance**: Async WebSocket broadcasting. Packet capturing runs in background thread.
-   **Scalability**: DB schema designed for time-series inserts.

---
*Transmission Ended.*
