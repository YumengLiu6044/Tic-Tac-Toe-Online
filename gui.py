import pygame

class EntryBox(pygame.Rect):
    """
    An entry box object that's based on the pygame.Rect class

    Attributes:
        screen: the screen to draw on
        text: the text to display
        FONT: the font object that renders the text_surface
        text_surface: the text surface that will be drawn on the screen
        pre_text_surface: the text surface that will appear before the entry box
        active: whether the entry box is active
        surface: the background for the text surface

    """
    def __init__(self, 
                 screen: pygame.Surface, 
                 left: float, 
                 top: float, 
                 width: float, 
                 height: float, 
                 pretext='') -> None:
        """ Initializes the entry box

        Args:
            screen: the screen to draw on
            left: the x coordinate
            top: the y coordinate
            width: the minimum width of the entry box when it's empty
            height: the height of the entry box
            pretext: the text that appears before the entry box
        
        """
        self.screen = screen
        self.text = ''
        self.FONT = pygame.font.Font(None, height)
        self.text_surface = self.FONT.render(self.text, 1, (0, 0, 0))
        self.pre_text_surface = self.FONT.render(pretext, 1, (200, 200, 200))
        self.active = False
        self.surface = pygame.Surface((width, height))
        self.surface.fill((255, 255, 255))
        super().__init__(left, top, width + self.pre_text_surface.get_width(), height)

    def get(self) -> str:
        """Get the text that's currently in the entry box

        Returns:
            the text that's in the entry box
        """
        return self.text
    
    def handleEvent(self, event: pygame.event.Event) -> None:
        """Handles user input

        If the user clicks on the entry box, it will be activated and will listen to keyboard input

        Args:
            event: the event to handle

        """

        # Check if mouse clicked on entry box
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.collidepoint(event.pos):
                self.surface.fill((108, 234, 203))
                self.active = True
            else:
                self.surface.fill((255, 255, 255))
                self.active = False
            
        # Check keyboard input and update self.text
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                
                elif event.key != pygame.K_RETURN:
                    self.text += event.unicode
                
                self.text_surface = self.FONT.render(self.text, 1, (0, 0, 0))
                self.update()

    def clear(self) -> None:
        """Clears the text in the entry box
        """
        self.text = ''
        self.text_surface = self.FONT.render(self.text, 1, (0, 0, 0))
        self.update()

    def update(self):
        """Updates the width of the entry box based on how long the text is
        """
        self.surface.fill((0, 0, 0))
        self.draw_me()
        self.surface = pygame.Surface((max(self.width - self.pre_text_surface.get_width(), self.text_surface.get_width()), self.height))
        self.surface.fill((108, 234, 203))

    def draw_me(self) -> None:
        """Draws the entry box and the texts on the screen"""
        self.screen.blit(self.surface, (self.left + self.pre_text_surface.get_width(), self.top))
        self.screen.blit(self.text_surface, (self.left + self.pre_text_surface.get_width(), self.top))
        self.screen.blit(self.pre_text_surface, (self.left, self.top))
    

class Button(pygame.Rect):
    """A button object that's based on pygame.Rect

    Attributes:
        screen: the screen to draw on
        FONT: the font object that renders the text_surface
        text_surface: the text surface that will be drawn on the screen
        pressed: whether the button is being pressed

    """
    def __init__(self, 
                 screen: pygame.Surface, 
                 text: str, 
                 left: float, 
                 top: float, 
                 height: float) -> None:
        """Initializes the button onject
        Args:
            screen: the screen to draw on
            text: the word on the button
            left: the x coordinate
            top: the y coordinate
            height: the height of the button
        """
        self.FONT = pygame.font.Font(None, height)
        self.text_surface = self.FONT.render(text, 1, (0, 0, 0))
        super().__init__(left, top, self.text_surface.get_width(), height)
        self.surface = pygame.Surface((self.width, height))
        self.surface.fill((160, 160, 160))
        self.screen = screen
        self.pressed = False
    
    def isPressed(self) -> bool:
        """Returns if the button is being pressed"""
        return self.pressed

    def release(self) -> None:
        """Release the button"""
        self.pressed = False

    def handleEvent(self, event: pygame.event.Event) -> None:
        """Handles player input

        If the player clicks on the button, set self.pressed to true.
        If not, set self.pressed to false

        Args:
            event: the event to handle

        """

        # Checks if player clicked on the button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.collidepoint(event.pos):
                self.pressed = True
                self.surface.fill((130, 130, 130))
            else:
                self.pressed = False
                self.surface.fill((160, 160, 160))

        # Checks if player released the mouse
        if event.type == pygame.MOUSEBUTTONUP:
                self.pressed = False
                self.surface.fill((160, 160, 160))

    def draw_me(self) -> None:
        """Draw the button on the screen"""
        self.screen.blit(self.surface, (self.left, self.top))
        self.screen.blit(self.text_surface, (self.left, self.top))


