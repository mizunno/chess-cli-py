from typing import List, Tuple
from enum import Enum, StrEnum
from dataclasses import dataclass

class Color(Enum):
    """Enum class to define piece colors."""
    WHITE = 0
    BLACK = 1

class Category(StrEnum):
    """Enum class to represent the category of each piece (e.g. King, Queen, etc)"""
    PAWN = "P"
    ROOK = "R"
    KNIGHT = "N"
    BISHOP = "B"
    QUEEN = "Q"
    KING = "K"

class Action(StrEnum):
    """Enum class to represent the action of the move"""
    MOVE = "m"
    CAPTURE = "x"
    CASTLING_KING = "O-O"
    CASTLING_QUEEN = "O-O-O"
    CHECK = "+"
    CHECKMATE = "#"
    PROMOTE = "="

@dataclass
class Movement:
    category: Category
    action: Action
    next_position: Tuple[int, int]
    current_row: int = None
    current_col: int = None
    next_category: Category = None

class InvalidMovement(Exception):
    pass

class Piece:

    def __init__(self, position, color, category):
        self.position = position
        self.color = color
        self.category = category

    def move(self, move: Movement):
        raise NotImplementedError()

    def get_path(self, move: Movement):
        raise NotImplementedError()

    def _is_outside_board(self, move: Movement):
        return (
            move.next_position[0] < 0 or
            move.next_position[0] > 7 or
            move.next_position[1] < 0 or
            move.next_position[1] > 7
        )

    def __str__(self):
        return str(self.category) if self.color == Color.BLACK else f"{self.category}'"

    def __repr__(self):
        return str(self.category) if self.color == Color.BLACK else f"{self.category}'"

class Pawn(Piece):

    def __init__(self, position: Tuple[int, int], color: Color):
        super().__init__(position, color, Category.PAWN)

    def move(self, move: Movement):
        if self._is_outside_board(move):
            raise InvalidMovement("Can't move to a position outside the board!")

        if move.action == Action.MOVE:
            if not self._is_valid_move(move):
                raise InvalidMovement()

            self.position = move.next_position

        elif move.action == Action.CAPTURE:
            pass

    def get_path(self, move: Movement):
        if not self._is_valid_move(move) or self._is_outside_board(move):
            raise InvalidMovement()

        path = []
        curr_position = self.position

        while curr_position != move.next_position:
            curr_position = list(curr_position)

            if self.color == Color.WHITE:
                curr_position[0] -= 1
            else:
                curr_position[0] += 1

            curr_position = tuple(curr_position)
            path.append(curr_position)

        return path

        
    def _is_first_move(self):
        return (
            (self.position[0] == 6 and self.color == Color.WHITE) or
            (self.position[0] == 1 and self.color == Color.BLACK)
        )

    def _is_valid_move(self, move: Movement):
        if self._is_first_move():
            return (
                (self.color == Color.BLACK and move.next_position[0] in [3, 2]) or
                (self.color == Color.WHITE and move.next_position[0] in [4, 5])
                )
        else:
            return (
                (self.color == Color.BLACK and self.position[0] + 1 == move.next_position[0]) or
                (self.color == Color.WHITE and self.position[0] - 1 == move.next_position[0])
                )


class Rook(Piece):

    def __init__(self, position: Tuple[int, int], color: Color):
        super().__init__(position, color, Category.ROOK)

    def move(self, move: Movement):
        if self._is_outside_board(move):
            raise InvalidMovement("Can't move to a position outside the board!")

        if move.action == Action.MOVE:
            if not self._is_valid_move(move):
                raise InvalidMovement()

            self.position = move.next_position

    def get_path(self, move: Movement):
        if not self._is_valid_move(move) or self._is_outside_board(move):
            raise InvalidMovement()

        path = []
        curr_position = self.position

        while curr_position != move.next_position:
            curr_position = list(curr_position)

            if self._is_vertical_move(move):
                if curr_position[0] < move.next_position[0]:
                    curr_position[0] += 1
                else:
                    curr_position[0] -= 1
            else:
                if curr_position[1] < move.next_position[1]:
                    curr_position[1] += 1
                else:
                    curr_position[1] -= 1

            curr_position = tuple(curr_position)
            path.append(curr_position)

        return path

    def _is_valid_move(self, move: Movement):
        return self._is_horizontal_move(move) or self._is_vertical_move(move)

    def _is_vertical_move(self, move: Movement):
        return self.position[1] == move.next_position[1] and self.position[0] != move.next_position[0]

    def _is_horizontal_move(self, move: Movement):
        return self.position[0] == move.next_position[0] and self.position[1] != move.next_position[1]

