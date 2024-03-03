from models import (
    Action,
    Category,
    Movement,
    Position,
)


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
            return Movement(Category.PAWN, Action.CAPTURE, Position(row, col))

        piece = Category(expr[0])
        return Movement(piece, Action.CAPTURE, Position(row, col))

    def _parse_castling_king(self, expr):
        return Movement(Category.KING, Action.CASTLING_KING, None)

    def _parse_castling_queen(self, expr):
        return Movement(Category.KING, Action.CASTLING_QUEEN, None)

    def _parse_check(self, expr):
        if len(expr) == 3:
            # Pawn checks
            col = self._letter_to_num(expr[0])
            row = self._parse_row(expr[1])
            return Movement(Category.PAWN, Action.CHECK, Position(row, col))

        piece = Category(expr[0])
        col = self._letter_to_num(expr[1])
        row = self._parse_row(expr[2])

        return Movement(piece, Action.CHECK, Position(row, col))

    def _parse_checkmate(self, expr):
        if len(expr) == 3:
            # Pawn checks
            col = self._letter_to_num(expr[0])
            row = self._parse_row(expr[1])
            return Movement(
                Category.PAWN,
                Action.CHECKMATE,
                Position(row, col),
            )

        piece = Category(expr[0])
        col = self._letter_to_num(expr[1])
        row = self._parse_row(expr[2])

        return Movement(piece, Action.CHECKMATE, Position(row, col))

    def _parse_promote(self, expr):
        col = self._letter_to_num(expr[0])
        row = self._parse_row(expr[1])
        next_category = Category(expr[-1])

        return Movement(
            Category.PAWN,
            Action.PROMOTE,
            Position(row, col),
            None,
            None,
            next_category,
        )

    def _parse_move(self, expr):
        # First char is the piece letter.
        # In case of pawn, piece letter is omitted.
        if len(expr) == 2:
            # Pawn movement
            col = self._letter_to_num(expr[0])
            row = self._parse_row(expr[1])

            return Movement(Category.PAWN, Action.MOVE, Position(row, col))
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

            return Movement(
                piece,
                Action.MOVE,
                Position(row, col),
                current_row,
                current_col
            )
        else:
            piece = Category(expr[0])
            col = self._letter_to_num(expr[1])
            row = self._parse_row(expr[2])

            return Movement(piece, Action.MOVE, Position(row, col))

    def _letter_to_num(self, letter):
        """Transform the file (letter) to a number representation."""
        return ord(letter) - ord("a")

    def _parse_row(self, original_row):
        return 8 - int(original_row)
