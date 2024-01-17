import pygame
import gui
import sys
from gameboard import BoardClass
import socket
import time

def getInfoScreen(screen: pygame.Surface) -> tuple[str, str, str]:
    """A screen that gets the host, port, and player name
    
    Args:
        screen: the screen to draw on
    
    Returns:
        A tuple that contains the host, port, and player name in that order

    """

    # Create two entry boxes and a submit button
    host_entry = gui.EntryBox(screen, 20, 20, 300, 50, 'Host:')
    port_entry = gui.EntryBox(screen, 20, 100, 300, 50, "Port:")
    name_entry = gui.EntryBox(screen, 20, 180, 300, 50, 'Name:')
    submit_button = gui.Button(screen, "Submit", 20, 260, 30)

    # Manages framerate
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))

        # Handles event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            host_entry.handleEvent(event)
            port_entry.handleEvent(event)
            name_entry.handleEvent(event)
            submit_button.handleEvent(event)
        
        # Checks if the button is pressed
        if submit_button.isPressed():
                host_ip = host_entry.get()
                port = port_entry.get()
                name = name_entry.get()

                if host_ip == '' or name == '' or port == '':
                    continue
                
                return (host_ip, port, name)

        # Draw the object and update the screen
        host_entry.draw_me()
        port_entry.draw_me()
        name_entry.draw_me()
        submit_button.draw_me()

        pygame.display.update()
        clock.tick(30)

def optionScreen(screen: pygame.Surface, msg: str) -> None:
    """"An option screen that prompts the user for a yes or no answer
    
    Args:
        screen: the screen to draw on
        msg: the message that displays on the screen

    """
    # Manages framerate
    clock = pygame.time.Clock()

    # Creates a text object, yes button, no button
    msg = gui.Text(screen, 20, 20, msg)
    y_button = gui.Button(screen, 'Yes', 20, 60, 30)
    n_button = gui.Button(screen, 'No', 70, 60, 30)

    # Renders the screen
    while True:
        screen.fill((0, 0, 0))

        # Handles user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            y_button.handleEvent(event)
            n_button.handleEvent(event)
        
        if y_button.isPressed():
            return True

        if n_button.isPressed():
            return False
        
        # Draws the objects and updates the screen
        msg.draw_me()
        y_button.draw_me()
        n_button.draw_me()
        pygame.display.update()
        clock.tick(30)

def checkBlocks(blocks: list[list[gui.Block]], event: pygame.event.Event) -> (tuple[int, int] | None):
    """Handle the events for all the blocks
    
    Args:
        blocks: the blocks to check
        event: the event to handle
    
    Returns:
        A tuple that contains the indices of the block that was clicked

    """
    for i in range(3):
        for j in range(3):
            if blocks[i][j].handleEvent(event):
                return (i, j)
    
    return None

def drawBoard(screen: pygame.Surface, blocks: list[list[gui.Block]]) -> None:
    """Draw the tic-tac-toe board and update the screen
    
    Args:
        screen: the screen to draw on
        blocks: the blocks to draw

    """
    for i in blocks:
        for j in i:
            j.draw_me()

    # Vertical lines
    for i in range(4):
        pygame.draw.line(screen, (255, 255, 255), (10 + i * 193, 10), (10 + i * 193, 589), 2)
    
    # Horizontal lines
    for i in range(4):
        pygame.draw.line(screen, (255, 255, 255), (10, 10 + i * 193), (589, 10 + i * 193), 2)         
            
    pygame.display.update()

