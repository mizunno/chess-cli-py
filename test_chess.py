import unittest
from models import (
    Category,
    Color,
    Action,
    Movement,
    Position,
    Pawn,
    Rook,
    Knight,
    Bishop,
    Queen,
    King,
    InvalidMovement,
    Checkmate,
)
from algebraic_expression_parser import AlgebraicExpressionParser
from chess import (
    Board,
    get_initial_board,
)


class TestAlgebraicExpressionParser(unittest.TestCase):
    def setUp(self):
        self.parser = AlgebraicExpressionParser()

    def test_pawn_move_e4(self):
        expr = "e4"
        move = self.parser.parse(expr)

        expected = Movement(Category.PAWN, Action.MOVE, Position(4, 4))

        self.assertEqual(expected, move)

    def test_pawn_move_a3(self):
        expr = "a3"
        move = self.parser.parse(expr)

        expected = Movement(Category.PAWN, Action.MOVE, Position(5, 0))

        self.assertEqual(expected, move)

    def test_knight_move_Nf3(self):
        expr = "Nf3"
        move = self.parser.parse(expr)

        expected = Movement(Category.KNIGHT, Action.MOVE, Position(5, 5))

        self.assertEqual(expected, move)

    def test_bishop_move_Bc5(self):
        expr = "Bc5"
        move = self.parser.parse(expr)

        expected = Movement(Category.BISHOP, Action.MOVE, Position(3, 2))

        self.assertEqual(expected, move)

    def test_rook_move_Rg7(self):
        expr = "Rg7"
        move = self.parser.parse(expr)

        expected = Movement(Category.ROOK, Action.MOVE, Position(1, 6))

        self.assertEqual(expected, move)

    def test_knight_move_Nbd2(self):
        # Special case in which two knights that are on the same
        # file (column) could move the same square.
        expr = "Nbd2"
        move = self.parser.parse(expr)

        expected = Movement(
            Category.KNIGHT,
            Action.MOVE,
            Position(6, 3),
            None,
            1
        )

        self.assertEqual(expected, move)

    def test_rook_move_R8c2(self):
        # Special case in which two rooks that are on the same
        # rank (row) could move to the same square.
        expr = "R8c2"
        move = self.parser.parse(expr)

        expected = Movement(
            Category.ROOK,
            Action.MOVE,
            Position(6, 2),
            0,
            None
        )

        self.assertEqual(expected, move)

    def test_pawn_capture_cxd5(self):
        expr = "cxd5"
        move = self.parser.parse(expr)

        expected = Movement(Category.PAWN, Action.CAPTURE, Position(3, 3))

        self.assertEqual(expected, move)

    def test_bishop_capture_Bxc6(self):
        expr = "Bxc6"
        move = self.parser.parse(expr)

        expected = Movement(Category.BISHOP, Action.CAPTURE, Position(2, 2))

        self.assertEqual(expected, move)

    def test_knight_capture_Nxh7(self):
        expr = "Nxh7"
        move = self.parser.parse(expr)

        expected = Movement(Category.KNIGHT, Action.CAPTURE, Position(1, 7))

        self.assertEqual(expected, move)

    def test_castling_king_side(self):
        expr = "O-O"
        move = self.parser.parse(expr)

        expected = Movement(Category.KING, Action.CASTLING_KING, None)

        self.assertEqual(expected, move)

    def test_castling_queen_side(self):
        expr = "O-O-O"
        move = self.parser.parse(expr)

        expected = Movement(Category.KING, Action.CASTLING_QUEEN, None)

        self.assertEqual(expected, move)

    def test_check_bishop_Bb5(self):
        expr = "Bb5+"
        move = self.parser.parse(expr)

        expected = Movement(Category.BISHOP, Action.CHECK, Position(3, 1))

        self.assertEqual(expected, move)

    def test_check_rook_Rh1(self):
        expr = "Rh1+"
        move = self.parser.parse(expr)

        expected = Movement(Category.ROOK, Action.CHECK, Position(7, 7))

        self.assertEqual(expected, move)

    def test_check_pawn_a8(self):
        expr = "a8+"
        move = self.parser.parse(expr)

        expected = Movement(Category.PAWN, Action.CHECK, Position(0, 0))

        self.assertEqual(expected, move)

    def test_checkmate_rook_Rb7(self):
        expr = "Rb7#"
        move = self.parser.parse(expr)

        expected = Movement(Category.ROOK, Action.CHECKMATE, Position(1, 1))

        self.assertEqual(expected, move)

    def test_checkmate_pawn_e6(self):
        expr = "e6#"
        move = self.parser.parse(expr)

        expected = Movement(Category.PAWN, Action.CHECKMATE, Position(2, 4))

        self.assertEqual(expected, move)

    def test_promote_d8Q(self):
        expr = "d8=Q"
        move = self.parser.parse(expr)

        expected = Movement(
            Category.PAWN,
            Action.PROMOTE,
            Position(0, 3),
            None,
            None,
            Category.QUEEN,
        )

        self.assertEqual(expected, move)

    def test_invalid_category(self):
        expr = "bd5"
        with self.assertRaises(ValueError):
            self.parser.parse(expr)


