import unittest
from chess import (
    AlgebraicExpressionParser,
    Category,
    Color,
    Action,
    Movement,
    Board,
    Pawn,
    Rook,
    Knight,
    Bishop,
    Queen,
    King,
    InvalidMovement,
)

class TestAlgebraicExpressionParser(unittest.TestCase):

    def setUp(self):
        self.parser = AlgebraicExpressionParser()

    def test_pawn_move_e4(self):
        expr = "e4"
        move = self.parser.parse(expr)

        expected = Movement(Category.PAWN, Action.MOVE, (4, 4))

        self.assertEqual(expected, move)

    def test_pawn_move_a3(self):
        expr = "a3"
        move = self.parser.parse(expr)

        expected = Movement(Category.PAWN, Action.MOVE, (5, 0))

        self.assertEqual(expected, move)

    def test_knight_move_Nf3(self):
        expr = "Nf3"
        move = self.parser.parse(expr)

        expected = Movement(Category.KNIGHT, Action.MOVE, (5, 5))

        self.assertEqual(expected, move)

    def test_bishop_move_Bc5(self):
        expr = "Bc5"
        move = self.parser.parse(expr)

        expected = Movement(Category.BISHOP, Action.MOVE, (3, 2))

        self.assertEqual(expected, move)

    def test_rook_move_Rg7(self):
        expr = "Rg7"
        move = self.parser.parse(expr)

        expected = Movement(Category.ROOK, Action.MOVE, (1, 6))

        self.assertEqual(expected, move)

    def test_knight_move_Nbd2(self):
        # Special case in which two knights that are on the same
        # file (column) could move the same square.
        expr = "Nbd2"
        move = self.parser.parse(expr)

        expected = Movement(Category.KNIGHT, Action.MOVE, (6, 3), None, 1)

        self.assertEqual(expected, move)

    def test_rook_move_R8c2(self):
        # Special case in which two rooks that are on the same
        # rank (row) could move to the same square.
        expr = "R8c2"
        move = self.parser.parse(expr)

        expected = Movement(Category.ROOK, Action.MOVE, (6, 2), 0, None)

        self.assertEqual(expected, move)

    def test_pawn_capture_cxd5(self):
        expr = "cxd5"
        move = self.parser.parse(expr)

        expected = Movement(Category.PAWN, Action.CAPTURE, (3, 3))

        self.assertEqual(expected, move)

    def test_bishop_capture_Bxc6(self):
        expr = "Bxc6"
        move = self.parser.parse(expr)

        expected = Movement(Category.BISHOP, Action.CAPTURE, (2, 2))

        self.assertEqual(expected, move)

    def test_knight_capture_Nxh7(self):
        expr = "Nxh7"
        move = self.parser.parse(expr)

        expected = Movement(Category.KNIGHT, Action.CAPTURE, (1, 7))

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

        expected = Movement(Category.BISHOP, Action.CHECK, (3, 1))

        self.assertEqual(expected, move)

    def test_check_rook_Rh1(self):
        expr = "Rh1+"
        move = self.parser.parse(expr)

        expected = Movement(Category.ROOK, Action.CHECK, (7, 7))

        self.assertEqual(expected, move)

    def test_check_pawn_a8(self):
        expr = "a8+"
        move = self.parser.parse(expr)

        expected = Movement(Category.PAWN, Action.CHECK, (0, 0))

        self.assertEqual(expected, move)

    def test_checkmate_rook_Rb7(self):
        expr = "Rb7#"
        move = self.parser.parse(expr)

        expected = Movement(Category.ROOK, Action.CHECKMATE, (1, 1))

        self.assertEqual(expected, move)

    def test_checkmate_pawn_e6(self):
        expr = "e6#"
        move = self.parser.parse(expr)

        expected = Movement(Category.PAWN, Action.CHECKMATE, (2, 4))

        self.assertEqual(expected, move)

    def test_promote_d8Q(self):
        expr = "d8=Q"
        move = self.parser.parse(expr)

        expected = Movement(
            Category.PAWN,
            Action.PROMOTE,
            (0, 3),
            None,
            None,
            Category.QUEEN
        )

        self.assertEqual(expected, move)

