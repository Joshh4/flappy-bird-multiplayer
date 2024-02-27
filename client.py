import configparser
import os
import sys

path_dir = os.path.dirname(__file__)
path_data_dir = os.path.join(path_dir, "data")
path_config_file = os.path.join(path_data_dir, "config.cfg")

config = configparser.RawConfigParser()
config.read(path_config_file)

from scripts import network

server_ip = network.Utility.get_local_ip()
server_port_tcp = int(config.get("CLIENT", "SERVER_PORT_TCP", fallback=9884))
server_port_udp = int(config.get("CLIENT", "SERVER_PORT_UDP", fallback=9885))

client = network.HClient(
    server_ip=server_ip,
    server_port_tcp=server_port_tcp,
    server_port_udp=server_port_udp
)

print(f"Connecting to server at {server_ip} {server_port_tcp}, {server_port_udp}...")
client.connect()
while not client.ready:
    r = client.pump()

print("Connected! Running event loop")

while True:
    result = client.pump()
    
    for event_tcp in result.events_tcp:
        print("TCP event:", event_tcp)
    
    for event_udp in result.events_udp:
        print("UDP event:", event_udp)