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
            pass

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


class Rook(Piece):
    def __init__(self, position: Position, color: Color):
        super().__init__(position, color, Category.ROOK)

    def move(self, move: Movement):
        if is_outside_board(move):
            raise InvalidMovement(
                "Can't move to a position outside the board!")

        if move.action == Action.MOVE:
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

    def _is_valid_move(self, move: Movement):
        return (
            is_horizontal_move(self.position, move)
            or is_vertical_move(self.position, move)
        )


class Knight(Piece):
    def __init__(self, position, color):
        super().__init__(position, color, Category.KNIGHT)

    def move(self, move: Movement):
        if is_outside_board(move):
            raise InvalidMovement(
                "Can't move to a position outside the board!")

        if move.action == Action.MOVE:
            if not self._is_valid_move(move):
                raise InvalidMovement()

            self.position = move.next_position

    def get_path(self, move: Movement):
        return []

    def _is_valid_move(self, move: Movement):
        possible_moves = [
            (-2, 1),
            (-1, 2),
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1),
        ]

        for x, y in possible_moves:
            possible_next_pos = Position(
                self.position.x + x,
                self.position.y + y,
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

        if move.action == Action.MOVE:
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

        if move.action == Action.MOVE:
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

        if move.action == Action.MOVE:
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

    def _is_valid_move(self, move: Movement):
        line_move = is_horizontal_move(
            self.position, move) or is_vertical_move(self.position, move)
        diag_move = is_diagonal_move(self.position, move)
        one_step = is_one_step(self.position, move)

        return (line_move or diag_move) and one_step
