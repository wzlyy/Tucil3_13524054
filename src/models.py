from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

Position = tuple[int, int]
State = tuple[int, int, int]


class InputValidationError(Exception):
    """Raised when an input file cannot be used as a puzzle board."""


@dataclass(frozen=True)
class Board:
    rows: int
    cols: int
    base_grid: tuple[str, ...]
    costs: tuple[tuple[int, ...], ...]
    start_pos: Position
    goal_pos: Position
    digit_positions: dict[int, tuple[Position, ...]] = field(default_factory=dict)
    source_path: Optional[str] = None
    min_passable_cost: int = 0

    @property
    def required_count(self) -> int:
        return max(self.digit_positions.keys(), default=-1) + 1

    @property
    def max_digit(self) -> int:
        return self.required_count - 1


@dataclass(frozen=True)
class MoveResult:
    new_state: State
    move_cost: int
    traversed_cells: list[Position]
    action: str


@dataclass
class Node:
    state: State
    g: float
    h: float = 0.0
    action: Optional[str] = None
    parent: Optional["Node"] = None
    move_cells: list[Position] = field(default_factory=list)

    @property
    def f(self) -> float:
        return self.g + self.h


@dataclass(frozen=True)
class BoardFrame:
    board_text: str
    actor_pos: Position
    state: State
    title: str
    action: Optional[str]
    step_index: int
    g: float
    h: float
    f: float
    next_number: int
    kind: str


@dataclass
class SearchResult:
    found: bool
    algorithm: str
    heuristic_name: Optional[str]
    solution_actions: list[str] = field(default_factory=list)
    solution_string: str = ""
    total_cost: int = 0
    iterations: int = 0
    execution_time_ms: float = 0.0
    solution_nodes: list[Node] = field(default_factory=list)
    solution_frames: list[BoardFrame] = field(default_factory=list)
    iteration_frames: list[BoardFrame] = field(default_factory=list)
    expanded_states_count: int = 0
    error_message: Optional[str] = None
