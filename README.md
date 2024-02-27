# Flappy Bird Multiplayer

This project initially started as an experiment making use of my network system, which is an event-based hybrid TCP and UDP setup.

This repository is currently in development and will not work as expected right now. When everything is completed this README will be updated with running instructions.

# Technical Requirements

Clients can connect to the server and host or join a game.

## How The Game Works

### Hosting A Game

For a client hosting a game, they have access to a Start button. Every client in a game can see a list of other clients in that same game. Games can also be password protected.

### On Game Start

On game start, all clients are informed that the game has started, and all clients are given the random seed for the specific round (To ensure all clients have the same generation of pipes so everything lines up visually).

### During The Game

Each client sends its position to the server as an `update-position` packet. This packet simply contains the position, rotation, and velocity for the specific client. The server then packs all client update-position packets into one large packet and sends that to each client. Client death events is a tcp packet, called `client-lifestate`, with a `tag` of `DEAD` or `ALIVE`.

When all clients have died, the round ends and a podium is shown with fun confetti particles.

## Other Details

Clients have the following attributes:

* Wearables they can configure, such as hats or glasses
* Colour of their own bird, out of some limited selection
* Appearance / shape of their own bird (Does not affect hitbox)

These cosmetics can be collected through the game possibly through some sort of simple client-sided store.
