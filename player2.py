#Name: Yumeng Liu
#ID: 84419467

import socket
import sys
from gameboard import BoardClass
import pygame
from gamefunctions import *


def main() -> None:
    """The main function

    Creates the server
    Creates the game board for player 2
    Connects to player 1
    Begins the game

    """
    pygame.init()
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption("Player 2")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p2_board = BoardClass()
    p2_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        # Get host info from user
        host, port, name = getInfoScreen(screen)
        try:
            # Try to establish the server
            server_socket.bind((host, int(port)))
            server_socket.listen(1)

            # Waits for player 1 to conenct
            p2_s = serverEstablishedScreen(screen, server_socket)

            # Exchange user name
            p2_board.setOtherPlayerName(p2_s.recv(1024).decode())
            p2_board.setPlayerName(name)
            
            p2_s.send(name.encode('ascii'))
            break
        
        except Exception as e:
            # If the server failed to establish, ask user to try again
            print(e)
            if not optionScreen(screen, "Server failed to establish. Try again?"):
                pygame.quit()
                sys.exit(0)

    while True:
        try:
            # Start a game
            gameLoop(p2_board, p2_s, screen, True, 'o')

            # When the game is over, wait for player 1's response
            postGameScreen(screen, p2_s, p2_board)

        except Exception as e:
            # If the connection is broken during the game, end the program
            print(e)
            pygame.quit()
            break


if __name__ == "__main__":
    main()