class Text:
    """A text object
    
    Attributes:
        FONT: the font object that renders the text
        surface: the text surface to draw on screen
        screen: the screen to draw on
        left: the x coordinate
        top: the y coordinate

    """
    def __init__(self, 
                 screen: pygame.Surface, 
                 left: float, 
                 top: float, 
                 text='', 
                 height=30, 
                 color=(255, 255, 255)) -> None:
        """Initialize the text obejct
        
        Args:
            screen: the screen to draw on
            left: the x coordinate
            top: the y coordinate
            text: the text to draw
            height: the height of the text
            color: the color of the text

        """
        self.FONT = pygame.font.Font(None, height)
        self.texts = text.split('\n')
        self.surfaces = [self.FONT.render(self.texts[i], 1, color, (0, 0, 0)) for i in range(len(self.texts))]
        self.screen = screen
        self.left = left
        self.top = top
    
    def draw_me(self) -> None:
        """Draw the text on screen"""
        for i in range(len(self.surfaces)):
            self.screen.blit(self.surfaces[i], (self.left, self.top + self.surfaces[i].get_height() * i))

    def update(self, text: str, color=(255, 255, 255)) -> None:
        """Update the text object with the new text and draw it on screen
        
        Args:
            text: the new text
            color: the new color

        """
        self.texts = text.split('\n')
        self.surfaces = [self.FONT.render(self.texts[i], 1, color, (0, 0, 0)) for i in range(len(self.texts))]
        self.draw_me()


class Block(pygame.Rect):
    """A block on the tic-tac-toe board
    Atttributes:
        screen: the screen to draw on
        surface: the surface to draw
        type: whether the block is empty

    """
    def __init__(self, 
                 screen: pygame.Surface, 
                 left: float, 
                 top: float, 
                 width: float) -> None:
        """Initializes the block
        
        Args:
            screen: the screen to draw on
            left: the x coordinate
            top: the y coordinate
            width: the width and height of the block

        """
        self.screen = screen
        self.surface = pygame.Surface((width, width))
        super().__init__(left, top, width, width)
        self.type = 'empty'

    def handleEvent(self, event: pygame.event.Event) -> bool:
        """Handles user input
        
        Checks if the user pressed on the block

        Args:
            event: the event to handle

        Returns:
            A boolean value representing if a valid move
            is made on the block

        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.collidepoint(event.pos):
                if self.type == 'taken':
                    return False

                self.type = 'taken'
                return True
            
        return False
            
    def drawCircle(self) -> None:
        """Draws a circle on the block"""
        pygame.draw.circle(self.surface, (255, 0, 0), (self.width / 2, self.width / 2), self.width / 2, 2)

    def drawX(self) -> None:
        """Draws an x on the block"""
        pygame.draw.line(self.surface, (255, 0, 0), (0, 0), (self.width, self.width), 2)
        pygame.draw.line(self.surface, (255, 0, 0), (self.width, 0), (0, self.width), 2) 
    
    def draw_me(self):
        """Draw the block on the screen"""
        self.screen.blit(self.surface, (self.left, self.top))


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((200, 200))
    text = Text(screen, 10, 10, 'I am\nBat\nMan')
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        
        text.draw_me()
        pygame.display.update()
        