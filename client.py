import configparser
import os

# Gather required filepaths

path_dir = os.path.dirname(__file__)
path_data_dir = os.path.join(path_dir, "data")
path_images_dir = os.path.join(path_data_dir, "images")
path_config_file = os.path.join(path_data_dir, "config.cfg")
path_font_file = os.path.join(path_images_dir, "font.png")

# Load the config file

config = configparser.RawConfigParser()
config.read(path_config_file)

# Define application state constant values

class ApplicationState:
    CONNECTING = 0
    MAIN_MENU = 1

# Import pygame and other requirements

import pygame
from pygame.locals import *
from scripts import network
from scripts import spritefont
from scripts import ui
import ui_loader

# Initialize constants retrieved from config

server_ip = network.Utility.get_local_ip()
server_port_tcp = int(config.get("CLIENT", "SERVER_PORT_TCP", fallback=9884))
server_port_udp = int(config.get("CLIENT", "SERVER_PORT_UDP", fallback=9885))

# Initialize pygame, display, fonts, and other images

pygame.init()
screen = pygame.Surface((300, 200))
display = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Flappy Friends")

font_main = spritefont.SpriteFont(
    surface=pygame.image.load(path_font_file).convert(),
    colour=(255, 255, 255))

application_state = ApplicationState.CONNECTING

ui_manager = ui.UiManager()
ui_loader.init_ui(
    manager=ui_manager,
    path_font_file=path_font_file)

ui_manager.set_page("connecting")




# Initialize the client

client = network.HClient(
    server_ip=server_ip,
    server_port_tcp=server_port_tcp,
    server_port_udp=server_port_udp)

# Start a connection to the server

print(f"Connecting to server at {server_ip} {server_port_tcp}, {server_port_udp}...")
client.connect()

# Main event loop

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(61) * 0.001

    result = client.pump()
    pygame_events = pygame.event.get()

    # Process "common" events

    for event in pygame_events:
        if event.type == pygame.QUIT:
            running = False
    
    for event_tcp in result.events_tcp:
        print("TCP event:", event_tcp)
    
    for event_udp in result.events_udp:
        print("UDP event:", event_udp)
    
    # Allow the ui manager to process inputs
    
    ui_manager.update(pygame_events)
    
    # Draw screen and handle updates depending on the application state
    
    screen.fill((40,45,50))

    ui_manager.render(screen)

    if ui_manager.current_page_identifier == "connecting":
        if client.ready:
            ui_manager.set_page("main")

    display.blit(pygame.transform.scale(screen, (900, 600)), (0,0))

    pygame.display.flip()

pygame.quit()