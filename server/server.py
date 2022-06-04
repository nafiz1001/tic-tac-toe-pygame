#!/usr/bin/env python

import asyncio
import json
import os
import secrets

from websockets import server
from websockets.server import WebSocketServerProtocol
from websockets.legacy import protocol

import core.game as tictactoe

import json

VALUE = tuple[tictactoe.TicTacToe, set[WebSocketServerProtocol]]
JOIN: dict[str, VALUE] = {}
WATCH: dict[str, VALUE] = {}


async def error(websocket: WebSocketServerProtocol, message):
    """
    Send an error message.

    """
    event = {
        "type": "error",
        "message": message,
    }
    print(str(event))
    await websocket.send(json.dumps(event))


def game_data(game: tictactoe.TicTacToe):
    data = game.to_dict()
    return data


async def replay(game: tictactoe.TicTacToe, connected):
    """
    Broadcast all moves.

    """
    event = {"type": "replay", "data": game_data(game)}

    protocol.broadcast(connected, json.dumps(event))


async def play(
    websocket: WebSocketServerProtocol, game: tictactoe.TicTacToe, player, connected
):
    """
    Receive and process moves from a player.

    """
    print(f"Player {tictactoe.TicTacToe.symbol_to_str(player)} has joined the game!")

    async for message in websocket:
        # Parse a "play" event from the UI.
        event = json.loads(message)
        assert event["type"] == "play"
        x = event["x"]
        y = event["y"]

        print(event)

        try:
            if player == game.get_player():
                game.play((x, y))
                await replay(game, connected)
            else:
                raise RuntimeError(
                    f"the current player is {tictactoe.TicTacToe.symbol_to_str(game.get_player())}"
                )
        except Exception as exc:
            # Send an "error" event if the move was illegal.
            await error(websocket, str(exc))
            continue


async def start(websocket: WebSocketServerProtocol):
    """
    Handle a connection from the first player: start a new tictactoe.

    """
    # Initialize a Connect Four game, the set of WebSocket connections
    # receiving moves from this game, and secret access tokens.
    game = tictactoe.TicTacToe()
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    watch_key = secrets.token_urlsafe(12)
    WATCH[watch_key] = game, connected

    try:
        # Send the secret access tokens to the browser of the first player,
        # where they'll be used for building "join" and "watch" links.
        event = {
            "type": "init",
            "join": join_key,
            "watch": watch_key,
            "data": game_data(game),
        }
        await websocket.send(json.dumps(event))
        # Receive and process moves from the first player.
        await play(websocket, game, tictactoe.X, connected)
    finally:
        del JOIN[join_key]
        del WATCH[watch_key]


async def join(websocket: WebSocketServerProtocol, join_key):
    """
    Handle a connection from the second player: join an existing tictactoe.

    """
    # Find the Connect Four tictactoe.
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return

    # Register to receive moves from this tictactoe.
    connected.add(websocket)
    try:
        # Send the first move, in case the first player already played it.
        await replay(game, connected)
        # Receive and process moves from the second player.
        await play(websocket, game, tictactoe.O, connected)
    finally:
        connected.remove(websocket)


async def watch(websocket: WebSocketServerProtocol, watch_key):
    """
    Handle a connection from a spectator: watch an existing tictactoe.

    """
    # Find the Connect Four tictactoe.
    try:
        game, connected = WATCH[watch_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return

    # Register to receive moves from this tictactoe.
    connected.add(websocket)
    try:
        # Send previous moves, in case the game already started.
        await replay(websocket, game)
        # Keep the connection open, but don't receive any messages.
        await websocket.wait_closed()
    finally:
        connected.remove(websocket)


async def handler(websocket: WebSocketServerProtocol):
    """
    Handle a connection and dispatch it according to who is connecting.

    """
    # Receive and parse the "init" event from the UI.
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if "join" in event:
        # Second player joins an existing tictactoe.
        await join(websocket, event["join"])
    elif "watch" in event:
        # Spectator watches an existing tictactoe.
        await watch(websocket, event["watch"])
    else:
        # First player starts a new tictactoe.
        await start(websocket)


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()

    port = int(os.environ.get("PORT", "8001"))
    async with server.serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
