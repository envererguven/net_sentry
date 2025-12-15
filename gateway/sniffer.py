from scapy.all import sniff, IP, TCP, ICMP, Raw
from database import save_packet
import asyncio
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global queue for WebSocket broadcasting
packet_queue = asyncio.Queue()

def packet_callback(packet):
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        proto = "UNKNOWN"
        payload = ""

        # Filter for ICMP (Ping)
        if ICMP in packet:
            proto = "ICMP"
            payload = f"Type: {packet[ICMP].type} Code: {packet[ICMP].code}"
        
        # Filter for TCP (HTTP usually on 80)
        elif TCP in packet:
            proto = "TCP"
            if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                proto = "HTTP"
            
            # Try to decode Raw payload
            if Raw in packet:
                try:
                    payload = packet[Raw].load.decode('utf-8', errors='ignore')
                    # Truncate for display if too long
                    payload = (payload[:100] + '...') if len(payload) > 100 else payload
                except:
                    payload = "[Binary Data]"
        
        # Construct packet data object
        pkt_data = {
            "src_ip": src,
            "dst_ip": dst,
            "protocol": proto,
            "payload": payload
        }

        # Only process interesting traffic (exclude internal Docker DNS/ARP noise if possible, but IP filter helps)
        if proto in ["ICMP", "HTTP", "TCP"]:
            # Save to DB (Synchronous call, might want to optimize later)
            save_packet(pkt_data)
            
            # Put in queue for WebSockets (Need to run this in a way that doesn't block scapy)
            # Since scapy's sniff is blocking, we usually push to a thread-safe queue or use asyncio loop.call_soon_threadsafe
            # For simplicity in this architecture, we'll append to a list or simple queue that the async loop checks, 
            # Or better, we just print/log here and let the async loop pick it up from a shared resource if we were truly parallel.
            # HOWEVER, `sniff` blocking the main thread prevents FastAPI from running if in the same process.
            # Solution: Run sniff in a separate thread.
            
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.call_soon_threadsafe(packet_queue.put_nowait, pkt_data)
            except RuntimeError:
                 # If no loop (shouldn't happen in the designed flow), just ignore push
                 pass

def start_sniffer(interface="eth0"):
    logger.info(f"Starting Sniffer on {interface}...")
    # filter: capture IP packets
    sniff(iface=interface, prn=packet_callback, filter="ip", store=False)