class TestPawn(unittest.TestCase):
    def test_pawn_is_pawn_category(self):
        pawn = Pawn(Position(0, 0), Color.BLACK)
        self.assertTrue(pawn.category, Category.PAWN)

    def test_valid_move_1_step_black(self):
        pawn = Pawn(Position(1, 0), Color.BLACK)

        movement = Movement(Category.PAWN, Action.MOVE, Position(2, 0))
        pawn.move(movement)

        self.assertEqual(pawn.position, movement.next_position)

    def test_invalid_move_1_step_black(self):
        pawn = Pawn(Position(1, 0), Color.BLACK)

        movement = Movement(Category.PAWN, Action.MOVE, Position(5, 0))

        with self.assertRaises(InvalidMovement):
            pawn.move(movement)

    def test_valid_move_1_step_white(self):
        pawn = Pawn(Position(6, 0), Color.WHITE)

        movement = Movement(Category.PAWN, Action.MOVE, Position(5, 0))
        pawn.move(movement)

        self.assertEqual(pawn.position, movement.next_position)

    def test_invalid_move_1_step_white(self):
        pawn = Pawn(Position(6, 0), Color.WHITE)

        movement = Movement(Category.PAWN, Action.MOVE, Position(1, 0))
        with self.assertRaises(InvalidMovement):
            pawn.move(movement)

    def test_valid_move_2_step_black(self):
        pawn = Pawn(Position(1, 0), Color.BLACK)

        movement = Movement(Category.PAWN, Action.MOVE, Position(3, 0))
        pawn.move(movement)

        self.assertEqual(pawn.position, movement.next_position)

    def test_valid_move_2_step_white(self):
        pawn = Pawn(Position(6, 0), Color.WHITE)

        movement = Movement(Category.PAWN, Action.MOVE, Position(4, 0))
        pawn.move(movement)

        self.assertEqual(pawn.position, movement.next_position)

    def test_invalid_move_outside_top(self):
        pawn = Pawn(Position(0, 0), Color.WHITE)

        movement = Movement(Category.PAWN, Action.MOVE, Position(-1, 0))

        with self.assertRaises(InvalidMovement):
            pawn.move(movement)

    def test_invalid_move_outside_bottom(self):
        pawn = Pawn(Position(0, 0), Color.WHITE)
        movement = Movement(Category.PAWN, Action.MOVE, Position(8, 0))

        with self.assertRaises(InvalidMovement):
            pawn.move(movement)

    def test_invalid_move_outside_left(self):
        pawn = Pawn(Position(0, 0), Color.WHITE)
        movement = Movement(Category.PAWN, Action.MOVE, Position(3, -1))

        with self.assertRaises(InvalidMovement):
            pawn.move(movement)

    def test_invalid_move_outside_right(self):
        pawn = Pawn(Position(0, 0), Color.WHITE)
        movement = Movement(Category.PAWN, Action.MOVE, Position(5, 8))

        with self.assertRaises(InvalidMovement):
            pawn.move(movement)

    def test_get_path_white(self):
        pawn = Pawn(Position(6, 0), Color.WHITE)
        movement = Movement(Category.PAWN, Action.MOVE, Position(4, 0))

        path = pawn.get_path(movement)

        self.assertEqual(path, [Position(5, 0), Position(4, 0)])

    def test_get_path_black(self):
        pawn = Pawn(Position(1, 0), Color.BLACK)
        movement = Movement(Category.PAWN, Action.MOVE, Position(3, 0))

        path = pawn.get_path(movement)

        self.assertEqual(path, [Position(2, 0), Position(3, 0)])

    def test_get_possible_moves_white_left_border(self):
        pawn = Pawn(Position(6, 0), Color.WHITE)

        moves = pawn.get_possible_moves()
        expected = [
            Movement(Category.PAWN, Action.MOVE, Position(5, 0)),
            Movement(Category.PAWN, Action.MOVE, Position(4, 0)),
            Movement(Category.PAWN, Action.CAPTURE, Position(5, 1)),
        ]

        self.assertEqual(moves, expected)

    def test_get_possible_moves_white_right_border(self):
        pawn = Pawn(Position(6, 7), Color.WHITE)

        moves = pawn.get_possible_moves()
        expected = [
            Movement(Category.PAWN, Action.MOVE, Position(5, 7)),
            Movement(Category.PAWN, Action.MOVE, Position(4, 7)),
            Movement(Category.PAWN, Action.CAPTURE, Position(5, 6)),
        ]

        self.assertEqual(moves, expected)

    def test_get_possible_moves_black_left_border(self):
        pawn = Pawn(Position(1, 0), Color.BLACK)

        moves = pawn.get_possible_moves()
        expected = [
            Movement(Category.PAWN, Action.MOVE, Position(2, 0)),
            Movement(Category.PAWN, Action.MOVE, Position(3, 0)),
            Movement(Category.PAWN, Action.CAPTURE, Position(2, 1)),
        ]

        self.assertEqual(moves, expected)

    def test_get_possible_moves_black_right_border(self):
        pawn = Pawn(Position(1, 7), Color.BLACK)

        moves = pawn.get_possible_moves()
        expected = [
            Movement(Category.PAWN, Action.MOVE, Position(2, 7)),
            Movement(Category.PAWN, Action.MOVE, Position(3, 7)),
            Movement(Category.PAWN, Action.CAPTURE, Position(2, 6)),
        ]

        self.assertEqual(moves, expected)


