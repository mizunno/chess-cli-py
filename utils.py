from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Movement, Position


def is_outside_board(move: Movement):
    return (
        move.next_position.x < 0
        or move.next_position.x > 7
        or move.next_position.y < 0
        or move.next_position.y > 7
    )


def is_vertical_move(position: Position, move: Movement):
    return (
        position.y == move.next_position.y
        and position.x != move.next_position.x
    )


def is_horizontal_move(position: Position, move: Movement):
    return (
        position.x == move.next_position.x
        and position.y != move.next_position.y
    )


def is_diagonal_move(position: Position, move: Movement):
    p1, p2 = subtract_positions(position, move)
    return p1 == p2


def is_one_step(position: Position, move: Movement):
    p1, p2 = subtract_positions(position, move)
    return (p1 + p2) <= 2


def subtract_positions(position: Position, move: Movement):
    p1 = abs(position.x - move.next_position.x)
    p2 = abs(position.y - move.next_position.y)

    return p1, p2
