import asyncio
import sys
import game as tictactoe
import ai as tictactoe_ai
import client as tictactoe_client

ttt = tictactoe.TicTacToe()
ai = tictactoe_ai.AI()


def ai_play():
    max_player = client.symbol == tictactoe.X
    point = ai.monte_carlo_method(ttt, max_player, 50)
    client.set_next_move(*point)


def play(point, symbol):
    ttt.play(point)
    if client.symbol != symbol:
        ai_play()


def replay(curr_board: dict, curr_player):
    for (x, y), p in curr_board.items():
        if p != tictactoe.EMPTY_CELL:
            ttt.board[(x, y)] = p
    if client.symbol == curr_player:
        ai_play()


def win(player, strats):
    print("win")


def draw():
    print("draw")


client = tictactoe_client.Client(play, replay, win, draw)
asyncio.run(client.start("ws://localhost:8001", sys.argv))
