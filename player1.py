#Name: Yumeng Liu
#ID: 84419467

import socket
import sys
from gameboard import BoardClass
import pygame
from gamefunctions import *

    
def main() -> None:
    """The main function

    Creates the game board for player 1.
    Connects to player 2.
    Begins the game

    """
    pygame.init()
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption("Player 1")
    p1_board = BoardClass()
    p1_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        # Get host info from user
        host, port, name = getInfoScreen(screen)
        try:
            # Try to connect to player 2 based on the host info
            p1_s.connect((host, int(port)))

            # Exchange user name
            p1_board.setPlayerName(name)
            p1_s.send(name.encode('ascii'))
            p1_board.setOtherPlayerName(p1_s.recv(1024).decode())
            break
        except Exception as e:
            # If connection fails, ask user to reconnect
            print(e)
            if not optionScreen(screen, 'Failed to connect. Try Again?'):
                sys.exit(0)
            
    while True:
        try:
            # Start a game
            gameLoop(p1_board, p1_s, screen, False, 'x')
            
            # When the game is over, ask player 1 to play again
            if optionScreen(screen, 'Game over. Play Again?') == False:
                p1_s.send('Fun Times'.encode('ascii'))
                resultScreen(screen, p1_board)
                break

            p1_s.send('Play Again'.encode('ascii'))

        except Exception as e:
            # If the connection is broken during the game, end the program
            print(e)
            break

    p1_s.close()



if __name__ == "__main__":
    main()