from __future__ import annotations

from collections.abc import Callable

from .models import Board, Position, State

HeuristicFunction = Callable[[Board, State], float]


def manhattan(first: Position, second: Position) -> int:
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def next_targets(board: Board, state: State) -> tuple[Position, ...]:
    row, col, next_number = state
    if next_number < board.required_count:
        return board.digit_positions.get(next_number, ())
    return (board.goal_pos,)


def h1(board: Board, state: State) -> float:
    row, col, _ = state
    current = (row, col)
    targets = next_targets(board, state)
    if not targets:
        return 0.0
    return float(min(manhattan(current, target) for target in targets))


def h2(board: Board, state: State) -> float:
    row, col, next_number = state
    distances: dict[Position, int] = {(row, col): 0}

    for digit in range(next_number, board.required_count):
        targets = board.digit_positions.get(digit, ())
        if not targets:
            return 0.0
        next_distances: dict[Position, int] = {}
        for target in targets:
            next_distances[target] = min(
                distance + manhattan(position, target)
                for position, distance in distances.items()
            )
        distances = next_distances

    return float(
        min(
            distance + manhattan(position, board.goal_pos)
            for position, distance in distances.items()
        )
    )


def h3(board: Board, state: State) -> float:
    return h2(board, state) * board.min_passable_cost


HEURISTICS: dict[str, HeuristicFunction] = {
    "H1": h1,
    "H2": h2,
    "H3": h3,
}


def get_heuristic(name: str | None) -> HeuristicFunction:
    if not name:
        return h1
    key = name.strip().upper()
    if key not in HEURISTICS:
        available = ", ".join(sorted(HEURISTICS))
        raise ValueError(f"Heuristic tidak dikenal: {name}. Pilihan: {available}.")
    return HEURISTICS[key]
