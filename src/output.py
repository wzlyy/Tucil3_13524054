from __future__ import annotations

from pathlib import Path

from .models import SearchResult


def format_number(value: float) -> str:
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.3f}"


def header_lines(result: SearchResult, input_path: str | None = None) -> list[str]:
    lines: list[str] = []
    if input_path:
        lines.append(f"Input File: {input_path}")
    lines.append(f"Algoritma: {result.algorithm}")
    if result.heuristic_name:
        lines.append(f"Heuristic: {result.heuristic_name}")
    else:
        lines.append("Heuristic: -")
    lines.append("")
    return lines


def format_solution(result: SearchResult, input_path: str | None = None) -> str:
    lines = header_lines(result, input_path)

    if not result.found:
        lines.extend(
            [
                "Status: Tidak ditemukan solusi.",
                f"Waktu Eksekusi: {format_number(result.execution_time_ms)} ms",
                f"Banyak Iterasi: {result.iterations}",
                "",
            ]
        )
        return "\n".join(lines)

    lines.extend(
        [
            "Status: Solusi ditemukan.",
            f"Solusi Yang Ditemukan: {result.solution_string}",
            f"Cost dari Solusi: {result.total_cost}",
            f"Waktu Eksekusi: {format_number(result.execution_time_ms)} ms",
            f"Banyak Iterasi: {result.iterations}",
            "",
        ]
    )

    for frame in result.solution_frames:
        lines.append(frame.title)
        lines.append(frame.board_text)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def save_solution(
    result: SearchResult,
    file_path: str | Path,
    input_path: str | None = None,
) -> None:
    path = Path(file_path)
    if path.parent != Path("."):
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(format_solution(result, input_path), encoding="utf-8")
