# BY: Mohamed Ashraf Gaber

# Importing libraries.
import tkinter as tk
from tkinter import messagebox


# This class will handle every thing about the game.
class HandlingTheGame:
    def __init__(self):
        # The chess board.
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.white_to_move = True  # White starts first at the game
        self.log = []  # The log that will have all moves player do.
        self.white_king_pos = (7, 4)  # The white king position.
        self.black_king_pos = (0, 4)  # The black king position.

        # This dictionary contains the moving functions for every piece in Chess.
        self.moving_functions = {'P': self.pawn_moves, 'R': self.rook_moves, 'N': self.knight_moves,
                                 'B': self.bishop_moves, 'Q': self.queen_moves, 'K': self.king_moves}

        # The check mate and stale mate variables.
        self.check_mate = False
        self.stale_mate = False

    # This method will handle making moves.
    def make_move(self, move):
        self.board[move.start[0]][move.start[1]] = '--'  # Making the old square empty.
        self.board[move.end[0]][move.end[1]] = move.piece_moved  # Setting the moves piece to its new square.
        self.log.append(move)  # Appending the move to the log.
        self.white_to_move = not self.white_to_move  # Changing the turns.

        # Checking if the king moved. And if the king moved, update king position.
        if move.piece_moved == 'wK':
            self.white_king_pos = (move.end[0], move.end[1])

        elif move.piece_moved == 'bK':
            self.black_king_pos = (move.end[0], move.end[1])

    # This method will undo the move.
    def undo_move(self):
        if len(self.log) != 0:
            last_move = self.log.pop()  # Getting the last move.

            # Returning the moved piece to its old square.
            self.board[last_move.start[0]][last_move.start[1]] = last_move.piece_moved
            # Returning the captured piece to its square.
            self.board[last_move.end[0]][last_move.end[1]] = last_move.piece_captured

            self.white_to_move = not self.white_to_move  # Changing the turns.

            # Checking if the king moved. And if the king moved, update king position.
            if last_move.piece_moved == 'wK':
                self.white_king_pos = (last_move.start[0], last_move.start[1])

            elif last_move.piece_moved == 'bK':
                self.black_king_pos = (last_move.start[0], last_move.start[1])

            # Setting the check_mate and stale mate variables to False.
            self.check_mate = False
            self.stale_mate = False

    # This method will return all valid moves that player can do.
    def valid_moves(self):
        # Getting all possible moves.
        moves = self.possible_moves()

        # Looping throw every move to check if it's valid or not.
        # If it's not valid, delete this move from the moves list.
        for move in range(len(moves)-1, -1, -1):
            self.make_move(moves[move])
            self.white_to_move = not self.white_to_move

            if self.in_check():
                moves.remove(moves[move])

            self.white_to_move = not self.white_to_move
            self.undo_move()

        # Checking if there is no valid moves.
        if len(moves) == 0:
            # Checking if it's check mate or stale mate
            if self.in_check():
                self.check_mate = True

            else:
                self.stale_mate = True

        # If there is valid moves, set the check_mate and stale mate variables to False.
        else:
            self.check_mate = False
            self.stale_mate = False

        if self.check_mate:
            winner = 'Black'
            if not self.white_to_move:
                winner = 'White'

            print("Check Mate")
            print(winner, 'is victorious')
            message_box('Check Mate', f'{winner} is victorious.')

        return moves  # Returning only the valid moves.

    # This method will return all possible moves.
    def possible_moves(self):
        moves = []

        # Looping over every row.
        for row in range(len(self.board)):
            # Looping over every square in the row.
            for col in range(len(self.board[row])):
                piece_color = self.board[row][col][0]  # Getting the piece color for every square.

                # If the piece color is white and white has to play or piece color is black and black has to play,
                # Generate all possible moves for this piece.
                if (piece_color == 'w' and self.white_to_move) or (piece_color == 'b' and not self.white_to_move):
                    piece = self.board[row][col][1]  # Getting the piece.

                    # Calling the piece's function to generate the possible moves for this piece.
                    self.moving_functions[piece](row, col, moves)

        return moves  # Returning all possible moves.

    # This method will return if the player in check or not.
    def in_check(self):
        # Checking if white has to play.
        # If white has to play, check if he is in check.
        # Else Check if black is in check.
        if self.white_to_move:
            return self.square_under_attack(self.white_king_pos[0], self.white_king_pos[1])

        return self.square_under_attack(self.black_king_pos[0], self.black_king_pos[1])

    # This method will return if a specific square is under attack or not.
    def square_under_attack(self, row, col):
        # Changing the turns and generating the opponents moves.
        self.white_to_move = not self.white_to_move
        opponents_moves = self.possible_moves()
        self.white_to_move = not self.white_to_move

        # Then looping throw them and if any move can attack this specific square return True Else return False.
        for move in opponents_moves:
            if move.end[0] == row and move.end[1] == col:
                return True

        return False

    # This method will generate all possible moves for every Pawn in the game.
    def pawn_moves(self, row, col, moves):
        if self.white_to_move:
            if self.board[row-1][col] == '--':
                moves.append(Move((row, col), (row-1, col), self.board))

                if row == 6 and self.board[row-2][col] == '--':
                    moves.append((Move((row, col), (row-2, col), self.board)))

            if col-1 >= 0 and col+1 <= 7:
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))

                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))

        else:
            if self.board[row+1][col] == '--':
                moves.append(Move((row, col), (row+1, col), self.board))

                if row == 1 and self.board[row+2][col] == '--':
                    moves.append((Move((row, col), (row + 2, col), self.board)))

            if col - 1 >= 0 and col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

                if self.board[row + 1][col - 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))

    # This method will generate all possible moves for every Rook in the game.
    def rook_moves(self, row, col, moves):
        color = 'b' if self.white_to_move else 'w'  # Getting the opponent color.
        direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # This is the direction of the Rook.

        for d in direction:
            for i in range(1, 8):
                r = row + d[0] * i
                c = col + d[1] * i

                if 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] == '--':
                        moves.append(Move((row, col), (r, c), self.board))

                    elif self.board[r][c][0] == color:
                        moves.append(Move((row, col), (r, c), self.board))
                        break

                    else:
                        break
                else:
                    break

    # This method will generate all possible moves for every Knight in the game.
    def knight_moves(self, row, col, moves):
        color = 'b' if self.white_to_move else 'w'  # Getting the opponent color.

        # This is the direction of the Knight.
        direction = [(1, 2), (2, 1), (-1, 2), (-1, -2), (2, -1), (-2, 1), (-2, -1), (1, -2)]

        for i in range(8):
            r = row + direction[i][0]
            c = col + direction[i][1]

            if 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == '--' or self.board[r][c][0] == color:
                    moves.append(Move((row, col), (r, c), self.board))

    # This method will generate all possible moves for every Bishop in the game.
    def bishop_moves(self, row, col, moves):
        color = 'b' if self.white_to_move else 'w'  # Getting the opponent color.
        direction = [(1, 1), (-1, -1), (1, -1), (-1, 1)]  # This is the direction of the Bishop.

        for d in direction:
            for i in range(1, 8):
                r = row + d[0] * i
                c = col + d[1] * i

                if 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] == '--':
                        moves.append(Move((row, col), (r, c), self.board))

                    elif self.board[r][c][0] == color:
                        moves.append(Move((row, col), (r, c), self.board))
                        break

                    else:
                        break
                else:
                    break

    # This method will generate all possible moves for every Queen in the game.
    def queen_moves(self, row, col, moves):
        # The queen can move like rook and bishop.
        self.rook_moves(row, col, moves)
        self.bishop_moves(row, col, moves)

    # This method will generate all possible moves for every King in the game.
    def king_moves(self, row, col, moves):
        color = 'b' if self.white_to_move else 'w'  # Getting the opponent color.

        # This is the direction of the King.
        direction = [(0, 1), (1, 1), (1, 0), (-1, 0), (-1, -1), (0, -1), (1, -1), (-1, 1)]

        for i in range(8):
            r = row + direction[i][0]
            c = col + direction[i][1]

            if 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c] == '--' or self.board[r][c][0] == color:
                    moves.append(Move((row, col), (r, c), self.board))


# This class will define every move.
# Every move will be an object from this class.
class Move:
    def __init__(self, start, end, board):
        self.start = start  # The starting position of the moving piece.
        self.end = end  # The ending position of the moving piece.
        self.piece_moved = board[self.start[0]][self.start[1]]  # The moved piece from the board.
        self.piece_captured = board[self.end[0]][self.end[1]]  # The captured piece from the board.

        # Creating an ID for every move to be able to compare two moves with each other.
        self.move_ID = self.start[0] * 1000 + self.start[1] * 100 + self.end[0] * 10 + self.end[1]

    # Changing the equal method to be able to compare two moves with each other.
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID


# This function will create a popup window when there is a winner.
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    root.destroy()