def gameLoop(player_board: BoardClass, player_s: socket.socket, screen: pygame.Surface, receive: bool, move: str) -> None:
    """The game loop
    
    Args:
        player_board: the player's gameBoard
        player_s: the player's socket
        screen: the screen to draw on
        receive: whether the player starts by receiving
        move: the player's move, either 'x' or 'o'

    """
    blocks = [[gui.Block(screen, 10 + x * 193, 10 + y * 193, 193) for y in range(3)] for x in range(3)]
    player_board.resetGameBoard()
    msg = gui.Text(screen, 10, 650, '')
    receiving = receive
    clock = pygame.time.Clock()
    ggs = gui.Text(screen, 400, 650, player_board.getResult())
    other_player_move = ''
    player_move = move
    if player_move == 'o':
        other_player_move = 'x'
    else:
        other_player_move = 'o'

    while True:
        if receiving:
            screen.fill((0, 0, 0))
            msg.update(player_board.getOtherPlayerName() + "\'s move")
            drawBoard(screen, blocks)

            #Receive move
            data = player_s.recv(1)
            x_cor = int(data.decode('ascii'))
            data = player_s.recv(1)
            y_cor = int(data.decode('ascii'))

            player_board.updateGameBoard((x_cor, y_cor), other_player_move, player_board.getOtherPlayerName())
            if other_player_move == 'o':
                blocks[x_cor][y_cor].drawCircle()
            else:
                blocks[x_cor][y_cor].drawX()

            #Check winning condition, end the game if the game is over
            if player_board.checkGameEnd():
                drawBoard(screen, blocks)
                ggs.update(player_board.getResult())
                pygame.display.update()
                time.sleep(2)
                return
            receiving = False
        
        if receiving == False:
            screen.fill((0, 0, 0))
            msg.update("Your move")
            drawBoard(screen, blocks)

            # Check event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    player_s.close()
                    sys.exit(0)

                coord = checkBlocks(blocks, event)
                if coord != None:
                    # Send the valid move
                    player_s.send(str(coord[0]).encode('ascii'))
                    player_s.send(str(coord[1]).encode('ascii'))

                    # Update board
                    player_board.updateGameBoard(coord, player_move, player_board.getPlayerName())
                    if player_move == 'o':
                        blocks[coord[0]][coord[1]].drawCircle()
                    else:
                        blocks[coord[0]][coord[1]].drawX()

                    #Check winning condition, end the game if the game is over
                    if player_board.checkGameEnd():
                        drawBoard(screen, blocks)
                        ggs.update(player_board.getResult())
                        pygame.display.update()
                        time.sleep(2)
                        return
                    
                    receiving = True

        pygame.display.update()       
        clock.tick(30)

def resultScreen(screen: pygame.Surface, player_board: BoardClass) -> None:
    """The screen that shows the result
    
    Args:
        screen: the screen to draw on
        player_board: the player's board

    """

    # Splits the stats returned by the player board by lines
    result_lines = player_board.computeStats().split('\n')
    texts = [gui.Text(screen, 20, 40 * i, result_lines[i]) for i in range(len(result_lines))]
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        for i in texts:
            i.draw_me()
        
        pygame.display.update()

def postGameScreen(screen: pygame.Surface, p2_s: socket.socket, p2_board: BoardClass) -> None:
    """The waiting screen for player 2 after the game is over

    Attributes:
        screen: the screen to draw on
        p2_s: the player 2's socket
        p2_board: player 2's game board

    """
    msg = gui.Text(screen, 20, 20, "Waiting for " + p2_board.getOtherPlayerName() + "\'s response")
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        msg.draw_me()
        pygame.display.update()
        if p2_s.recv(10).decode('ascii') != 'Play Again':
            p2_s.close()
            resultScreen(screen, p2_board)
        else:
            return
        pygame.display.udpate()
        clock.tick(30)

def serverEstablishedScreen(screen: pygame.Surface, server_socket: socket.socket) -> socket.socket:
    """The screen that shows the sever is successfull established

    Args:
        screen: the screen to draw on
        server_socket: the server socket that will accept the connection

    Returns:
        A socket that represents the conenction to the client
    """
    msg = gui.Text(screen, 20, 20, "Server established. Waiting for player 1 connection")
    while True:
        screen.fill((0, 0, 0))
        msg.draw_me()
        pygame.display.update()
        return server_socket.accept()[0]