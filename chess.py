import os
import copy
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
    PieceFactory,
)
from typing import List, Tuple


class Board:
    def __init__(self, pieces: List[Piece]):
        self.pieces: List[Piece] = pieces
        self.history_movements: List[Tuple[Piece, Movement]] = []
        self.captured_pieces: List[Piece] = []

    # TODO: next_state
    def perform_movement(self, move: Movement, color: Color):
        if move.action == Action.MOVE:
            self._move(move, color)
        elif move.action == Action.CASTLING_KING:
            self._castling_king(move, color)
        elif move.action == Action.CASTLING_QUEEN:
            self._castling_queen(move, color)
        elif move.action == Action.CAPTURE:
            self._capture(move, color)
        elif move.action == Action.CHECK:
            self._check(move, color)
        elif move.action == Action.CHECKMATE:
            self._checkmate(move, color)
        elif move.action == Action.PROMOTE:
            self._promote(move, color)
        else:
            raise InvalidMovement()

    def _move(self, move: Movement, color: Color):
        if not self._is_square_empty(move.next_position):
            raise InvalidMovement("Target square is not empty!")

        possible_pieces = self._get_possible_pieces(move, color)
        # At this point, there must be only one valid piece,
        # although there could be multiple pieces with the
        # same color and category
        # i.e. only one piece can move to the next position.
        moved = False
        piece_moved = None
        for p in possible_pieces:
            try:
                if move.category != Category.KNIGHT:
                    # Check if there is a piece in the way
                    if self._piece_in_the_way(p, move):
                        continue
                p.move(move)
                moved = True
                piece_moved = copy.deepcopy(p)
            except InvalidMovement:
                continue

        if not moved:
            raise InvalidMovement()

        current_board = copy.deepcopy(self)
        if current_board._can_piece_capture_king(piece_moved, color):
            move.action = Action.CHECK

        self.history_movements.append((piece_moved, move))

    def _castling_king(self, move: Movement, color: Color):
        # TODO: refactor

        # KING SIDE RULES:
        # - g1 and f1 or g8 and f8 free.
        # - King cannot have moved.
        # - Rook (right) cannot have moved.
        # - King cannot be in check.
        # - King cannot pass through check.

        if color == Color.WHITE:
            if not self._is_square_empty(Position(7, 5)) and not self._is_square_empty(Position(7, 6)):
                raise InvalidMovement("g1 and f1 must be free.")
        else:
            # Check if the squares at (0, 5) and (0, 6) are empty
            if not self._is_square_empty(Position(0, 5)) and not self._is_square_empty(Position(0, 6)):
                raise InvalidMovement("g8 and f8 must be free.")

        for piece, move in self.history_movements:
            # King cannot have moved.
            if self._king_has_moved(color):
                raise InvalidMovement(
                    "Your king has been moved previously.")

            # Right Rook cannot have moved.
            if self._right_rook_has_moved(color):
                raise InvalidMovement(
                    "Your right rook has been moved previously.")

        # King cannot be in check.
        if self._is_king_in_check(color):
            raise InvalidMovement("Your king is in check!")

        if self._is_king_passing_through_check(color):
            raise InvalidMovement("Your king pass through check!")

        king = self._get_king(color)
        right_rook = [p for p in self.pieces if p.category ==
                      Category.ROOK and p.color == color and p.position.y == 7][0]

        if color == Color.WHITE:
            king.position = Position(7, 6)
            right_rook.position = Position(7, 5)
        else:
            king.position = Position(0, 6)
            right_rook.position = Position(0, 5)

    def _castling_queen(self, move: Movement, color: Color):
        # TODO: refactor

        # QUEEN SIDE RULES:
        # - c1 and d1 or c8 and d8 free.
        # - King cannot have moved.
        # - Rook (left) cannot have moved.
        # - King cannot be in check.
        # - King cannot pass through check.

        if color == Color.WHITE:
            if not self._is_square_empty(Position(7, 1)) and not self._is_square_empty(Position(7, 2)) and not self._is_square_empty(Position(7, 3)):
                raise InvalidMovement("b1, c1, and d1 must be free.")
        else:
            if not self._is_square_empty(Position(0, 1)) and not self._is_square_empty(Position(0, 2)) and not self._is_square_empty(Position(0, 3)):
                raise InvalidMovement("b8, c8, and d8 must be free.")

        for piece, move in self.history_movements:
            # King cannot have moved.
            if self._king_has_moved(color):
                raise InvalidMovement(
                    "Your king has been moved previously.")

            # Right Rook cannot have moved.
            if self._left_rook_has_moved(color):
                raise InvalidMovement(
                    "Your right rook has been moved previously.")

        # King cannot be in check.
        if self._is_king_in_check(color):
            raise InvalidMovement("Your king is in check!")

        if self._is_king_passing_through_check(color):
            raise InvalidMovement("Your king pass through check!")

        king = self._get_king(color)
        left_rook = [p for p in self.pieces if p.category ==
                     Category.ROOK and p.color == color and p.position.y == 0][0]

        if color == Color.WHITE:
            king.position = Position(7, 2)
            left_rook.position = Position(7, 3)
        else:
            king.position = Position(0, 2)
            left_rook.position = Position(0, 3)

    def _capture(self, move: Movement, color: Color):
        if self._is_square_empty(move.next_position):
            raise InvalidMovement("You cannot capture an empty square!")

        possible_pieces = self._get_possible_pieces(move, color)
        # At this point, there must be only one valid piece,
        # although there could be multiple pieces with the
        # same color and category
        # i.e. only one piece can move to the next position.
        moved = False
        piece_moved = None
        piece_captured = self._get_piece(move.next_position)

        for p in possible_pieces:
            try:
                if move.category != Category.KNIGHT and move.category != Category.PAWN:
                    # Check if there is a piece in the way
                    if self._piece_in_the_way_without_last_position(p, move):
                        continue
                p.move(move)
                moved = True
                self.captured_pieces.append(piece_captured)
                self.pieces.remove(piece_captured)
                piece_moved = copy.deepcopy(p)
            except InvalidMovement:
                continue

        if not moved:
            raise InvalidMovement()

        self.history_movements.append((piece_moved, move))

    def _check(self, move: Movement, color: Color):
        # We need to check if the king will be in check after the movement.
        if not self._will_enemy_king_be_in_check(move, color):
            raise InvalidMovement("Enemy king will not be in check!")

        # At this point, we can actually perform the check movement.
        self._move(move, color)
        # Remove last history movement because the previous _move
        # already added the movement to the history movements.
        last_movement = self.history_movements.pop()
        move.action = Action.CHECK
        self.history_movements.append((last_movement[0], move))

    def _promote(self, move: Movement, color: Color):
        if move.next_category == Category.PAWN:
            raise InvalidMovement("You cannot promote to a pawn!")

        move.action = Action.MOVE
        self._move(move, color)

        old_piece = self.history_movements[-1][0]
        new_piece = PieceFactory.create_piece(
            category=move.next_category, position=old_piece.position, color=old_piece.color)

        self.pieces.remove(
            [p for p in self.pieces if p.position == old_piece.position][0])
        self.pieces.append(new_piece)

    def _will_enemy_king_be_in_check(self, move: Movement, color: Color):
        # TODO: refactor and abstract
        current_board = copy.deepcopy(self)

        if move.action == Action.CHECK:
            move.action = Action.MOVE

        current_board.perform_movement(move, color)

        piece = current_board.history_movements[-1][0]

        return current_board._can_piece_capture_king(piece, color)

    def _can_piece_capture_king(self, piece: Piece, color: Color):
        enemy_color = self._get_enemy_color(color)
        king = self._get_king(enemy_color)

        try:
            self.perform_movement(
                Movement(
                    piece.category,
                    Action.CAPTURE,
                    king.position
                ),
                color
            )
        except InvalidMovement:
            return False

        return True

    def _checkmate(self, move: Movement, color: Color):
        # TODO: efficient way to checkmate
        pass

    def _get_king(self, color: Color):
        return [p for p in self.pieces if p.category == Category.KING and p.color == color][0]

    def _get_piece(self, position: Position):
        for piece in self.pieces:
            if piece.position == position:
                return piece

        return None

    def _king_has_moved(self, color):
        for piece, move in self.history_movements:
            if piece.category == Category.KING and piece.color == color:
                return True

        return False

    def _right_rook_has_moved(self, color):
        for piece, move in self.history_movements:
            if piece.category == Category.ROOK and piece.color == color and piece.position.y == 7:
                return True

        return False

    def _left_rook_has_moved(self, color):
        for piece, move in self.history_movements:
            if piece.category == Category.ROOK and piece.color == color and piece.position.y == 0:
                return True

        return False

    def _is_king_passing_through_check(self, color):
        if color == Color.WHITE:
            positions_to_check = [Position(x=7, y=5), Position(x=7, y=6)]
        else:
            positions_to_check = [Position(x=0, y=5), Position(x=0, y=6)]

        enemy_color = self._get_enemy_color(color)
        # King cannot pass through check.
        for position in positions_to_check:
            current_board = copy.deepcopy(self)
            current_board.perform_movement(
                Movement(Category.KING, Action.MOVE, position), color)
            enemy_pieces = [
                p for p in current_board.pieces if p.color == enemy_color]

            for enemy_piece in enemy_pieces:
                try:
                    current_board.perform_movement(
                        Movement(
                            enemy_piece.category,
                            Action.CAPTURE,
                            position
                        ),
                        enemy_color
                    )
                    return True
                except InvalidMovement:
                    continue

        return False

    def _get_enemy_color(self, current_color):
        return Color.BLACK if current_color == Color.WHITE else Color.WHITE

    def _is_king_in_check(self, color: Color):
        return self.history_movements[-1][1].action == Action.CHECK and self.history_movements[-1][0].color != color

    def _get_possible_pieces(self, move: Movement, color: Color):
        possible_pieces = [
            p for p in self.pieces if p.category == move.category and p.color == color
        ]

        if move.current_row is not None:
            possible_pieces = [
                p for p in possible_pieces if p.position.x == move.current_row]

        if move.current_col is not None:
            possible_pieces = [
                p for p in possible_pieces if p.position.y == move.current_col]

        if move.category == Category.PAWN and move.action == Action.MOVE:
            return [
                p for p in possible_pieces if p.position.y == move.next_position.y
            ]

        if move.category == Category.PAWN and move.action == Action.CAPTURE:
            return [
                p for p in possible_pieces if abs(p.position.x - move.next_position.x) == 1 and abs(p.position.y - move.next_position.y) == 1
            ]

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

    def _piece_in_the_way_without_last_position(self, piece: Piece, move: Movement):
        path = piece.get_path(move)[:-1]

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
        print()

    def __str__(self):
        pass