class Knight(Piece):

    def __init__(self, position, color):
        super().__init__(position, color, Category.KNIGHT)

    def move(self, move: Movement):
        if self._is_outside_board(move):
            raise InvalidMovement("Can't move to a position outside the board!")

        if move.action == Action.MOVE:
            if not self._is_valid_move(move):
                raise InvalidMovement()

            self.position = move.next_position

    def get_path(self, move: Movement):
        return []

    def _is_valid_move(self, move: Movement):
        possible_moves = [
            (-2, 1), (-1, 2),
            (1, 2), (2, 1),
            (2, -1), (1, -2),
            (-1, -2), (-2, -1)
        ]

        for x, y in possible_moves:
            possible_next_pos = self.position[0] + x, self.position[1] + y
            if possible_next_pos == move.next_position:
                return True

        return False


class Bishop(Piece):

    def __init__(self, position, color):
        super().__init__(position, color, Category.BISHOP)

    def move(self, move: Movement):
        if self._is_outside_board(move):
            raise InvalidMovement("Can't move to a position outside the board!")

        if move.action == Action.MOVE:
            if not self._is_valid_move(move):
                raise InvalidMovement()

            self.position = move.next_position

    def get_path(self, move: Movement):
        if not self._is_valid_move(move) or self._is_outside_board(move):
            raise InvalidMovement()

        path = []
        curr_position = self.position

        while curr_position != move.next_position:
            curr_position = list(curr_position)

            if curr_position[0] < move.next_position[0] and curr_position[1] > move.next_position[1]:
                curr_position[0] += 1
                curr_position[1] -= 1
            elif curr_position[0] > move.next_position[0] and curr_position[1] > move.next_position[1]:
                curr_position[0] -= 1
                curr_position[1] -= 1
            elif curr_position[0] > move.next_position[0] and curr_position[1] < move.next_position[1]:
                curr_position[0] -= 1
                curr_position[1] += 1
            elif curr_position[0] < move.next_position[0] and curr_position[1] < move.next_position[1]:
                curr_position[0] += 1
                curr_position[1] += 1

            curr_position = tuple(curr_position)
            path.append(curr_position)

        return path

    def _is_valid_move(self, move: Movement):
        p1 = abs(self.position[0] - move.next_position[0])
        p2 = abs(self.position[1] - move.next_position[1])

        return p1 == p2

    def _is_vertical_move(self, move: Movement):
        return self.position[1] == move.next_position[1] and self.position[0] != move.next_position[0]

    def _is_horizontal_move(self, move: Movement):
        return self.position[0] == move.next_position[0] and self.position[1] != move.next_position[1]


class Queen(Piece):

    def __init__(self, position, color):
        super().__init__(position, color, Category.QUEEN)

    def move(self, move: Movement):
        if self._is_outside_board(move):
            raise InvalidMovement("Can't move to a position outside the board!")

        if move.action == Action.MOVE:
            if not self._is_valid_move(move):
                raise InvalidMovement()

            self.position = move.next_position

    def get_path(self, move: Movement):
        if not self._is_valid_move(move) or self._is_outside_board(move):
            raise InvalidMovement()

        path = []
        curr_position = self.position

        while curr_position != move.next_position:
            curr_position = list(curr_position)

            if curr_position[0] < move.next_position[0] and curr_position[1] > move.next_position[1]:
                curr_position[0] += 1
                curr_position[1] -= 1
            elif curr_position[0] > move.next_position[0] and curr_position[1] > move.next_position[1]:
                curr_position[0] -= 1
                curr_position[1] -= 1
            elif curr_position[0] > move.next_position[0] and curr_position[1] < move.next_position[1]:
                curr_position[0] -= 1
                curr_position[1] += 1
            elif curr_position[0] < move.next_position[0] and curr_position[1] < move.next_position[1]:
                curr_position[0] += 1
                curr_position[1] += 1
            elif self._is_horizontal_move(move) and curr_position[1] < move.next_position[1]:
                curr_position[1] += 1
            elif self._is_horizontal_move(move) and curr_position[1] > move.next_position[1]:
                curr_position[1] -= 1
            elif self._is_vertical_move(move) and curr_position[0] < move.next_position[0]:
                curr_position[0] += 1
            elif self._is_vertical_move(move) and curr_position[0] > move.next_position[0]:
                curr_position[0] -= 1

            curr_position = tuple(curr_position)
            path.append(curr_position)

        return path

    def _is_valid_move(self, move: Movement):
        line_move = self._is_horizontal_move(move) or self._is_vertical_move(move)
        diag_move = self._is_diagonal_move(move)

        return line_move or diag_move

    def _is_vertical_move(self, move: Movement):
        return self.position[1] == move.next_position[1] and self.position[0] != move.next_position[0]

    def _is_horizontal_move(self, move: Movement):
        return self.position[0] == move.next_position[0] and self.position[1] != move.next_position[1]

    def _is_diagonal_move(self, move: Movement):
        p1 = abs(self.position[0] - move.next_position[0])
        p2 = abs(self.position[1] - move.next_position[1])

        return p1 == p2


