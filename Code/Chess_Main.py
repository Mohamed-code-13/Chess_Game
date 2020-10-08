# BY: Mohamed Ashraf Gaber.
# CHESS GAME. #

# # # # :NOTE: # # # #
# If There is a problem when you try to open the game change line 9 to be like this "import Chess_Engine".

# Importing libraries.
import pygame
from Chess_Game.Code import Chess_Engine

pygame.init()  # Initializing Pygame.
pygame.display.set_caption('Chess Game')  # Setting a title to the game.

# Declaring some global variables.
WIDTH = 512  # The width and the height of the game (512 x 512).
DIMENSION = 8  # The chess board is (8 x 8).
SQUARE_SIZE = WIDTH // DIMENSION  # The size of each square in the board.
IMAGES = {}  # This dictionary will contain the images of the pieces.

# Declaring some colors.
WHITE = (255, 255, 255)
BROWN = (205, 126, 0)


# This is the main function that will contain all functions and will handle the whole process.
def main():
    load_images()  # Loading the images.
    screen = pygame.display.set_mode((WIDTH, WIDTH))  # This is the screen that will have the chess game.
    game = Chess_Engine.HandlingTheGame()  # This is the actual game from the engine.
    valid_moves = game.valid_moves()  # Getting only the valid moves.
    move_made = False  # It'll be True when the move was made and generating only valid move for the next player.
    run = True  # It will be true until the game ends.
    selected_square = ()  # Square was selected by the user.
    user_clicks = []  # It will contain the user clicks.

    while run:
        # Looping over every event user do.
        for event in pygame.event.get():
            # If the user wants to close the game, stop the while loop and close the game.
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # Getting mouse position.

                col = mouse_pos[0] // SQUARE_SIZE  # Getting the column that user clicked.
                row = mouse_pos[1] // SQUARE_SIZE  # Getting the row that user clicked.

                # If user chose the same square twice, ignore this square.
                if selected_square == (row, col):
                    selected_square = ()
                    user_clicks = []

                # If not, get this square.
                else:
                    selected_square = (row, col)
                    user_clicks.append(selected_square)

                # If user chose empty square, ignore this square.
                if len(user_clicks) == 1 and game.board[row][col] == '--':
                    selected_square = ()
                    user_clicks = []

                # If user chose two different squares and the move is valid, make the move.
                elif len(user_clicks) == 2:
                    # Creating a move object.
                    move = Chess_Engine.Move(user_clicks[0], user_clicks[1], game.board)

                    # Checking if the move that player made is valid or not.
                    if move in valid_moves:
                        game.make_move(move)  # Make the move.

                        move_made = True

                        # Setting these variables empty preparing the next move.
                        selected_square = ()
                        user_clicks = []

                    # If player chose a piece and changed his mind to chose another piece,
                    # Only get the last piece clicked.
                    else:
                        user_clicks = [selected_square]

            # Checking if player pressed Space to undo the last move.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.undo_move()  # Undo the last move.
                    move_made = True

            # If the move was made, generate the valid moves for the next player.
            if move_made:
                valid_moves = game.valid_moves()
                move_made = False

        draw_window(screen, game.board)  # Drawing the window.
        pygame.display.update()  # Updating the screen.


# This function will load pieces' images.
def load_images():
    # The names of the pieces.
    pieces = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'bP']

    # Looping throw every piece.
    for piece in pieces:
        IMAGES[piece] = pygame.image.load(f'../images/{piece}.png')


# This function will draw the window of the game.
def draw_window(screen, board):
    draw_board(screen)  # Drawing the board.
    draw_pieces(screen, board)  # Drawing the pieces.


# This function will draw the chess board.
def draw_board(screen):
    colors = [WHITE, BROWN]

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]

            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE,  SQUARE_SIZE))


# This function will draw the chess pieces.
def draw_pieces(screen, board):
    for row in range(DIMENSION):  # Looping over every row.
        for col in range(DIMENSION):  # Looping over every square in the row.
            piece = board[row][col]  # Setting what is it inside this square.

            # If the square has a piece, draw it in the screen.
            if piece != '--':
                screen.blit(IMAGES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))


# Calling the main function.
main()

# If the program reaches this part, that means that the user closed the game.
pygame.quit()
