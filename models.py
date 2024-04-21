from enum import Enum, StrEnum
from dataclasses import dataclass
from utils import (
    is_outside_board,
    is_vertical_move,
    is_horizontal_move,
    is_diagonal_move,
    is_one_step,
)


class Color(Enum):
    """Enum class to define piece colors."""

    WHITE = 0
    BLACK = 1


class Category(StrEnum):
    """Enum class to represent the category of each
    piece (e.g. King, Queen, etc)"""

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
class Position:
    x: int
    y: int


@dataclass
class Movement:
    category: Category
    action: Action
    next_position: Position
    current_row: int = None
    current_col: int = None
    next_category: Category = None


class InvalidMovement(Exception):
    pass


class Checkmate(Exception):
    pass


class InvalidAlgebraicExpression(Exception):
    pass


class Piece:
    def __init__(
        self,
        position: Position,
        color: Position,
        category: Position
    ):
        self.position = position
        self.color = color
        self.category = category

    def move(self, move: Movement):
        raise NotImplementedError()

    def get_path(self, move: Movement):
        raise NotImplementedError()

    def get_possible_moves(self):
        # Possible moves may contain invalid moves
        raise NotImplementedError()

    def __str__(self):
        return str(self.category) if self.color == Color.BLACK else f"{self.category}'"

    def __repr__(self):
        return str(self.category) if self.color == Color.BLACK else f"{self.category}'"


class Pawn(Piece):
    def __init__(self, position: Position, color: Color):
        super().__init__(position, color, Category.PAWN)

    def move(self, move: Movement):
        if is_outside_board(move):
            raise InvalidMovement(
                "Can't move to a position outside the board!")

        if move.action == Action.MOVE:
            if not self._is_valid_move(move):
                raise InvalidMovement()

            self.position = move.next_position

        elif move.action == Action.CAPTURE:
            if not self._is_valid_capture(move):
                print("asd")
                raise InvalidMovement()

            self.position = move.next_position

    def get_path(self, move: Movement):
        if not self._is_valid_move(move) or is_outside_board(move):
            raise InvalidMovement()

        path = []
        curr_position = self.position

        while curr_position != move.next_position:

            if self.color == Color.WHITE:
                curr_position = Position(curr_position.x - 1, curr_position.y)
            else:
                curr_position = Position(curr_position.x + 1, curr_position.y)

            path.append(curr_position)

        return path

    def get_possible_moves(self):
        possible_moves = []

        if self.color == Color.WHITE:
            possible_moves.append(Movement(Category.PAWN, Action.MOVE, Position(
                self.position.x - 1, self.position.y)))
            if self._is_first_move():
                possible_moves.append(Movement(Category.PAWN, Action.MOVE, Position(
                    self.position.x - 2, self.position.y)))

            capture_relative_positions = [(-1, -1), (-1, 1)]
            for dx, dy in capture_relative_positions:
                capture_move = Movement(Category.PAWN, Action.CAPTURE, Position(
                    self.position.x + dx, self.position.y + dy))
                if not is_outside_board(capture_move):
                    possible_moves.append(capture_move)

        else:
            possible_moves.append(Movement(Category.PAWN, Action.MOVE, Position(
                self.position.x + 1, self.position.y)))
            if self._is_first_move():
                possible_moves.append(Movement(Category.PAWN, Action.MOVE, Position(
                    self.position.x + 2, self.position.y)))

            capture_relative_positions = [(1, -1), (1, 1)]
            for dx, dy in capture_relative_positions:
                capture_move = Movement(Category.PAWN, Action.CAPTURE, Position(
                    self.position.x + dx, self.position.y + dy))
                if not is_outside_board(capture_move):
                    possible_moves.append(capture_move)

        return possible_moves

    def _is_first_move(self):
        return (self.position.x == 6 and self.color == Color.WHITE) or (
            self.position.x == 1 and self.color == Color.BLACK
        )

    def _is_valid_move(self, move: Movement):
        if self._is_first_move():
            return (
                self.color == Color.BLACK and move.next_position.x in [3, 2]
            ) or (
                self.color == Color.WHITE and move.next_position.x in [4, 5]
            )
        else:
            return (
                self.color == Color.BLACK
                and self.position.x + 1 == move.next_position.x
            ) or (
                self.color == Color.WHITE
                and self.position.x - 1 == move.next_position.x
            )

    def _is_valid_capture(self, move: Movement):
        if self.color == Color.BLACK:
            return (
                self.position.x + 1 == move.next_position.x
                and self.position.y - 1 == move.next_position.y
            ) or (
                self.position.x + 1 == move.next_position.x
                and self.position.y + 1 == move.next_position.y
            )
        else:
            return (
                self.position.x - 1 == move.next_position.x
                and self.position.y - 1 == move.next_position.y
            ) or (
                self.position.x - 1 == move.next_position.x
                and self.position.y + 1 == move.next_position.y
            )