class King(Piece):

    def __init__(self, position, color):
        super().__init__(position, color, Category.KING)

    def move(self, move: Movement):
        if self._is_outside_board(move):
            raise InvalidMovement("Can't move to a position outside the board!")

        if move.action == Action.MOVE:
            if not self._is_valid_move(move):
                raise InvalidMovement()

            self.position = move.next_position

    def get_path(self, move: Movement):
        if not self._is_valid_move(move) or self._is_outside_board(move):
            raise InvalidMovement()

        path = []
        curr_position = self.position

        while curr_position != move.next_position:
            curr_position = list(curr_position)

            if curr_position[0] < move.next_position[0] and curr_position[1] > move.next_position[1]:
                curr_position[0] += 1
                curr_position[1] -= 1
            elif curr_position[0] > move.next_position[0] and curr_position[1] > move.next_position[1]:
                curr_position[0] -= 1
                curr_position[1] -= 1
            elif curr_position[0] > move.next_position[0] and curr_position[1] < move.next_position[1]:
                curr_position[0] -= 1
                curr_position[1] += 1
            elif curr_position[0] < move.next_position[0] and curr_position[1] < move.next_position[1]:
                curr_position[0] += 1
                curr_position[1] += 1
            elif self._is_horizontal_move(move) and curr_position[1] < move.next_position[1]:
                curr_position[1] += 1
            elif self._is_horizontal_move(move) and curr_position[1] > move.next_position[1]:
                curr_position[1] -= 1
            elif self._is_vertical_move(move) and curr_position[0] < move.next_position[0]:
                curr_position[0] += 1
            elif self._is_vertical_move(move) and curr_position[0] > move.next_position[0]:
                curr_position[0] -= 1

            curr_position = tuple(curr_position)
            path.append(curr_position)

        return path

    def _is_valid_move(self, move: Movement):
        line_move = self._is_horizontal_move(move) or self._is_vertical_move(move)
        diag_move = self._is_diagonal_move(move)
        is_one_step = self._is_one_step(move)

        return (line_move or diag_move) and is_one_step

    def _is_vertical_move(self, move: Movement):
        return self.position[1] == move.next_position[1] and self.position[0] != move.next_position[0]

    def _is_horizontal_move(self, move: Movement):
        return self.position[0] == move.next_position[0] and self.position[1] != move.next_position[1]

    def _is_diagonal_move(self, move: Movement):
        p1, p2 = self._subtract_positions(move)
        return p1 == p2

    def _is_one_step(self, move: Movement):
        p1, p2 = self._subtract_positions(move)
        return (p1 + p2) <= 2

    def _subtract_positions(self, move: Movement):
        p1 = abs(self.position[0] - move.next_position[0])
        p2 = abs(self.position[1] - move.next_position[1])

        return p1, p2


class AlgebraicExpressionParser:

    def parse(self, expr):
        # (piece cat, action, dst)

        if Action.CAPTURE in expr[1]:
            return self._parse_capture(expr)
        elif Action.CASTLING_KING == expr:
            return self._parse_castling_king(expr)
        elif Action.CASTLING_QUEEN == expr:
            return self._parse_castling_queen(expr)
        elif Action.CHECK in expr:
            return self._parse_check(expr)
        elif Action.CHECKMATE in expr[-1]:
            return self._parse_checkmate(expr)
        elif Action.PROMOTE == expr[-2]:
            return self._parse_promote(expr)
        else:
            return self._parse_move(expr)

    def _parse_capture(self, expr):
        col = self._letter_to_num(expr[2])
        row = self._parse_row(expr[3])

        if expr[0].lower() == expr[0]:
            # Pawn captures
            return Movement(Category.PAWN, Action.CAPTURE, (row, col))

        piece = Category(expr[0])
        return Movement(piece, Action.CAPTURE, (row, col))

    def _parse_castling_king(self, expr):
        return Movement(Category.KING, Action.CASTLING_KING, None)

    def _parse_castling_queen(self, expr):
        return Movement(Category.KING, Action.CASTLING_QUEEN, None)

    def _parse_check(self, expr):
        if len(expr) == 3:
            # Pawn checks
            col = self._letter_to_num(expr[0])
            row = self._parse_row(expr[1])
            return Movement(Category.PAWN, Action.CHECK, (row, col))

        piece = Category(expr[0])
        col = self._letter_to_num(expr[1])
        row = self._parse_row(expr[2])

        return Movement(piece, Action.CHECK, (row, col))

    def _parse_checkmate(self, expr):
        if len(expr) == 3:
            # Pawn checks
            col = self._letter_to_num(expr[0])
            row = self._parse_row(expr[1])
            return Movement(Category.PAWN, Action.CHECKMATE, (row, col))

        piece = Category(expr[0])
        col = self._letter_to_num(expr[1])
        row = self._parse_row(expr[2])

        return Movement(piece, Action.CHECKMATE, (row, col))

    def _parse_promote(self, expr):
        col = self._letter_to_num(expr[0])
        row = self._parse_row(expr[1])
        next_category = Category(expr[-1])

        return Movement(Category.PAWN, Action.PROMOTE, (row, col), None, None, next_category)

    def _parse_move(self, expr):
        # First char is the piece letter.
        # In case of pawn, piece letter is omitted.
        if len(expr) == 2:
            # Pawn movement
            col = self._letter_to_num(expr[0])
            row = self._parse_row(expr[1])

            return Movement(Category.PAWN, Action.MOVE, (row, col))
        elif len(expr) == 4:
            # Special case when two same category pieces can move
            # to the same square.

            piece = Category(expr[0])
            col = self._letter_to_num(expr[2])
            row = self._parse_row(expr[3])
            current_row, current_col = None, None

            if expr[1].isdigit():
                current_row = self._parse_row(expr[1])
            else:
                current_col = self._letter_to_num(expr[1])

            return Movement(piece, Action.MOVE, (row, col), current_row, current_col)
        else:
            piece = Category(expr[0])
            col = self._letter_to_num(expr[1])
            row = self._parse_row(expr[2])

            return Movement(piece, Action.MOVE, (row, col))

    def _letter_to_num(self, letter):
        """Transform the file (letter) to a number representation."""
        return ord(letter) - ord("a")

    def _parse_row(self, original_row):
        return 8 - int(original_row)