class TestRook(unittest.TestCase):
    def test_rook_is_rook_category(self):
        rook = Rook(Position(0, 0), Color.BLACK)
        self.assertTrue(rook.category, Category.ROOK)

    def test_invalid_move_outside_top(self):
        rook = Rook(Position(0, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, Position(-1, 0))

        with self.assertRaises(InvalidMovement):
            rook.move(movement)

    def test_invalid_move_outside_bottom(self):
        rook = Rook(Position(0, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, Position(9, 0))

        with self.assertRaises(InvalidMovement):
            rook.move(movement)

    def test_invalid_move_outside_left(self):
        rook = Rook(Position(0, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, Position(2, -2))

        with self.assertRaises(InvalidMovement):
            rook.move(movement)

    def test_invalid_move_outside_right(self):
        rook = Rook(Position(0, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, Position(2, 10))

        with self.assertRaises(InvalidMovement):
            rook.move(movement)

    def test_valid_move_1_step_vertical(self):
        rook = Rook(Position(4, 4), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, Position(5, 4))

        rook.move(movement)

        self.assertEqual(rook.position, movement.next_position)

    def test_valid_move_4_step_vertical(self):
        rook = Rook(Position(2, 4), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, Position(6, 4))

        rook.move(movement)

        self.assertEqual(rook.position, movement.next_position)

    def test_valid_move_1_step_horizontal(self):
        rook = Rook(Position(4, 4), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, Position(4, 5))

        rook.move(movement)

        self.assertEqual(rook.position, movement.next_position)

    def test_valid_move_4_step_horizontal_right(self):
        rook = Rook(Position(4, 2), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, Position(4, 6))

        rook.move(movement)

        self.assertEqual(rook.position, movement.next_position)

    def test_get_path_white_vertical_up(self):
        rook = Rook(Position(7, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, Position(4, 0))

        path = rook.get_path(movement)

        self.assertEqual(path, [
            Position(6, 0),
            Position(5, 0),
            Position(4, 0),
        ])

    def test_get_path_white_vertical_down(self):
        rook = Rook(Position(3, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, Position(7, 0))

        path = rook.get_path(movement)

        self.assertEqual(path, [
            Position(4, 0),
            Position(5, 0),
            Position(6, 0),
            Position(7, 0),
        ])

    def test_get_path_white_horizontal_left(self):
        rook = Rook(Position(4, 7), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, Position(4, 0))

        path = rook.get_path(movement)

        self.assertEqual(path, [
            Position(4, 6),
            Position(4, 5),
            Position(4, 4),
            Position(4, 3),
            Position(4, 2),
            Position(4, 1),
            Position(4, 0),
        ])

    def test_get_path_white_horizontal_right(self):
        rook = Rook(Position(4, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, Position(4, 7))

        path = rook.get_path(movement)

        self.assertEqual(path, [
            Position(4, 1),
            Position(4, 2),
            Position(4, 3),
            Position(4, 4),
            Position(4, 5),
            Position(4, 6),
            Position(4, 7),
        ])

    def test_get_possible_moves(self):
        rook = Rook(Position(3, 3), Color.WHITE)
        possible_moves = rook.get_possible_moves()

        expected_moves = []
        # Rook can move horizontally and vertically
        for i in range(8):
            if i != rook.position.y:
                expected_moves.append(
                    Movement(Category.ROOK, Action.MOVE, Position(rook.position.x, i)))
                expected_moves.append(
                    Movement(Category.ROOK, Action.CAPTURE, Position(rook.position.x, i)))

            if i != rook.position.x:
                expected_moves.append(
                    Movement(Category.ROOK, Action.MOVE, Position(i, rook.position.y)))
                expected_moves.append(
                    Movement(Category.ROOK, Action.CAPTURE, Position(i, rook.position.y)))

        # Check if the obtained moves match the expected moves
        self.assertCountEqual(possible_moves, expected_moves)


class TestKnight(unittest.TestCase):
    def test_invalid_move_outside_top(self):
        knight = Knight(Position(0, 0), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(-1, 2))

        with self.assertRaises(InvalidMovement):
            knight.move(movement)

    def test_invalid_move_outside_bottom(self):
        knight = Knight(Position(7, 7), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(8, 6))

        with self.assertRaises(InvalidMovement):
            knight.move(movement)

    def test_invalid_move_outside_left(self):
        knight = Knight(Position(0, 0), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(1, -2))

        with self.assertRaises(InvalidMovement):
            knight.move(movement)

    def test_invalid_move_outside_right(self):
        knight = Knight(Position(7, 7), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(6, 9))

        with self.assertRaises(InvalidMovement):
            knight.move(movement)

    def test_valid_move_0(self):
        knight = Knight(Position(3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(1, 4))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_1(self):
        knight = Knight(Position(3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(2, 5))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_2(self):
        knight = Knight(Position(3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(4, 5))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_3(self):
        knight = Knight(Position(3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(5, 4))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_4(self):
        knight = Knight(Position(3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(5, 2))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_5(self):
        knight = Knight(Position(3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(4, 1))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_6(self):
        knight = Knight(Position(3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(2, 1))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_7(self):
        knight = Knight(Position(3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(1, 2))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_invalid_move_0(self):
        knight = Knight(Position(3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(1, 1))

        with self.assertRaises(InvalidMovement):
            knight.move(movement)

    def test_invalid_move_1(self):
        knight = Knight(Position(4, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, Position(1, 1))

        with self.assertRaises(InvalidMovement):
            knight.move(movement)

    def test_get_possible_moves(self):
        knight = Knight(Position(3, 3), Color.WHITE)
        possible_moves = knight.get_possible_moves()

        knight_relative_positions = [
            (-2, 1),
            (-1, 2),
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1),
        ]

        expected_moves = []
        # Rook can move horizontally and vertically
        for dx, dy in knight_relative_positions:
            expected_moves.append(
                Movement(Category.KNIGHT, Action.MOVE, Position(knight.position.x + dx, knight.position.y + dy)))
            expected_moves.append(
                Movement(Category.KNIGHT, Action.CAPTURE, Position(knight.position.x + dx, knight.position.y + dy)))

        # Check if the obtained moves match the expected moves
        self.assertCountEqual(possible_moves, expected_moves)


class TestBishop(unittest.TestCase):
    def test_invalid_move_outside_diagonal_1(self):
        bishop = Bishop(Position(0, 0), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, Position(-1, -1))

        with self.assertRaises(InvalidMovement):
            bishop.move(movement)

    def test_invalid_move_outside_diagonal_2(self):
        bishop = Bishop(Position(0, 7), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, Position(-1, 8))

        with self.assertRaises(InvalidMovement):
            bishop.move(movement)

    def test_invalid_move_outside_diagonal_3(self):
        bishop = Bishop(Position(7, 7), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, Position(8, 8))

        with self.assertRaises(InvalidMovement):
            bishop.move(movement)

    def test_invalid_move_outside_diagonal_4(self):
        bishop = Bishop(Position(7, 0), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, Position(8, -1))

        with self.assertRaises(InvalidMovement):
            bishop.move(movement)

    def test_valid_move_diagonal_1(self):
        bishop = Bishop(Position(3, 3), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, Position(1, 1))

        bishop.move(movement)

        self.assertEqual(bishop.position, movement.next_position)

    def test_valid_move_diagonal_2(self):
        bishop = Bishop(Position(3, 3), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, Position(2, 4))

        bishop.move(movement)

        self.assertEqual(bishop.position, movement.next_position)

    def test_valid_move_diagonal_3(self):
        bishop = Bishop(Position(3, 3), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, Position(7, 7))

        bishop.move(movement)

        self.assertEqual(bishop.position, movement.next_position)

    def test_valid_move_diagonal_4(self):
        bishop = Bishop(Position(3, 3), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, Position(5, 1))

        bishop.move(movement)

        self.assertEqual(bishop.position, movement.next_position)

    def test_get_path_white_diagonal_1(self):
        bishop = Bishop(Position(4, 4), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, Position(0, 0))

        path = bishop.get_path(movement)

        self.assertEqual(path, [
            Position(3, 3),
            Position(2, 2),
            Position(1, 1),
            Position(0, 0),
        ])

    def test_get_path_white_diagonal_2(self):
        bishop = Bishop(Position(4, 4), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, Position(1, 7))

        path = bishop.get_path(movement)

        self.assertEqual(path, [
            Position(3, 5),
            Position(2, 6),
            Position(1, 7),
        ])

    def test_get_path_white_diagonal_3(self):
        bishop = Bishop(Position(4, 4), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, Position(7, 7))

        path = bishop.get_path(movement)

        self.assertEqual(path, [
            Position(5, 5),
            Position(6, 6),
            Position(7, 7),
        ])

    def test_get_path_white_diagonal_4(self):
        bishop = Bishop(Position(4, 4), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, Position(5, 3))

        path = bishop.get_path(movement)

        self.assertEqual(path, [Position(5, 3)])


class TestQueen(unittest.TestCase):
    def test_invalid_move_outside_diagonal_1(self):
        queen = Queen(Position(0, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(-1, -1))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_diagonal_2(self):
        queen = Queen(Position(0, 7), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(-1, 8))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_diagonal_3(self):
        queen = Queen(Position(7, 7), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(8, 8))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_diagonal_4(self):
        queen = Queen(Position(7, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(8, -1))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_top(self):
        queen = Queen(Position(0, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(-1, 2))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_bottom(self):
        queen = Queen(Position(7, 7), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(8, 6))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_left(self):
        queen = Queen(Position(0, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(1, -2))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_right(self):
        queen = Queen(Position(7, 7), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(6, 9))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_valid_move_1(self):
        queen = Queen(Position(0, 0), Color.BLACK)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(0, 1))

        queen.move(movement)

        self.assertTrue(queen.position, movement.next_position)

    def test_valid_move_2(self):
        queen = Queen(Position(4, 3), Color.BLACK)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(1, 0))

        queen.move(movement)

        self.assertTrue(queen.position, movement.next_position)

    def test_valid_move_3(self):
        queen = Queen(Position(6, 2), Color.BLACK)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(6, 7))

        queen.move(movement)

        self.assertTrue(queen.position, movement.next_position)

    def test_valid_move_4(self):
        queen = Queen(Position(1, 6), Color.BLACK)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(7, 6))

        queen.move(movement)

        self.assertTrue(queen.position, movement.next_position)

    def test_get_path_white_diagonal_1(self):
        queen = Queen(Position(4, 4), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(0, 0))

        path = queen.get_path(movement)

        self.assertEqual(path, [
            Position(3, 3),
            Position(2, 2),
            Position(1, 1),
            Position(0, 0),
        ])

    def test_get_path_white_diagonal_2(self):
        queen = Queen(Position(4, 4), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(1, 7))

        path = queen.get_path(movement)

        self.assertEqual(path, [
            Position(3, 5),
            Position(2, 6),
            Position(1, 7),
        ])

    def test_get_path_white_diagonal_3(self):
        queen = Queen(Position(4, 4), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(7, 7))

        path = queen.get_path(movement)

        self.assertEqual(path, [
            Position(5, 5),
            Position(6, 6),
            Position(7, 7),
        ])

    def test_get_path_white_diagonal_4(self):
        queen = Queen(Position(4, 4), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(5, 3))

        path = queen.get_path(movement)

        self.assertEqual(path, [Position(5, 3)])

    def test_get_path_white_vertical_up(self):
        queen = Queen(Position(7, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(4, 0))

        path = queen.get_path(movement)

        self.assertEqual(path, [
            Position(6, 0),
            Position(5, 0),
            Position(4, 0),
        ])

    def test_get_path_white_vertical_down(self):
        queen = Queen(Position(3, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(7, 0))

        path = queen.get_path(movement)

        self.assertEqual(path, [
            Position(4, 0),
            Position(5, 0),
            Position(6, 0),
            Position(7, 0),
        ])

    def test_get_path_white_horizontal_left(self):
        queen = Queen(Position(4, 7), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(4, 0))

        path = queen.get_path(movement)

        self.assertEqual(path, [
            Position(4, 6),
            Position(4, 5),
            Position(4, 4),
            Position(4, 3),
            Position(4, 2),
            Position(4, 1),
            Position(4, 0),
        ])

    def test_get_path_white_horizontal_right(self):
        queen = Queen(Position(4, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, Position(4, 7))

        path = queen.get_path(movement)

        self.assertEqual(path, [
            Position(4, 1),
            Position(4, 2),
            Position(4, 3),
            Position(4, 4),
            Position(4, 5),
            Position(4, 6),
            Position(4, 7),
        ])


class TestKing(unittest.TestCase):
    def test_invalid_move_outside_diagonal_1(self):
        king = King(Position(0, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(-1, -1))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_diagonal_2(self):
        king = King(Position(0, 7), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(-1, 8))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_diagonal_3(self):
        king = King(Position(7, 7), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(8, 8))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_diagonal_4(self):
        king = King(Position(7, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(8, -1))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_top(self):
        king = King(Position(0, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(-1, 2))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_bottom(self):
        king = King(Position(7, 7), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(8, 6))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_left(self):
        king = King(Position(0, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(1, -2))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_right(self):
        king = King(Position(7, 7), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(6, 9))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_valid_move_1(self):
        king = King(Position(0, 4), Color.BLACK)
        movement = Movement(Category.KING, Action.MOVE, Position(0, 5))

        king.move(movement)

        self.assertEqual(king.position, movement.next_position)

    def test_valid_move_2(self):
        king = King(Position(7, 4), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(7, 3))

        king.move(movement)

        self.assertEqual(king.position, movement.next_position)

    def test_valid_move_3(self):
        king = King(Position(3, 7), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(2, 6))

        king.move(movement)

        self.assertEqual(king.position, movement.next_position)

    def test_get_path_white_diagonal_1(self):
        king = King(Position(4, 4), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(3, 3))

        path = king.get_path(movement)

        self.assertEqual(path, [Position(3, 3)])

    def test_get_path_white_diagonal_2(self):
        king = King(Position(4, 4), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(3, 5))

        path = king.get_path(movement)

        self.assertEqual(path, [Position(3, 5)])

    def test_get_path_white_diagonal_3(self):
        king = King(Position(4, 4), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(5, 5))

        path = king.get_path(movement)

        self.assertEqual(path, [Position(5, 5)])

    def test_get_path_white_diagonal_4(self):
        king = King(Position(4, 4), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(5, 3))

        path = king.get_path(movement)

        self.assertEqual(path, [Position(5, 3)])

    def test_get_path_white_vertical_up(self):
        king = King(Position(7, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(6, 0))

        path = king.get_path(movement)

        self.assertEqual(path, [Position(6, 0)])

    def test_get_path_white_vertical_down(self):
        king = King(Position(3, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(4, 0))

        path = king.get_path(movement)

        self.assertEqual(path, [Position(4, 0)])

    def test_get_path_white_horizontal_left(self):
        king = King(Position(4, 7), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(4, 6))

        path = king.get_path(movement)

        self.assertEqual(path, [Position(4, 6)])

    def test_get_path_white_horizontal_right(self):
        king = King(Position(4, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, Position(4, 1))

        path = king.get_path(movement)

        self.assertEqual(path, [Position(4, 1)])


class TestBoardCastling(unittest.TestCase):

    def setUp(self):
        pieces = self.get_initial_pieces_castling()
        self.board = Board(pieces)

    def get_initial_pieces_castling(self):
        # 8 |  R  |     |     |     |  K  |     |     |  R  |
        #  --------------------------------------------------
        # 7 |  P  |  P  |  P  |     |     |  P  |  P  |  P  |
        #  --------------------------------------------------
        # 6 |     |     |     |     |     |     |     |     |
        # --------------------------------------------------
        # 5 |     |     |     |     |     |     |     |     |
        # --------------------------------------------------
        # 4 |     |     |     |     |     |     |     |     |
        # --------------------------------------------------
        # 3 |     |     |     |     |     |     |     |     |
        # --------------------------------------------------
        # 2 |  P' |  P' |  P' |     |     |  P' |  P' |  P' |
        # --------------------------------------------------
        # 1 |  R' |     |     |     |  K' |     |     |  R' |
        # --------------------------------------------------
        #      a     b     c     d     e     f     g     h

        pieces = []
        # WHITE
        pieces.append(Pawn(position=Position(6, 0), color=Color.WHITE))
        pieces.append(Pawn(position=Position(6, 1), color=Color.WHITE))
        pieces.append(Pawn(position=Position(6, 2), color=Color.WHITE))
        pieces.append(Pawn(position=Position(6, 5), color=Color.WHITE))
        pieces.append(Pawn(position=Position(6, 6), color=Color.WHITE))
        pieces.append(Pawn(position=Position(6, 7), color=Color.WHITE))
        pieces.append(Rook(position=Position(7, 0), color=Color.WHITE))
        pieces.append(Rook(position=Position(7, 7), color=Color.WHITE))
        pieces.append(King(position=Position(7, 4), color=Color.WHITE))

        # BLACK
        pieces.append(Pawn(position=Position(1, 0), color=Color.BLACK))
        pieces.append(Pawn(position=Position(1, 1), color=Color.BLACK))
        pieces.append(Pawn(position=Position(1, 2), color=Color.BLACK))
        pieces.append(Pawn(position=Position(1, 5), color=Color.BLACK))
        pieces.append(Pawn(position=Position(1, 6), color=Color.BLACK))
        pieces.append(Pawn(position=Position(1, 7), color=Color.BLACK))
        pieces.append(Rook(position=Position(0, 0), color=Color.BLACK))
        pieces.append(Rook(position=Position(0, 7), color=Color.BLACK))
        pieces.append(King(position=Position(0, 4), color=Color.BLACK))

        return pieces

    def test_castling_king_white(self):
        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)
        king = [p for p in self.board.pieces if p.category ==
                Category.KING and p.color == Color.WHITE][0]
        right_rook = [p for p in self.board.pieces if p.category ==
                      Category.ROOK and p.color == Color.WHITE and p.position.y == 7][0]
        self.board.perform_movement(move, Color.WHITE)

        self.assertEqual(king.position.x, 7)
        self.assertEqual(king.position.y, 6)
        self.assertEqual(right_rook.position.x, 7)
        self.assertEqual(right_rook.position.y, 5)

    def test_castling_king_black(self):
        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)
        king = [p for p in self.board.pieces if p.category ==
                Category.KING and p.color == Color.BLACK][0]
        right_rook = [p for p in self.board.pieces if p.category ==
                      Category.ROOK and p.color == Color.BLACK and p.position.y == 7][0]
        self.board.perform_movement(move, Color.BLACK)

        self.assertEqual(king.position.x, 0)
        self.assertEqual(king.position.y, 6)
        self.assertEqual(right_rook.position.x, 0)
        self.assertEqual(right_rook.position.y, 5)

    def test_castling_king_white_no_space(self):
        # - g1 and f1 or g8 and f8 are not free.
        self.board.pieces.append(Pawn(Position(7, 6), Color.WHITE))
        self.board.pieces.append(Pawn(Position(7, 5), Color.WHITE))
        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)
        with self.assertRaises(InvalidMovement):
            self.board.perform_movement(move, Color.WHITE)

    def test_castling_king_black_no_space(self):
        # - g1 and f1 or g8 and f8 are not free.
        self.board.pieces.append(Pawn(Position(0, 6), Color.BLACK))
        self.board.pieces.append(Pawn(Position(0, 5), Color.BLACK))
        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)
        with self.assertRaises(InvalidMovement):
            self.board.perform_movement(move, Color.BLACK)

    def test_castling_king_white_king_moved(self):
        # - King has moved.
        self.board.history_movements.append((
            King(position=Position(7, 4), color=Color.WHITE),
            Movement(category=Category.KING, action=Action.MOVE,
                     next_position=Position(7, 5))
        ))

        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)
        with self.assertRaises(InvalidMovement):
            self.board.perform_movement(move, Color.WHITE)

    def test_castling_king_black_king_moved(self):
        # - King has moved.
        self.board.history_movements.append((
            King(position=Position(0, 4), color=Color.BLACK),
            Movement(category=Category.KING, action=Action.MOVE,
                     next_position=Position(0, 5))
        ))

        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)
        with self.assertRaises(InvalidMovement):
            self.board.perform_movement(move, Color.BLACK)

    def test_castling_king_white_rook_moved(self):
        # - Rook has moved.
        self.board.history_movements.append((
            Rook(position=Position(7, 7), color=Color.WHITE),
            Movement(category=Category.ROOK, action=Action.MOVE,
                     next_position=Position(6, 7))
        ))

        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)
        with self.assertRaises(InvalidMovement):
            self.board.perform_movement(move, Color.WHITE)

    def test_castling_king_black_rook_moved(self):
        # - Rook has moved.
        self.board.history_movements.append((
            Rook(position=Position(0, 7), color=Color.BLACK),
            Movement(category=Category.ROOK, action=Action.MOVE,
                     next_position=Position(1, 7))
        ))

        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)
        with self.assertRaises(InvalidMovement):
            self.board.perform_movement(move, Color.BLACK)

    def test_castling_king_white_king_in_check(self):
        # - King is in check.
        self.board.pieces.append(
            Queen(position=Position(4, 4), color=Color.BLACK))
        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)
        with self.assertRaises(InvalidMovement):
            self.board.perform_movement(move, Color.WHITE)

    def test_castling_king_black_king_in_check(self):
        # - King is in check.
        self.board.pieces.append(
            Queen(position=Position(4, 4), color=Color.WHITE))
        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)
        with self.assertRaises(InvalidMovement):
            self.board.perform_movement(move, Color.BLACK)

    def test_castling_king_white_king_passes_through_check_in_7_5(self):
        # - King passes through check.
        # Add piece that puts king in check in position 7, 5
        self.board.pieces.append(Bishop(Position(5, 3), Color.BLACK))
        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)

        with self.assertRaises(InvalidMovement):
            self.board.perform_movement(move, Color.WHITE)

    def test_castling_king_white_king_passes_through_check_in_7_6(self):
        # - King passes through check.

        # Add a previous movement to avoid king is in check checking from firing
        self.board.history_movements.append((
            Pawn(position=Position(1, 5), color=Color.BLACK),
            Movement(category=Category.PAWN, action=Action.CHECK,
                     next_position=Position(2, 5))
        ))

        # Add piece that puts king in check in position 7, 6
        self.board.pieces.append(Knight(Position(5, 5), Color.BLACK))
        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)

        with self.assertRaises(InvalidMovement):
            self.board.perform_movement(move, Color.WHITE)

    def test_castling_king_black_king_passes_through_check_in_0_5(self):
        # - King passes through check.

        # Add a previous movement to avoid king is in check checking from firing
        self.board.history_movements.append((
            Pawn(position=Position(1, 5), color=Color.WHITE),
            Movement(category=Category.PAWN, action=Action.CHECK,
                     next_position=Position(2, 5))
        ))

        # Add piece that puts king in check in position 0, 5
        self.board.pieces.append(Bishop(Position(2, 3), Color.WHITE))
        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)

        with self.assertRaises(InvalidMovement):
            self.board.perform_movement(move, Color.BLACK)

    def test_castling_king_black_king_passes_through_check_in_0_6(self):
        # - King passes through check.

        # Add a previous movement to avoid king is in check checking from firing
        self.board.history_movements.append((
            Pawn(position=Position(1, 5), color=Color.WHITE),
            Movement(category=Category.PAWN, action=Action.CHECK,
                     next_position=Position(2, 5))
        ))

        # Add piece that puts king in check in position 0, 6
        self.board.pieces.append(Knight(Position(2, 5), Color.WHITE))
        move = Movement(category=Category.KING,
                        action=Action.CASTLING_KING, next_position=None)

        with self.assertRaises(InvalidMovement):
            self.board.perform_movement(move, Color.BLACK)

    def test_castling_queen_white(self):
        # We need to populate history movements with atleast one movement
        # because we just created the board and history_movements is empty
        self.board.history_movements.append((
            Pawn(position=Position(1, 0), color=Color.BLACK),
            Movement(category=Category.PAWN, action=Action.MOVE,
                     next_position=Position(2, 0))
        ))

        move = Movement(category=Category.KING,
                        action=Action.CASTLING_QUEEN, next_position=None)
        king = [p for p in self.board.pieces if p.category ==
                Category.KING and p.color == Color.WHITE][0]
        left_rook = [p for p in self.board.pieces if p.category ==
                     Category.ROOK and p.color == Color.WHITE and p.position.y == 0][0]
        self.board.perform_movement(move, Color.WHITE)

        self.assertEqual(king.position.x, 7)
        self.assertEqual(king.position.y, 2)
        self.assertEqual(left_rook.position.x, 7)
        self.assertEqual(left_rook.position.y, 3)

    def test_castling_queen_black(self):
        # We need to populate history movements with atleast one movement
        # because we just created the board and history_movements is empty
        self.board.history_movements.append((
            Pawn(position=Position(6, 0), color=Color.WHITE),
            Movement(category=Category.PAWN, action=Action.MOVE,
                     next_position=Position(5, 0))
        ))

        move = Movement(category=Category.KING,
                        action=Action.CASTLING_QUEEN, next_position=None)
        king = [p for p in self.board.pieces if p.category ==
                Category.KING and p.color == Color.BLACK][0]
        left_rook = [p for p in self.board.pieces if p.category ==
                     Category.ROOK and p.color == Color.BLACK and p.position.y == 0][0]
        self.board.perform_movement(move, Color.BLACK)

        self.assertEqual(king.position.x, 0)
        self.assertEqual(king.position.y, 2)
        self.assertEqual(left_rook.position.x, 0)
        self.assertEqual(left_rook.position.y, 3)


class TestBoardCapture(unittest.TestCase):

    def test_pawn_white_capture_1(self):
        pieces = [
            Pawn(position=Position(3, 3), color=Color.WHITE),
            Pawn(position=Position(2, 4), color=Color.BLACK),
            King(position=Position(0, 5), color=Color.WHITE),
            King(position=Position(7, 5), color=Color.BLACK),
        ]

        board = Board(pieces)
        move = Movement(category=Category.PAWN,
                        action=Action.CAPTURE, next_position=Position(2, 4))

        board.perform_movement(move, Color.WHITE)

        self.assertEqual(len(board.pieces), 3)
        self.assertEqual(board.pieces[0].position, Position(2, 4))
        self.assertEqual(board.pieces[0].color, Color.WHITE)

    def test_pawn_white_capture_2(self):
        pieces = [
            Pawn(position=Position(3, 3), color=Color.WHITE),
            Pawn(position=Position(2, 2), color=Color.BLACK),
            King(position=Position(0, 5), color=Color.WHITE),
            King(position=Position(7, 5), color=Color.BLACK),
        ]

        board = Board(pieces)
        move = Movement(category=Category.PAWN,
                        action=Action.CAPTURE, next_position=Position(2, 2))

        board.perform_movement(move, Color.WHITE)

        self.assertEqual(len(board.pieces), 3)
        self.assertEqual(board.pieces[0].position, Position(2, 2))
        self.assertEqual(board.pieces[0].color, Color.WHITE)

    def test_pawn_black_capture_1(self):
        pieces = [
            Pawn(position=Position(3, 3), color=Color.BLACK),
            Pawn(position=Position(4, 2), color=Color.WHITE),
            King(position=Position(0, 5), color=Color.WHITE),
            King(position=Position(7, 5), color=Color.BLACK),
        ]

        board = Board(pieces)
        move = Movement(category=Category.PAWN,
                        action=Action.CAPTURE, next_position=Position(4, 2))

        board.perform_movement(move, Color.BLACK)

        self.assertEqual(len(board.pieces), 3)
        self.assertEqual(board.pieces[0].position, Position(4, 2))
        self.assertEqual(board.pieces[0].color, Color.BLACK)

    def test_pawn_black_capture_2(self):
        pieces = [
            Pawn(position=Position(3, 3), color=Color.BLACK),
            Pawn(position=Position(4, 4), color=Color.WHITE),
            King(position=Position(0, 5), color=Color.WHITE),
            King(position=Position(7, 5), color=Color.BLACK),
        ]

        board = Board(pieces)
        move = Movement(category=Category.PAWN,
                        action=Action.CAPTURE, next_position=Position(4, 4))

        board.perform_movement(move, Color.BLACK)

        self.assertEqual(len(board.pieces), 3)
        self.assertEqual(board.pieces[0].position, Position(4, 4))
        self.assertEqual(board.pieces[0].color, Color.BLACK)

    def test_knight_white_capture(self):
        pieces = [
            Knight(position=Position(3, 3), color=Color.WHITE),
            Pawn(position=Position(1, 2), color=Color.BLACK),
            King(position=Position(0, 5), color=Color.WHITE),
            King(position=Position(7, 5), color=Color.BLACK),
        ]

        board = Board(pieces)
        move = Movement(category=Category.KNIGHT,
                        action=Action.CAPTURE, next_position=Position(1, 2))

        board.perform_movement(move, Color.WHITE)

        self.assertEqual(len(board.pieces), 3)
        self.assertEqual(board.pieces[0].position, Position(1, 2))
        self.assertEqual(board.pieces[0].color, Color.WHITE)

    def test_bishop_black_capture(self):
        pieces = [
            Bishop(position=Position(3, 3), color=Color.BLACK),
            Pawn(position=Position(1, 1), color=Color.WHITE),
            King(position=Position(0, 5), color=Color.WHITE),
            King(position=Position(7, 5), color=Color.BLACK),
        ]

        board = Board(pieces)
        move = Movement(category=Category.BISHOP,
                        action=Action.CAPTURE, next_position=Position(1, 1))

        board.perform_movement(move, Color.BLACK)

        self.assertEqual(len(board.pieces), 3)
        self.assertEqual(board.pieces[0].position, Position(1, 1))
        self.assertEqual(board.pieces[0].color, Color.BLACK)

    def test_rook_white_capture(self):
        pieces = [
            Rook(position=Position(3, 3), color=Color.WHITE),
            Pawn(position=Position(3, 1), color=Color.BLACK),
            King(position=Position(0, 5), color=Color.WHITE),
            King(position=Position(7, 5), color=Color.BLACK),
        ]

        board = Board(pieces)
        move = Movement(category=Category.ROOK,
                        action=Action.CAPTURE, next_position=Position(3, 1))

        board.perform_movement(move, Color.WHITE)

        self.assertEqual(len(board.pieces), 3)
        self.assertEqual(board.pieces[0].position, Position(3, 1))
        self.assertEqual(board.pieces[0].color, Color.WHITE)

    def test_queen_black_capture(self):
        pieces = [
            Queen(position=Position(3, 3), color=Color.BLACK),
            Pawn(position=Position(1, 5), color=Color.WHITE),
            King(position=Position(0, 5), color=Color.WHITE),
            King(position=Position(7, 5), color=Color.BLACK),
        ]

        board = Board(pieces)
        move = Movement(category=Category.QUEEN,
                        action=Action.CAPTURE, next_position=Position(1, 5))

        board.perform_movement(move, Color.BLACK)

        self.assertEqual(len(board.pieces), 3)
        self.assertEqual(board.pieces[0].position, Position(1, 5))
        self.assertEqual(board.pieces[0].color, Color.BLACK)

    def test_king_white_capture(self):
        pieces = [
            King(position=Position(3, 3), color=Color.WHITE),
            Pawn(position=Position(2, 3), color=Color.BLACK),
            King(position=Position(7, 5), color=Color.BLACK),
        ]

        board = Board(pieces)
        move = Movement(category=Category.KING,
                        action=Action.CAPTURE, next_position=Position(2, 3))

        board.perform_movement(move, Color.WHITE)

        self.assertEqual(len(board.pieces), 2)
        self.assertEqual(board.pieces[0].position, Position(2, 3))
        self.assertEqual(board.pieces[0].color, Color.WHITE)


class TestBoardCheck(unittest.TestCase):

    def setUp(self):
        pieces = self.get_initial_pieces_check()
        self.board = Board(pieces)

    def get_initial_pieces_check(self):
        pieces = []
        # WHITE
        pieces.append(King(position=Position(7, 4), color=Color.WHITE))
        # BLACK
        pieces.append(King(position=Position(0, 4), color=Color.BLACK))

        return pieces

    def test_check_white_with_pawn(self):
        # Add piece that puts king in check in position d2
        self.board.pieces.append(Pawn(Position(5, 3), Color.BLACK))

        move = Movement(category=Category.PAWN, action=Action.CHECK,
                        next_position=Position(6, 3))

        self.board.perform_movement(move, Color.BLACK)

        self.assertTrue(self.board._is_king_in_check(Color.WHITE))

    def test_check_black_with_pawn(self):
        # Add piece that puts king in check in position d2
        self.board.pieces.append(Pawn(Position(2, 3), Color.WHITE))

        move = Movement(category=Category.PAWN, action=Action.CHECK,
                        next_position=Position(1, 3))

        self.board.perform_movement(move, Color.WHITE)

        self.assertTrue(self.board._is_king_in_check(Color.BLACK))

    def test_move_ends_up_in_check(self):
        # Add piece that puts king in check in position d2
        self.board.pieces.append(Pawn(Position(5, 3), Color.BLACK))

        move = Movement(category=Category.PAWN, action=Action.MOVE,
                        next_position=Position(6, 3))

        self.board.perform_movement(move, Color.BLACK)

        self.assertTrue(self.board._is_king_in_check(Color.WHITE))


class TestBoardPromote(unittest.TestCase):

    def setUp(self):
        pieces = self.get_initial_pieces_promote()
        self.board = Board(pieces)

    def get_initial_pieces_promote(self):
        pieces = []
        # WHITE
        # King is added because a valid game has always kings
        pieces.append(King(position=Position(0, 4), color=Color.BLACK))
        pieces.append(Pawn(position=Position(6, 0), color=Color.BLACK))
        # BLACK
        pieces.append(King(position=Position(7, 4), color=Color.WHITE))
        pieces.append(Pawn(position=Position(1, 0), color=Color.WHITE))

        return pieces

    def test_promote_to_queen_black(self):
        move = Movement(
            category=Category.PAWN,
            action=Action.PROMOTE,
            next_position=Position(7, 0),
            next_category=Category.QUEEN,
        )
        self.board.perform_movement(move, Color.BLACK)

        new_piece = [
            p for p in self.board.pieces if p.position == Position(7, 0)][0]

        self.assertTrue(new_piece.category == Category.QUEEN)
        self.assertTrue(new_piece.color == Color.BLACK)

    def test_promote_to_queen_white(self):
        move = Movement(
            category=Category.PAWN,
            action=Action.PROMOTE,
            next_position=Position(0, 0),
            next_category=Category.QUEEN,
        )
        self.board.perform_movement(move, Color.WHITE)

        new_piece = [
            p for p in self.board.pieces if p.position == Position(0, 0)][0]

        self.assertTrue(new_piece.category == Category.QUEEN)
        self.assertTrue(new_piece.color == Color.WHITE)


class TestBoardCheckmate(unittest.TestCase):

    def setUp(self):
        pieces = self.get_initial_pieces_checkmate()
        self.board = Board(pieces)

    def get_initial_pieces_checkmate(self):
        pieces = []
        # WHITE
        pieces.append(King(position=Position(7, 4), color=Color.WHITE))
        # BLACK
        pieces.append(King(position=Position(0, 4), color=Color.BLACK))

        return pieces

    def test_checkmate_white(self):
        # Add piece that puts king in check in position d2
        self.board.pieces.append(Rook(Position(0, 3), Color.BLACK))
        self.board.pieces.append(Rook(Position(0, 5), Color.BLACK))
        self.board.pieces.append(Queen(Position(4, 4), Color.WHITE))

        move = Movement(category=Category.QUEEN, action=Action.CHECKMATE,
                        next_position=Position(2, 4))

        with self.assertRaises(Checkmate):
            self.board.perform_movement(move, Color.WHITE)

    def test_invalid_checkmate_white(self):
        # Add piece that puts king in check in position d2
        self.board.pieces.append(Rook(Position(7, 3), Color.WHITE))
        self.board.pieces.append(Rook(Position(7, 5), Color.WHITE))
        self.board.pieces.append(Queen(Position(3, 4), Color.BLACK))

        move = Movement(category=Category.QUEEN, action=Action.CHECKMATE,
                        next_position=Position(4, 4))

        with self.assertRaises(InvalidMovement):
            self.board.perform_movement(move, Color.BLACK)


if __name__ == "__main__":
    unittest.main()
