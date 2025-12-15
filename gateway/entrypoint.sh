#!/bin/bash

# Enable IP Forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Setup Masquerading (NAT) so traffic coming from client (net_client_gateway) 
# going to server (net_gateway_server) is handled correctly.
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
# (Note: Interface names eth0/eth1 depend on docker startup order, standard usually eth0/eth1)
# We'll just mask everything leaving any interface to be safe for this demo.
iptables -t nat -A POSTROUTING -j MASQUERADE

# Start the application
uvicorn main:app --host 0.0.0.0 --port 8000
