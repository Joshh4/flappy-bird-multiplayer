import configparser
import os

path_dir = os.path.dirname(__file__)
path_data_dir = os.path.join(path_dir, "data")
path_config_file = os.path.join(path_data_dir, "config.cfg")

config = configparser.RawConfigParser()
config.read(path_config_file)

from scripts import network
from scripts import serverclasses

server_ip = network.Utility.get_local_ip()
server_port_tcp = int(config.get("SERVER", "SERVER_PORT_TCP", fallback=9884))
server_port_udp = int(config.get("SERVER", "SERVER_PORT_UDP", fallback=9885))

system = network.HSystem(
    ip=server_ip,
    port_tcp=server_port_tcp,
    port_udp=server_port_udp,
    client_model=serverclasses.ClientModel
)

game_manager = serverclasses.ServerGameManager()

print(f"Server is active at {server_ip}")

while True:
    result = system.pump()

    for client in result.new_clients:
        print("New client:", client.addr_tcp, client.cid)

    for client in result.disconnected_clients:
        print("Disconnected client:", client.addr_tcp, client.cid)
    
    for event_tcp in result.events_tcp:
        print("TCP event:", event_tcp)
    
    for event_udp in result.events_udp:
        print("UDP event:", event_udp)