class Rook(Piece):
    def __init__(self, position: Position, color: Color):
        super().__init__(position, color, Category.ROOK)

    def move(self, move: Movement):
        if is_outside_board(move):
            raise InvalidMovement(
                "Can't move to a position outside the board!")

        if not self._is_valid_move(move):
            raise InvalidMovement()

        self.position = move.next_position

    def get_path(self, move: Movement):
        if not self._is_valid_move(move) or is_outside_board(move):
            raise InvalidMovement()

        path = []
        curr_position = self.position

        while curr_position != move.next_position:
            # curr_position = list(curr_position)

            if is_vertical_move(self.position, move):
                if curr_position.x < move.next_position.x:
                    curr_position = Position(
                        curr_position.x + 1,
                        curr_position.y
                    )
                else:
                    curr_position = Position(
                        curr_position.x - 1,
                        curr_position.y
                    )
            else:
                if curr_position.y < move.next_position.y:
                    curr_position = Position(
                        curr_position.x,
                        curr_position.y + 1
                    )
                else:
                    curr_position = Position(
                        curr_position.x,
                        curr_position.y - 1
                    )

            # curr_position = tuple(curr_position)
            path.append(curr_position)

        return path

    def get_possible_moves(self):
        possible_moves = []

        # Rook can move horizontally
        for i in range(8):
            if i != self.position.y:
                possible_moves.append(
                    Movement(Category.ROOK, Action.MOVE, Position(self.position.x, i)))
                possible_moves.append(
                    Movement(Category.ROOK, Action.CAPTURE, Position(self.position.x, i)))

        # Rook can move vertically
        for i in range(8):
            if i != self.position.x:
                possible_moves.append(
                    Movement(Category.ROOK, Action.MOVE, Position(i, self.position.y)))
                possible_moves.append(
                    Movement(Category.ROOK, Action.CAPTURE, Position(i, self.position.y)))

        return possible_moves

    def _is_valid_move(self, move: Movement):
        return (
            is_horizontal_move(self.position, move)
            or is_vertical_move(self.position, move)
        )


class Knight(Piece):

    possible_relative_positions = [
        (-2, 1),
        (-1, 2),
        (1, 2),
        (2, 1),
        (2, -1),
        (1, -2),
        (-1, -2),
        (-2, -1),
    ]

    def __init__(self, position, color):
        super().__init__(position, color, Category.KNIGHT)

    def move(self, move: Movement):
        if is_outside_board(move):
            raise InvalidMovement(
                "Can't move to a position outside the board!")

        if not self._is_valid_move(move):
            raise InvalidMovement()

        self.position = move.next_position

    def get_path(self, move: Movement):
        return []

    def get_possible_moves(self):
        possible_moves = []

        # Iterate over each possible relative position
        for dx, dy in self.possible_relative_positions:
            # Calculate the next position based on the relative position
            next_pos = Position(self.position.x + dx, self.position.y + dy)
            # Check if the next position is within the board bounds
            if 0 <= next_pos.x < 8 and 0 <= next_pos.y < 8:
                # Add the movement to possible_moves
                possible_moves.append(
                    Movement(Category.KNIGHT, Action.MOVE, next_pos))
                possible_moves.append(
                    Movement(Category.KNIGHT, Action.CAPTURE, next_pos))

        return possible_moves

    def _is_valid_move(self, move: Movement):

        for dx, dy in self.possible_relative_positions:
            possible_next_pos = Position(
                self.position.x + dx,
                self.position.y + dy,
            )
            if possible_next_pos == move.next_position:
                return True

        return False