class TestPawn(unittest.TestCase):

    def test_pawn_is_pawn_category(self):
        pawn = Pawn((0, 0), Color.BLACK)
        self.assertTrue(pawn.category, Category.PAWN)

    def test_valid_move_1_step_black(self):
        pawn = Pawn((1, 0), Color.BLACK)

        movement = Movement(Category.PAWN, Action.MOVE, (2, 0))
        pawn.move(movement)

        self.assertEqual(pawn.position, movement.next_position)

    def test_invalid_move_1_step_black(self):
        pawn = Pawn((1, 0), Color.BLACK)

        movement = Movement(Category.PAWN, Action.MOVE, (5, 0))

        with self.assertRaises(InvalidMovement):
            pawn.move(movement)

    def test_valid_move_1_step_white(self):
        pawn = Pawn((6, 0), Color.WHITE)

        movement = Movement(Category.PAWN, Action.MOVE, (5, 0))
        pawn.move(movement)

        self.assertEqual(pawn.position, movement.next_position)

    def test_invalid_move_1_step_white(self):
        pawn = Pawn((6, 0), Color.WHITE)

        movement = Movement(Category.PAWN, Action.MOVE, (1, 0))
        with self.assertRaises(InvalidMovement):
            pawn.move(movement)

    def test_valid_move_2_step_black(self):
        pawn = Pawn((1, 0), Color.BLACK)

        movement = Movement(Category.PAWN, Action.MOVE, (3, 0))
        pawn.move(movement)

        self.assertEqual(pawn.position, movement.next_position)

    def test_valid_move_2_step_white(self):
        pawn = Pawn((6, 0), Color.WHITE)

        movement = Movement(Category.PAWN, Action.MOVE, (4, 0))
        pawn.move(movement)

        self.assertEqual(pawn.position, movement.next_position)

    def test_invalid_move_outside_top(self):
        pawn = Pawn((0, 0), Color.WHITE)

        movement = Movement(Category.PAWN, Action.MOVE, (-1, 0))

        with self.assertRaises(InvalidMovement):
            pawn.move(movement)

    def test_invalid_move_outside_bottom(self):
        pawn = Pawn((0, 0), Color.WHITE)
        movement = Movement(Category.PAWN, Action.MOVE, (8, 0))

        with self.assertRaises(InvalidMovement):
            pawn.move(movement)

    def test_invalid_move_outside_left(self):
        pawn = Pawn((0, 0), Color.WHITE)
        movement = Movement(Category.PAWN, Action.MOVE, (3, -1))

        with self.assertRaises(InvalidMovement):
            pawn.move(movement)

    def test_invalid_move_outside_right(self):
        pawn = Pawn((0, 0), Color.WHITE)
        movement = Movement(Category.PAWN, Action.MOVE, (5, 8))

        with self.assertRaises(InvalidMovement):
            pawn.move(movement)

    def test_get_path_white(self):
        pawn = Pawn((6, 0), Color.WHITE)
        movement = Movement(Category.PAWN, Action.MOVE, (4, 0))

        path = pawn.get_path(movement)

        self.assertEqual(path, [(5, 0), (4, 0)])

    def test_get_path_black(self):
        pawn = Pawn((1, 0), Color.BLACK)
        movement = Movement(Category.PAWN, Action.MOVE, (3, 0))

        path = pawn.get_path(movement)

        self.assertEqual(path, [(2, 0), (3, 0)])

