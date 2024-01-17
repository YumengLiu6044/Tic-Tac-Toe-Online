class BoardClass:
    """The Tic-Tac-Toe game board

        Attributes:
            player_name: Player's user name
            other_player_name: The other player's name
            number_of_last_player: User name of the last player to have a turn
            number_of_win: Number of times the player won
            number_of_ties: Number of tied games
            number_of_losses: Number of times the player lost
            games_played: the total number of games played
            board: the tic-tac-toe board represented by a 2D array. All values are initialized as 0
    """
    
    def __init__(self) -> None:
        """The tic-tac-toe game board
        """
        self.player_name = ''
        self.other_player_name = ''
        self.name_of_last_player = ''
        self.number_of_win = 0
        self.number_of_ties = 0
        self.number_of_losses = 0
        self.games_played = 0
        self.result = ''
        self.board = [[0,0,0] for _ in range(3)]

    def updateGamesPlayed(self) -> None:
        """Updates how many games were played
        
        Updates the total number of games played by adding the
        total number of wins, losses, and ties.

        """
        self.games_played = self.number_of_losses + self.number_of_ties + self.number_of_win

    def resetGameBoard(self) -> None:
        """Resets the game board

        Reinitialize the board by setting it to a 3x3 2D array of 0s
        
        """
        self.board = [[0,0,0] for _ in range(3)]

    def updateGameBoard(self, index : tuple, move : str, player_name: str) -> None:
        """Updates the game board

        Updates the game board based on the move a player made.
        Update the name of the last player to make a move

        Args:
            index: the location of the move
            move: the move that was made, either 'x' or 'o'
            player_name: the name of the player that made the move

        """
        self.board[index[0]][index[1]] = move
        self.name_of_last_player = player_name

    def isWinner(self) -> bool:
        """Checks if the current game board has a winner

        Check the rows, columns, and diagonals if there are same three
        characters that are not 0 
        If so, set winner to a non-empty string.
        Update the wins and losses. If the last player to make a move is
        the player, then it's a win, otherwise it's a lose.

        Returns:
            A bool value indicating if there is a winner.
        
        """
        winner = ''
        # Check rows
        for i in range(3):
            if self.board[i].count('x') == 3:
                winner = 'p1'
            if self.board[i].count('o') == 3:
                winner = 'p2'
        
        # Check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
                winner = 'someone'
        
        # Check diagonal
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            winner = 'someone'
        if self.board[2][0] == self.board[1][1] == self.board[0][2] != 0:
            winner = 'someone'
        
        # Update the game score and return True
        if winner != '':
            if self.name_of_last_player == self.player_name:
                self.result = 'You have won'
                self.number_of_win += 1
            else:
                self.result = 'You have lost'
                self.number_of_losses += 1
            return True

        # Return False if nobody is winning
        return False


    def boardIsFull(self) -> bool:
        """Checks if the board is full

        Checks if the board is full by checking if there is any 0 left,
        which is the default value. Update the tie count if the
        board is full

        Returns:
            A bool value that indicates if the board is full
        """
        for i in self.board:
            if 0 in i:
                return False
        self.result = 'Tie'
        self.number_of_ties += 1
        return True

    def computeStats(self) -> str:
        """Return the game statistic as a string

        Appends each of the following on a new line of the returned string:
        the players user name
        the user name of the last person to make a move
        the number of games
        the number of wins
        the number of losses
        the number of ties

        Returns:
            the string representation of the game stats

        """
        self.updateGamesPlayed()
        result = "Player name: {0}\n".format(self.player_name)
        result += "Last player to make a move: {0}\n".format(self.name_of_last_player)
        result += "Number of games: {0}\n".format(self.games_played)
        result += "Number of wins: {0}\n".format(self.number_of_win)
        result += "Number of losses: {0}\n".format(self.number_of_losses)
        result += "Number of ties: {0}\n".format(self.number_of_ties)
        return result

    def checkGameEnd(self) -> bool:
        """Check if the game is over.

        The game is over when there is either a winner or the board is full
        
        Returns:
            A bool that shows if the game is over
        """
        # Checks if there is a winner
        if self.isWinner():
            return True
        
        # Checks if the board is full
        if self.boardIsFull():
            return True
        
        # Returns false if the game isn't over
        return False
    
    def setPlayerName(self, name: str) -> None:
        """Set the player_name to name

        Args:
            name: the name to set to the player
        
        """
        
        self.player_name = name
    
    def setOtherPlayerName(self, name: str) -> None:
        """Set the other_player_name to name

        Args:
            name: the name to set to the other player
        
        """
        
        self.other_player_name = name
    
    def getOtherPlayerName(self) -> str:
        """Get the other player's name

        Return:
            the other player's name
        
        """
        return self.other_player_name
    
    def getPlayerName(self) -> str:
        """Get the player's name

        Return:
            the player's name
        """
        return self.player_name

    def getResult(self) -> str:
        """Get the result of the game

        Return:
            The result of the game, either "You have won", "You have lost", or "Tie"

        """
        return self.result
    