class Bishop(Piece):
    def __init__(self, position, color):
        super().__init__(position, color, Category.BISHOP)

    def move(self, move: Movement):
        if is_outside_board(move):
            raise InvalidMovement(
                "Can't move to a position outside the board!")

        if not self._is_valid_move(move):
            raise InvalidMovement()

        self.position = move.next_position

    def get_path(self, move: Movement):
        if not self._is_valid_move(move) or is_outside_board(move):
            raise InvalidMovement()

        path = []
        curr_position = self.position

        while curr_position != move.next_position:
            # curr_position = list(curr_position)

            if (
                curr_position.x < move.next_position.x
                and curr_position.y > move.next_position.y
            ):
                curr_position = Position(
                    curr_position.x + 1,
                    curr_position.y - 1,
                )
            elif (
                curr_position.x > move.next_position.x
                and curr_position.y > move.next_position.y
            ):
                curr_position = Position(
                    curr_position.x - 1,
                    curr_position.y - 1,
                )
            elif (
                curr_position.x > move.next_position.x
                and curr_position.y < move.next_position.y
            ):
                curr_position = Position(
                    curr_position.x - 1,
                    curr_position.y + 1,
                )
            elif (
                curr_position.x < move.next_position.x
                and curr_position.y < move.next_position.y
            ):
                curr_position = Position(
                    curr_position.x + 1,
                    curr_position.y + 1,
                )

            # curr_position = tuple(curr_position)
            path.append(curr_position)

        return path

    def get_possible_moves(self):
        possible_moves = []

        # Iterate over all possible directions a bishop can move
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            # Iterate over all possible distances a bishop can move in each direction
            for i in range(1, 8):
                # Calculate the next position based on the direction and distance
                next_pos = Position(self.position.x + dx * i,
                                    self.position.y + dy * i)
                # Check if the next position is within the board bounds
                if 0 <= next_pos.x < 8 and 0 <= next_pos.y < 8:
                    # Add the movement to possible_moves
                    possible_moves.append(
                        Movement(Category.BISHOP, Action.MOVE, next_pos))
                    possible_moves.append(
                        Movement(Category.BISHOP, Action.CAPTURE, next_pos))
                else:
                    # If the next position is outside the board bounds, stop iterating in this direction
                    break

        return possible_moves

    def _is_valid_move(self, move: Movement):
        p1 = abs(self.position.x - move.next_position.x)
        p2 = abs(self.position.y - move.next_position.y)

        return p1 == p2

    def _is_vertical_move(self, move: Movement):
        return (
            self.position.y == move.next_position.y
            and self.position.x != move.next_position.x
        )

    def _is_horizontal_move(self, move: Movement):
        return (
            self.position.x == move.next_position.x
            and self.position.y != move.next_position.y
        )


