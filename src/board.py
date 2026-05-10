from __future__ import annotations

from .models import Board, BoardFrame, MoveResult, Node, Position, State

DIRECTIONS: dict[str, tuple[int, int]] = {
    "U": (-1, 0),
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
}

DIRECTION_ORDER: tuple[str, ...] = ("U", "R", "D", "L")


def start_state(board: Board) -> State:
    return (board.start_pos[0], board.start_pos[1], 0)


def in_bounds(board: Board, row: int, col: int) -> bool:
    return 0 <= row < board.rows and 0 <= col < board.cols


def tile_at(board: Board, row: int, col: int) -> str:
    return board.base_grid[row][col]


def is_goal(board: Board, state: State) -> bool:
    row, col, next_number = state
    return (row, col) == board.goal_pos and next_number == board.required_count


def simulate_move(board: Board, state: State, direction: str) -> MoveResult | None:
    if direction not in DIRECTIONS:
        return None

    row, col, next_number = state
    dr, dc = DIRECTIONS[direction]
    total_cost = 0
    moved = False
    traversed_cells: list[Position] = []

    while True:
        next_row = row + dr
        next_col = col + dc

        if not in_bounds(board, next_row, next_col):
            return None

        tile = tile_at(board, next_row, next_col)
        if tile == "X":
            if not moved:
                return None
            return MoveResult(
                new_state=(row, col, next_number),
                move_cost=total_cost,
                traversed_cells=traversed_cells,
                action=direction,
            )

        moved = True
        traversed_cells.append((next_row, next_col))
        total_cost += board.costs[next_row][next_col]

        if tile == "L":
            return None

        if tile.isdigit():
            digit = int(tile)
            if digit < next_number:
                pass
            elif digit == next_number:
                next_number += 1
            else:
                return None

        row = next_row
        col = next_col


def render_board_lines(
    board: Board,
    actor_pos: Position | None = None,
    next_number: int | None = None,
) -> list[str]:
    lines: list[str] = []
    for row_index, row_text in enumerate(board.base_grid):
        chars = list(row_text)
        if next_number is not None:
            for col_index, char in enumerate(chars):
                if char.isdigit() and int(char) < next_number:
                    chars[col_index] = "*"
        if actor_pos is not None and row_index == actor_pos[0]:
            chars[actor_pos[1]] = "Z"
        lines.append("".join(chars))
    return lines


def render_board_text(
    board: Board,
    actor_pos: Position | None = None,
    next_number: int | None = None,
) -> str:
    return "\n".join(render_board_lines(board, actor_pos, next_number))


def make_frame(
    board: Board,
    node: Node,
    title: str,
    step_index: int,
    kind: str,
    action: str | None = None,
) -> BoardFrame:
    row, col, next_number = node.state
    return BoardFrame(
        board_text=render_board_text(board, (row, col), next_number),
        actor_pos=(row, col),
        state=node.state,
        title=title,
        action=action,
        step_index=step_index,
        g=node.g,
        h=node.h,
        f=node.f,
        next_number=next_number,
        kind=kind,
    )
