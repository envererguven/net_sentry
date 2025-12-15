FROM python:3.9-slim

WORKDIR /app

# Install ping utility, iproute2 (for ip command), and python libraries
RUN apt-get update && apt-get install -y iputils-ping iproute2 && rm -rf /var/lib/apt/lists/*
RUN pip install requests pythonping

COPY traffic_gen.py .

CMD ["python", "traffic_gen.py"]