class Board:

    def __init__(self, pieces: List[Piece]):
        self.pieces = pieces

    # TODO: next_state
    def perform_movement(self, move: Movement, color: Color):
        possible_pieces = self._get_possible_pieces(move, color)

        if move.action == Action.MOVE and self._is_square_empty(move.next_position):
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
        possible_pieces = [p for p in self.pieces if p.category == move.category and p.color == color]

        if move.category == Category.PAWN:
            valid_piece = [p for p in possible_pieces if p.position[1] == move.next_position[1]]
            return valid_piece

        if move.current_col != None or move.current_row != None:
            # code to infer in this case
            return None

        return possible_pieces

    def _is_square_empty(self, position):
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
        board = [["" for i in range (8)] for i in range(8)]
        for piece in self.pieces:
            board[piece.position[0]][piece.position[1]] = str(piece)

        for i, row in enumerate(board):
            print("  ", end="")
            print("-"*50)
            print(f" {8-i} ", end="")
            for j, cell in enumerate(row):
                if cell == "":
                    print(f"|     ", end="")
                elif "'" in cell:
                    print(f"|  {cell} ", end="")
                else:
                    print(f"|  {cell}  ", end="")


            print("|")
        print("  ", end="")
        print("-"*50)

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
        # begins infinite loop
        while 1:
            self.board.show()
            player_input = input(f"{self.current_turn} > ")
            player_movement = self.parser.parse(player_input)
            try:
                self.board.perform_movement(player_movement, self.current_turn)
                self._next_turn()
            except InvalidMovement:
                print("Invalid movement. Try again!")

    def _next_turn(self):
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE


def get_initial_board():
    # WHITE pieces
    pieces = [Pawn(position=(6, i), color=Color.WHITE) for i in range(8)]
    pieces.extend([Knight(position=(7, 1), color=Color.WHITE), Knight(position=(7, 6), color=Color.WHITE)])
    pieces.extend([Bishop(position=(7, 2), color=Color.WHITE), Bishop(position=(7, 5), color=Color.WHITE)])
    pieces.extend([Rook(position=(7, 0), color=Color.WHITE), Rook(position=(7, 7), color=Color.WHITE)])
    pieces.extend([Queen(position=(7, 3), color=Color.WHITE)])
    pieces.extend([King(position=(7, 4), color=Color.WHITE)])

    # BLACK pieces
    pieces.extend([Pawn(position=(1, i), color=Color.BLACK) for i in range(8)])
    pieces.extend([Knight(position=(0, 1), color=Color.BLACK), Knight(position=(0, 6), color=Color.BLACK)])
    pieces.extend([Bishop(position=(0, 2), color=Color.BLACK), Bishop(position=(0, 5), color=Color.BLACK)])
    pieces.extend([Rook(position=(0, 0), color=Color.BLACK), Rook(position=(0, 7), color=Color.BLACK)])
    pieces.extend([Queen(position=(0, 3), color=Color.BLACK)])
    pieces.extend([King(position=(0, 4), color=Color.BLACK)])

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
