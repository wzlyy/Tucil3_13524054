from __future__ import annotations

import heapq
import itertools
import time

from .board import DIRECTION_ORDER, is_goal, make_frame, simulate_move, start_state
from .heuristic import get_heuristic
from .models import Board, BoardFrame, Node, SearchResult

SUPPORTED_ALGORITHMS = ("UCS", "GBFS", "A*")
EPSILON = 1e-9



def priority(algorithm: str, node: Node) -> float:
    if algorithm == "UCS":
        return node.g
    if algorithm == "GBFS":
        return node.h
    return node.f


def reconstruct_nodes(goal_node: Node) -> list[Node]:
    nodes: list[Node] = []
    current: Node | None = goal_node
    while current is not None:
        nodes.append(current)
        current = current.parent
    nodes.reverse()
    return nodes


def build_solution_frames(board: Board, nodes: list[Node]) -> list[BoardFrame]:
    frames: list[BoardFrame] = []
    for index, node in enumerate(nodes):
        if index == 0:
            title = "Initial"
            action = None
        else:
            action = node.action
            title = f"Step {index} : {action}"
        frames.append(
            make_frame(
                board=board,
                node=node,
                title=title,
                step_index=index,
                kind="solution",
                action=action,
            )
        )
    return frames


def solve(
    board: Board,
    algorithm: str = "UCS",
    heuristic_name: str | None = "H1",
    collect_iteration_frames: bool = True,
) -> SearchResult:

    active_heuristic_name = None if algorithm == "UCS" else (heuristic_name or "H1")
    heuristic = None if algorithm == "UCS" else get_heuristic(active_heuristic_name)

    start = start_state(board)
    start_h = 0.0 if heuristic is None else float(heuristic(board, start))
    root = Node(state=start, g=0.0, h=start_h)

    counter = itertools.count()
    frontier: list[tuple[float, int, Node]] = []
    heapq.heappush(frontier, (priority(algorithm, root), next(counter), root))
    best_cost: dict[tuple[int, int, int], float] = {start: 0.0}
    iterations = 0
    iteration_frames: list[BoardFrame] = []
    goal_node: Node | None = None

    start_time = time.perf_counter()

    while frontier:
        _, _, node = heapq.heappop(frontier)
        if node.g > best_cost.get(node.state, float("inf")) + EPSILON:
            continue

        iterations += 1
        if collect_iteration_frames:
            iteration_frames.append(
                make_frame(
                    board=board,
                    node=node,
                    title=f"Iteration {iterations}",
                    step_index=iterations,
                    kind="iteration",
                    action=node.action,
                )
            )

        if is_goal(board, node.state):
            goal_node = node
            break

        for direction in DIRECTION_ORDER:
            move = simulate_move(board, node.state, direction)
            if move is None:
                continue

            new_g = node.g + move.move_cost
            if new_g + EPSILON >= best_cost.get(move.new_state, float("inf")):
                continue

            new_h = 0.0 if heuristic is None else float(heuristic(board, move.new_state))
            child = Node(
                state=move.new_state,
                g=new_g,
                h=new_h,
                action=direction,
                parent=node,
                move_cells=move.traversed_cells,
            )
            best_cost[move.new_state] = new_g
            heapq.heappush(frontier, (priority(algorithm, child), next(counter), child))

    execution_time_ms = (time.perf_counter() - start_time) * 1000

    if goal_node is None:
        return SearchResult(
            found=False,
            algorithm=algorithm,
            heuristic_name=active_heuristic_name,
            iterations=iterations,
            execution_time_ms=execution_time_ms,
            iteration_frames=iteration_frames,
            expanded_states_count=iterations,
            error_message="Tidak ditemukan solusi.",
        )

    solution_nodes = reconstruct_nodes(goal_node)
    solution_actions = [node.action for node in solution_nodes[1:] if node.action is not None]
    return SearchResult(
        found=True,
        algorithm=algorithm,
        heuristic_name=active_heuristic_name,
        solution_actions=solution_actions,
        solution_string="".join(solution_actions),
        total_cost=int(goal_node.g),
        iterations=iterations,
        execution_time_ms=execution_time_ms,
        solution_nodes=solution_nodes,
        solution_frames=build_solution_frames(board, solution_nodes),
        iteration_frames=iteration_frames,
        expanded_states_count=iterations,
    )