class TestRook(unittest.TestCase):

    def test_rook_is_rook_category(self):
        rook = Rook((0, 0), Color.BLACK)
        self.assertTrue(rook.category, Category.ROOK)

    def test_invalid_move_outside_top(self):
        rook = Rook((0, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, (-1, 0))

        with self.assertRaises(InvalidMovement):
            rook.move(movement)

    def test_invalid_move_outside_bottom(self):
        rook = Rook((0, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, (9, 0))

        with self.assertRaises(InvalidMovement):
            rook.move(movement)

    def test_invalid_move_outside_left(self):
        rook = Rook((0, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, (2, -2))

        with self.assertRaises(InvalidMovement):
            rook.move(movement)

    def test_invalid_move_outside_right(self):
        rook = Rook((0, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, (2, 10))

        with self.assertRaises(InvalidMovement):
            rook.move(movement)

    def test_valid_move_1_step_vertical(self):
        rook = Rook((4, 4), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, (5, 4))

        rook.move(movement)

        self.assertEqual(rook.position, movement.next_position)

    def test_valid_move_4_step_vertical(self):
        rook = Rook((2, 4), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, (6, 4))

        rook.move(movement)

        self.assertEqual(rook.position, movement.next_position)

    def test_valid_move_1_step_horizontal(self):
        rook = Rook((4, 4), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, (4, 5))

        rook.move(movement)

        self.assertEqual(rook.position, movement.next_position)

    def test_valid_move_4_step_horizontal_right(self):
        rook = Rook((4, 2), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, (4, 6))

        rook.move(movement)

        self.assertEqual(rook.position, movement.next_position)

    def test_get_path_white_vertical_up(self):
        rook = Rook((7, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, (4, 0))

        path = rook.get_path(movement)

        self.assertEqual(path, [(6, 0), (5, 0), (4, 0)])

    def test_get_path_white_vertical_down(self):
        rook = Rook((3, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, (7, 0))

        path = rook.get_path(movement)

        self.assertEqual(path, [(4, 0), (5, 0), (6, 0), (7, 0)])

    def test_get_path_white_horizontal_left(self):
        rook = Rook((4, 7), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, (4, 0))

        path = rook.get_path(movement)

        self.assertEqual(path, [(4, 6), (4, 5), (4, 4), (4, 3), (4, 2), (4, 1), (4, 0)])

    def test_get_path_white_horizontal_right(self):
        rook = Rook((4, 0), Color.WHITE)
        movement = Movement(Category.ROOK, Action.MOVE, (4, 7))

        path = rook.get_path(movement)

        self.assertEqual(path, [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7)])

    #def test_invalid_move_piece_in_way_vertical(self):
    #    rook = Rook((7, 0), Color.WHITE)
    #    movement = Movement(Category.ROOK, Action.MOVE, (5, 0))

    #    with self.assertRaises(InvalidMovement):
    #        rook.move(movement)


class TestKnight(unittest.TestCase):

    def test_invalid_move_outside_top(self):
        knight = Knight((0, 0), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (-1, 2))

        with self.assertRaises(InvalidMovement):
            knight.move(movement)

    def test_invalid_move_outside_bottom(self):
        knight = Knight((7, 7), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (8, 6))

        with self.assertRaises(InvalidMovement):
            knight.move(movement)

    def test_invalid_move_outside_left(self):
        knight = Knight((0, 0), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (1, -2))

        with self.assertRaises(InvalidMovement):
            knight.move(movement)

    def test_invalid_move_outside_right(self):
        knight = Knight((7, 7), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (6, 9))

        with self.assertRaises(InvalidMovement):
            knight.move(movement)

    def test_valid_move_0(self):
        knight = Knight((3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (1, 4))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_1(self):
        knight = Knight((3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (2, 5))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_2(self):
        knight = Knight((3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (4, 5))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_3(self):
        knight = Knight((3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (5, 4))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_4(self):
        knight = Knight((3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (5, 2))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_5(self):
        knight = Knight((3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (4, 1))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_6(self):
        knight = Knight((3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (2, 1))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_valid_move_7(self):
        knight = Knight((3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (1, 2))

        knight.move(movement)

        self.assertTrue(knight.position, movement.next_position)

    def test_invalid_move_0(self):
        knight = Knight((3, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (1, 1))

        with self.assertRaises(InvalidMovement):
            knight.move(movement)

    def test_invalid_move_1(self):
        knight = Knight((4, 3), Color.WHITE)
        movement = Movement(Category.KNIGHT, Action.MOVE, (1, 1))

        with self.assertRaises(InvalidMovement):
            knight.move(movement)



class TestBishop(unittest.TestCase):

    def test_invalid_move_outside_diagonal_1(self):
        bishop = Bishop((0, 0), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, (-1, -1))

        with self.assertRaises(InvalidMovement):
            bishop.move(movement)

    def test_invalid_move_outside_diagonal_2(self):
        bishop = Bishop((0, 7), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, (-1, 8))

        with self.assertRaises(InvalidMovement):
            bishop.move(movement)

    def test_invalid_move_outside_diagonal_3(self):
        bishop = Bishop((7, 7), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, (8, 8))

        with self.assertRaises(InvalidMovement):
            bishop.move(movement)

    def test_invalid_move_outside_diagonal_4(self):
        bishop = Bishop((7, 0), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, (8, -1))

        with self.assertRaises(InvalidMovement):
            bishop.move(movement)

    def test_valid_move_diagonal_1(self):
        bishop = Bishop((3, 3), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, (1, 1))

        bishop.move(movement)

        self.assertEqual(bishop.position, movement.next_position)

    def test_valid_move_diagonal_2(self):
        bishop = Bishop((3, 3), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, (2, 4))

        bishop.move(movement)

        self.assertEqual(bishop.position, movement.next_position)

    def test_valid_move_diagonal_3(self):
        bishop = Bishop((3, 3), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, (7, 7))

        bishop.move(movement)

        self.assertEqual(bishop.position, movement.next_position)

    def test_valid_move_diagonal_4(self):
        bishop = Bishop((3, 3), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, (5, 1))

        bishop.move(movement)

        self.assertEqual(bishop.position, movement.next_position)

    def test_get_path_white_diagonal_1(self):
        bishop = Bishop((4, 4), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, (0, 0))

        path = bishop.get_path(movement)

        self.assertEqual(path, [(3, 3), (2, 2), (1, 1), (0, 0)])

    def test_get_path_white_diagonal_2(self):
        bishop = Bishop((4, 4), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, (1, 7))

        path = bishop.get_path(movement)

        self.assertEqual(path, [(3, 5), (2, 6), (1, 7)])

    def test_get_path_white_diagonal_3(self):
        bishop = Bishop((4, 4), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, (7, 7))

        path = bishop.get_path(movement)

        self.assertEqual(path, [(5, 5), (6, 6), (7, 7)])

    def test_get_path_white_diagonal_4(self):
        bishop = Bishop((4, 4), Color.WHITE)
        movement = Movement(Category.BISHOP, Action.MOVE, (5, 3))

        path = bishop.get_path(movement)

        self.assertEqual(path, [(5, 3)])

class TestQueen(unittest.TestCase):

    def test_invalid_move_outside_diagonal_1(self):
        queen = Queen((0, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (-1, -1))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_diagonal_2(self):
        queen = Queen((0, 7), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (-1, 8))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_diagonal_3(self):
        queen = Queen((7, 7), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (8, 8))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_diagonal_4(self):
        queen = Queen((7, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (8, -1))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_top(self):
        queen = Queen((0, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (-1, 2))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_bottom(self):
        queen = Queen((7, 7), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (8, 6))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_left(self):
        queen = Queen((0, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (1, -2))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_invalid_move_outside_right(self):
        queen = Queen((7, 7), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (6, 9))

        with self.assertRaises(InvalidMovement):
            queen.move(movement)

    def test_valid_move_1(self):
        queen = Queen((0, 0), Color.BLACK)
        movement = Movement(Category.QUEEN, Action.MOVE, (0, 1))

        queen.move(movement)

        self.assertTrue(queen.position, movement.next_position)

    def test_valid_move_2(self):
        queen = Queen((4, 3), Color.BLACK)
        movement = Movement(Category.QUEEN, Action.MOVE, (1, 0))

        queen.move(movement)

        self.assertTrue(queen.position, movement.next_position)

    def test_valid_move_3(self):
        queen = Queen((6, 2), Color.BLACK)
        movement = Movement(Category.QUEEN, Action.MOVE, (6, 7))

        queen.move(movement)

        self.assertTrue(queen.position, movement.next_position)

    def test_valid_move_4(self):
        queen = Queen((1, 6), Color.BLACK)
        movement = Movement(Category.QUEEN, Action.MOVE, (7, 6))

        queen.move(movement)

        self.assertTrue(queen.position, movement.next_position)

    def test_get_path_white_diagonal_1(self):
        queen = Queen((4, 4), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (0, 0))

        path = queen.get_path(movement)

        self.assertEqual(path, [(3, 3), (2, 2), (1, 1), (0, 0)])

    def test_get_path_white_diagonal_2(self):
        queen = Queen((4, 4), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (1, 7))

        path = queen.get_path(movement)

        self.assertEqual(path, [(3, 5), (2, 6), (1, 7)])

    def test_get_path_white_diagonal_3(self):
        queen = Queen((4, 4), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (7, 7))

        path = queen.get_path(movement)

        self.assertEqual(path, [(5, 5), (6, 6), (7, 7)])

    def test_get_path_white_diagonal_4(self):
        queen = Queen((4, 4), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (5, 3))

        path = queen.get_path(movement)

        self.assertEqual(path, [(5, 3)])

    def test_get_path_white_vertical_up(self):
        queen = Queen((7, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (4, 0))

        path = queen.get_path(movement)

        self.assertEqual(path, [(6, 0), (5, 0), (4, 0)])

    def test_get_path_white_vertical_down(self):
        queen = Queen((3, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (7, 0))

        path = queen.get_path(movement)

        self.assertEqual(path, [(4, 0), (5, 0), (6, 0), (7, 0)])

    def test_get_path_white_horizontal_left(self):
        queen = Queen((4, 7), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (4, 0))

        path = queen.get_path(movement)

        self.assertEqual(path, [(4, 6), (4, 5), (4, 4), (4, 3), (4, 2), (4, 1), (4, 0)])

    def test_get_path_white_horizontal_right(self):
        queen = Queen((4, 0), Color.WHITE)
        movement = Movement(Category.QUEEN, Action.MOVE, (4, 7))

        path = queen.get_path(movement)

        self.assertEqual(path, [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7)])


class TestKing(unittest.TestCase):

    def test_invalid_move_outside_diagonal_1(self):
        king = King((0, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (-1, -1))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_diagonal_2(self):
        king = King((0, 7), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (-1, 8))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_diagonal_3(self):
        king = King((7, 7), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (8, 8))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_diagonal_4(self):
        king = King((7, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (8, -1))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_top(self):
        king = King((0, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (-1, 2))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_bottom(self):
        king = King((7, 7), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (8, 6))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_left(self):
        king = King((0, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (1, -2))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_invalid_move_outside_right(self):
        king = King((7, 7), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (6, 9))

        with self.assertRaises(InvalidMovement):
            king.move(movement)

    def test_valid_move_1(self):
        king = King((0, 4), Color.BLACK)
        movement = Movement(Category.KING, Action.MOVE, (0, 5))

        king.move(movement)

        self.assertEqual(king.position, movement.next_position)

    def test_valid_move_2(self):
        king = King((7, 4), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (7, 3))

        king.move(movement)

        self.assertEqual(king.position, movement.next_position)

    def test_valid_move_3(self):
        king = King((3, 7), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (2, 6))

        king.move(movement)

        self.assertEqual(king.position, movement.next_position)

    def test_get_path_white_diagonal_1(self):
        king = King((4, 4), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (3, 3))

        path = king.get_path(movement)

        self.assertEqual(path, [(3, 3)])

    def test_get_path_white_diagonal_2(self):
        king = King((4, 4), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (3, 5))

        path = king.get_path(movement)

        self.assertEqual(path, [(3, 5)])

    def test_get_path_white_diagonal_3(self):
        king = King((4, 4), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (5, 5))

        path = king.get_path(movement)

        self.assertEqual(path, [(5, 5)])

    def test_get_path_white_diagonal_4(self):
        king = King((4, 4), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (5, 3))

        path = king.get_path(movement)

        self.assertEqual(path, [(5, 3)])

    def test_get_path_white_vertical_up(self):
        king = King((7, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (6, 0))

        path = king.get_path(movement)

        self.assertEqual(path, [(6, 0)])

    def test_get_path_white_vertical_down(self):
        king = King((3, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (4, 0))

        path = king.get_path(movement)

        self.assertEqual(path, [(4, 0)])

    def test_get_path_white_horizontal_left(self):
        king = King((4, 7), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (4, 6))

        path = king.get_path(movement)

        self.assertEqual(path, [(4, 6)])

    def test_get_path_white_horizontal_right(self):
        king = King((4, 0), Color.WHITE)
        movement = Movement(Category.KING, Action.MOVE, (4, 1))

        path = king.get_path(movement)

        self.assertEqual(path, [(4, 1)])


class TestBoard(unittest.TestCase):

    def setUp(self):
        pieces = []
        self.board = Board(pieces)



if __name__ == "__main__":
    unittest.main()
