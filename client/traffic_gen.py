import time
import random
import requests
import os
import subprocess
from pythonping import ping

TARGET_IP = os.getenv("TARGET_IP", "172.21.0.11")
GATEWAY_IP = os.getenv("GATEWAY_IP", "172.20.0.10")
TARGET_URL = f"http://{TARGET_IP}"

def setup_routing():
    print(f"[*] Setting up routing: {TARGET_IP} via {GATEWAY_IP}")
    try:
        # Add route to target subnet via gateway
        # Assuming typical /24 subnets. Target is 172.21.0.X, Gateway is 172.20.0.10
        target_subnet = ".".join(TARGET_IP.split(".")[:3]) + ".0/24"
        cmd = ["ip", "route", "add", target_subnet, "via", GATEWAY_IP]
        subprocess.run(cmd, check=True)
        print("[*] Route added successfully.")
    except Exception as e:
        print(f"[!] Failed to add route (might already exist or permission denied): {e}")

def generate_traffic():
    print(f"[*] Starting Traffic Generator targeting {TARGET_IP}...")
    while True:
        try:
            # 1. Ping the server
            print(f"[*] Pinging {TARGET_IP}...")
            # pythonping requires root, which we have in docker usually
            ping(TARGET_IP, count=1, verbose=True)
            
            # 2. HTTP GET request
            print(f"[*] Sending HTTP GET to {TARGET_URL}...")
            response = requests.get(TARGET_URL, timeout=5)
            print(f"[*] HTTP Status: {response.status_code}")

        except Exception as e:
            print(f"[!] Error: {e}")
        
        # Random sleep
        sleep_time = random.randint(2, 5)
        print(f"[*] Sleeping for {sleep_time}s...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    time.sleep(5) # Wait for gateway init
    setup_routing()
    generate_traffic()
