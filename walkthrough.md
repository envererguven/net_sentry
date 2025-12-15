# NetSentry Walkthrough

## How to Test the System

This guide outlines how to verify that NetSentry is working as intended.

### Step 1: Boot the System
Run the following command in the project root:
```bash
docker-compose up --build -d
```
*Wait approximately 10-15 seconds for containers to initialize and the Client to set up its routing table.*

### Step 2: Access the Dashboard
Open **http://localhost:8000**.
-   You should see a dark, matrix-style interface.
-   Top right status should say **SYSTEM STATUS: CONNECTED**.

### Step 3: Verify Traffic
The Client is programmed to annoy the server indefinitely.

#### Scenario A: ICMP Ping
1.  Watch the "LIVE TRAFFIC FEED".
2.  Wait for a packet labeled **ICMP** (Yellow).
3.  Source should be `172.20.0.11` (Client).
4.  Destination should be `172.21.0.11` (Server).

#### Scenario B: HTTP Request
1.  Watch for **TCP** or **HTTP** (Blue).
2.  This indicates the Python script successfully routed an HTTP GET request through the gateway.

### Step 4: Manual Investigation (Optional)
If you want to manually trigger traffic:

1.  **Enter the Client Container**:
    ```bash
    docker exec -it net_sentry_client bash
    ```
2.  **Manual Ping**:
    ```bash
    ping -c 3 172.21.0.11
    ```
    *Observe the Dashboard immediately showing these new pings.*
3.  **Manual Curl**:
    ```bash
    curl http://172.21.0.11
    ```
    *Observe the HTTP packet capture.*

### Step 5: Shut Down
```bash
docker-compose down
```
