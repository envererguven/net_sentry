FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for Scapy and Network monitoring
# libpcap is essential for scapy
RUN apt-get update && apt-get install -y \
    libpcap-dev \
    tcpdump \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN pip install fastapi uvicorn scapy websockets requests

COPY . .

RUN chmod +x entrypoint.sh

# Expose API and WebSocket port
EXPOSE 8000

CMD ["./entrypoint.sh"]