class Game:
    def __init__(self, board, parser):
        self.board = board
        self.parser = parser
        # stack with all board states
        self.board_states = [copy.deepcopy(self.board)]
        self.current_board_state_idx = 0
        self.current_turn = Color.WHITE

    def play(self):
        show_error = False
        error_msg = ""
        # begins infinite loop
        while 1:
            self._clear_screen()
            self._show_game()
            if show_error:
                print(error_msg)
                show_error = False

            player_input = self._get_player_input()

            if player_input == "":
                continue
            if player_input == "exit":
                break
            elif player_input == "undo":
                if self.current_board_state_idx == 0:
                    error_msg = "No more undos available."
                    show_error = True
                    continue

                self.current_board_state_idx -= 1
                self.board = self.board_states[self.current_board_state_idx]
                self._next_turn()
                continue
            elif player_input == "redo":
                if self.current_board_state_idx == len(self.board_states) - 1:
                    error_msg = "No more redos available."
                    show_error = True
                    continue

                self.current_board_state_idx += 1
                self.board = self.board_states[self.current_board_state_idx]
                self._next_turn()
                continue
            elif player_input == "how":
                self._show_how()
                continue
            elif player_input == "help":
                self._show_help()
                continue

            try:
                player_movement = self.parser.parse(player_input)
                self.board.perform_movement(player_movement, self.current_turn)
                self._next_turn()
                self._save_board_state()
            except InvalidMovement:
                error_msg = "Invalid movement. Try again!"
                show_error = True
            except ValueError:
                raise
                error_msg = "Invalid category. Try again!"
                show_error = True

    def _get_player_input(self):
        player_input = input(self._get_player_prompt())
        player_input = player_input.strip()
        return player_input

    def _get_player_prompt(self):
        return f"{self.current_turn} > "

    def _save_board_state(self):
        self.board_states.append(copy.deepcopy(self.board))
        self.current_board_state_idx += 1

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

    def _show_game(self):
        print("Welcome to Chess CLI Py!")
        print("Type 'help' for more information.")
        print()
        self.board.show()

    def _show_help(self):
        print()
        print("Type 'exit' to leave the game.")
        print("Type 'undo' to undo the last movement.")
        print("Type 'redo' to redo the last undone.")
        print("Type 'how' to show the movement notation.")
        print("Type 'help' to show this message.")
        input("Press any key to continue...")

    def _show_how(self):
        print()
        print("Movement is coded using algebraic notation. For example:")
        print("  - 'e4' means move the pawn to the e4 square.")
        print("  - 'Nf3' means move the knight to the f3 square.")
        print("  - 'O-O' means castling king side.")
        print("  - 'O-O-O' means castling queen side.")
        print("  - 'exd5' means capture the pawn at d5 with the e pawn.")
        print("  - 'Nxd5' means capture the pawn at d5 with the knight.")
        print()
        print(
            "See 'https://www.chess.com/terms/chess-notation' for more information.")
        input("Press any key to continue...")


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