class Queen(Piece):
    def __init__(self, position, color):
        super().__init__(position, color, Category.QUEEN)

    def move(self, move: Movement):
        if is_outside_board(move):
            raise InvalidMovement(
                "Can't move to a position outside the board!")

        if not self._is_valid_move(move):
            raise InvalidMovement()

        self.position = move.next_position

    def get_path(self, move: Movement):
        # TODO: Refactor this
        if not self._is_valid_move(move) or is_outside_board(move):
            raise InvalidMovement()

        path = []
        curr_position = self.position

        while curr_position != move.next_position:
            # curr_position = list(curr_position)

            if (
                curr_position.x < move.next_position.x
                and curr_position.y > move.next_position.y
            ):
                curr_position = Position(
                    curr_position.x + 1,
                    curr_position.y - 1,
                )
            elif (
                curr_position.x > move.next_position.x
                and curr_position.y > move.next_position.y
            ):
                curr_position = Position(
                    curr_position.x - 1,
                    curr_position.y - 1,
                )
            elif (
                curr_position.x > move.next_position.x
                and curr_position.y < move.next_position.y
            ):
                curr_position = Position(
                    curr_position.x - 1,
                    curr_position.y + 1,
                )
            elif (
                curr_position.x < move.next_position.x
                and curr_position.y < move.next_position.y
            ):
                curr_position = Position(
                    curr_position.x + 1,
                    curr_position.y + 1,
                )
            elif (
                is_horizontal_move(self.position, move)
                and curr_position.y < move.next_position.y
            ):
                curr_position = Position(
                    curr_position.x,
                    curr_position.y + 1,
                )
            elif (
                is_horizontal_move(self.position, move)
                and curr_position.y > move.next_position.y
            ):
                curr_position = Position(
                    curr_position.x,
                    curr_position.y - 1,
                )
            elif (
                is_vertical_move(self.position, move)
                and curr_position.x < move.next_position.x
            ):
                curr_position = Position(
                    curr_position.x + 1,
                    curr_position.y,
                )
            elif (
                is_vertical_move(self.position, move)
                and curr_position.x > move.next_position.x
            ):
                curr_position = Position(
                    curr_position.x - 1,
                    curr_position.y,
                )

            # curr_position = tuple(curr_position)
            path.append(curr_position)

        return path

    def get_possible_moves(self):
        possible_moves = []

        # Iterate over all possible directions a queen can move (horizontal, vertical, and diagonal)
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            # Iterate over all possible distances a queen can move in each direction
            for i in range(1, 8):
                # Calculate the next position based on the direction and distance
                next_pos = Position(self.position.x + dx * i,
                                    self.position.y + dy * i)
                # Check if the next position is within the board bounds
                if 0 <= next_pos.x < 8 and 0 <= next_pos.y < 8:
                    # Add the movement to possible_moves
                    possible_moves.append(
                        Movement(Category.QUEEN, Action.MOVE, next_pos))
                    possible_moves.append(
                        Movement(Category.QUEEN, Action.CAPTURE, next_pos))
                else:
                    # If the next position is outside the board bounds, stop iterating in this direction
                    break

        return possible_moves

    def _is_valid_move(self, move: Movement):
        line_move = is_horizontal_move(
            self.position, move) or is_vertical_move(self.position, move)
        diag_move = is_diagonal_move(self.position, move)

        return line_move or diag_move


class King(Piece):
    def __init__(self, position, color):
        super().__init__(position, color, Category.KING)

    def move(self, move: Movement):
        if is_outside_board(move):
            raise InvalidMovement(
                "Can't move to a position outside the board!")

        if not self._is_valid_move(move):
            raise InvalidMovement()

        self.position = move.next_position

    def get_path(self, move: Movement):
        if not self._is_valid_move(move):
            raise InvalidMovement("Invalid move for King")

        path = []
        curr_position = self.position

        while curr_position != move.next_position:
            dx = move.next_position.x - curr_position.x
            dy = move.next_position.y - curr_position.y

            # Determine the direction of movement
            direction_x = 0 if dx == 0 else dx // abs(dx)
            direction_y = 0 if dy == 0 else dy // abs(dy)

            # Update the current position
            curr_position = Position(
                curr_position.x + direction_x, curr_position.y + direction_y)

            # Add the updated position to the path
            path.append(curr_position)

        return path

    def get_possible_moves(self):
        possible_moves = []

        # Iterate over all adjacent squares
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                # Skip the case where both dx and dy are zero (current position)
                if dx == 0 and dy == 0:
                    continue

                # Calculate the next position based on the current position and the offset
                next_pos = Position(self.position.x + dx, self.position.y + dy)

                # Check if the next position is within the bounds of the board
                if 0 <= next_pos.x < 8 and 0 <= next_pos.y < 8:
                    # Add the movement to possible_moves
                    possible_moves.append(
                        Movement(Category.KING, Action.MOVE, next_pos))
                    possible_moves.append(
                        Movement(Category.KING, Action.CAPTURE, next_pos))

        return possible_moves

    def _is_valid_move(self, move: Movement):
        line_move = is_horizontal_move(
            self.position, move) or is_vertical_move(self.position, move)
        diag_move = is_diagonal_move(self.position, move)
        one_step = is_one_step(self.position, move)

        return (line_move or diag_move) and one_step


class PieceFactory:
    def create_piece(category: Category, position: Position, color: Color):
        if category == Category.PAWN:
            return Pawn(position, color)
        elif category == Category.ROOK:
            return Rook(position, color)
        elif category == Category.KNIGHT:
            return Knight(position, color)
        elif category == Category.BISHOP:
            return Bishop(position, color)
        elif category == Category.QUEEN:
            return Queen(position, color)
        elif category == Category.KING:
            return King(position, color)
        else:
            raise ValueError("Invalid category")
