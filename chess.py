import os
from algebraic_expression_parser import AlgebraicExpressionParser
from models import (
    Action,
    Position,
    Category,
    Movement,
    Color,
    Piece,
    InvalidMovement,
    Pawn,
    Rook,
    Knight,
    Bishop,
    Queen,
    King,
)
from typing import List


class Board:
    def __init__(self, pieces: List[Piece]):
        self.pieces = pieces

    # TODO: next_state
    def perform_movement(self, move: Movement, color: Color):
        possible_pieces = self._get_possible_pieces(move, color)

        if (
            move.action == Action.MOVE
            and self._is_square_empty(move.next_position)
        ):
            # At this point, there must be only one valid piece,
            # although there could be multiple pieces with the
            # same color and category
            # i.e. only one piece can move to the next position.
            moved = False
            for p in possible_pieces:
                try:
                    if move.category != Category.KNIGHT:
                        # Check if there is a piece in the way
                        if self._piece_in_the_way(p, move):
                            continue
                    p.move(move)
                    moved = True
                except InvalidMovement:
                    continue

            if not moved:
                raise InvalidMovement()

        else:
            raise InvalidMovement()

    def _get_possible_pieces(self, move: Movement, color: Color):
        possible_pieces = [
            p for p in self.pieces if p.category == move.category and p.color == color
        ]

        if move.category == Category.PAWN:
            valid_piece = [
                p for p in possible_pieces if p.position.y == move.next_position.y
            ]
            return valid_piece

        if move.current_col is not None or move.current_row is not None:
            # code to infer in this case
            return None

        return possible_pieces

    def _is_square_empty(self, position: Position):
        for piece in self.pieces:
            if piece.position == position:
                return False

        return True

    def _piece_in_the_way(self, piece: Piece, move: Movement):
        path = piece.get_path(move)

        for other_piece in self.pieces:
            if piece is not other_piece and other_piece.position in path:
                return True

        return False

    def show(self):
        board = [["" for i in range(8)] for i in range(8)]
        for piece in self.pieces:
            board[piece.position.x][piece.position.y] = str(piece)

        for i, row in enumerate(board):
            print("  ", end="")
            print("-" * 50)
            print(f" {8-i} ", end="")
            for j, cell in enumerate(row):
                if cell == "":
                    print("|     ", end="")
                elif "'" in cell:
                    print(f"|  {cell} ", end="")
                else:
                    print(f"|  {cell}  ", end="")

            print("|")
        print("  ", end="")
        print("-" * 50)

        print("      a     b     c     d     e     f     g     h")

    def __str__(self):
        pass


class Game:
    def __init__(self, board, parser):
        self.board = board
        self.parser = parser
        # stack with all board states
        self.board_states = []
        self.current_turn = Color.WHITE

    def play(self):
        show_error = False
        error_msg = ""
        # begins infinite loop
        while 1:
            self._clear_screen()
            self.board.show()
            if show_error:
                print(error_msg)
                show_error = False

            player_input = input(f"{self.current_turn} > ")
            player_movement = self.parser.parse(player_input)
            try:
                self.board.perform_movement(player_movement, self.current_turn)
                self._next_turn()
            except InvalidMovement:
                error_msg = "Invalid movement. Try again!"
                show_error = True

    def _clear_screen(self):
        # For POSIX (Linux, macOS)
        if os.name == 'posix':
            os.system('clear')
        # For Windows
        elif os.name == 'nt':
            os.system('cls')
        # For other systems, try ANSI escape codes
        else:
            print('\033[H\033[J')  # ANSI escape code for clearing screen

    def _next_turn(self):
        self.current_turn = (
            Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        )


def get_initial_board():
    # WHITE pieces
    pieces = [Pawn(position=Position(6, i), color=Color.WHITE)
              for i in range(8)]
    pieces.extend(
        [
            Knight(position=Position(7, 1), color=Color.WHITE),
            Knight(position=Position(7, 6), color=Color.WHITE),
        ]
    )
    pieces.extend(
        [
            Bishop(position=Position(7, 2), color=Color.WHITE),
            Bishop(position=Position(7, 5), color=Color.WHITE),
        ]
    )
    pieces.extend(
        [
            Rook(position=Position(7, 0), color=Color.WHITE),
            Rook(position=Position(7, 7), color=Color.WHITE),
        ]
    )
    pieces.extend([Queen(position=Position(7, 3), color=Color.WHITE)])
    pieces.extend([King(position=Position(7, 4), color=Color.WHITE)])

    # BLACK pieces
    pieces.extend([Pawn(position=Position(1, i), color=Color.BLACK)
                  for i in range(8)])
    pieces.extend(
        [
            Knight(position=Position(0, 1), color=Color.BLACK),
            Knight(position=Position(0, 6), color=Color.BLACK),
        ]
    )
    pieces.extend(
        [
            Bishop(position=Position(0, 2), color=Color.BLACK),
            Bishop(position=Position(0, 5), color=Color.BLACK),
        ]
    )
    pieces.extend(
        [
            Rook(position=Position(0, 0), color=Color.BLACK),
            Rook(position=Position(0, 7), color=Color.BLACK),
        ]
    )
    pieces.extend([Queen(position=Position(0, 3), color=Color.BLACK)])
    pieces.extend([King(position=Position(0, 4), color=Color.BLACK)])

    board = Board(pieces)

    return board


def main():
    print("Welcome to Chess CLI Py!")

    board = get_initial_board()
    parser = AlgebraicExpressionParser()
    game = Game(board, parser)
    game.play()


if __name__ == "__main__":
    main()
