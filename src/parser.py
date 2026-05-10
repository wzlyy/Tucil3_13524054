from __future__ import annotations

from pathlib import Path

from .models import Board, InputValidationError, Position

VALID_TILES = set("X*LZO0123456789")


def parse_positive_int(value: str, label: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise InputValidationError(f"{label} harus berupa integer.") from exc
    if parsed <= 0:
        raise InputValidationError(f"{label} harus bernilai positif.")
    return parsed


def parse_cost_row(line: str, expected_cols: int, row_number: int) -> tuple[int, ...]:
    parts = line.split()
    if len(parts) != expected_cols:
        raise InputValidationError(
            f"Baris cost ke-{row_number} harus berisi tepat {expected_cols} integer."
        )

    costs: list[int] = []
    for col_number, part in enumerate(parts, start=1):
        try:
            value = int(part)
        except ValueError as exc:
            raise InputValidationError(
                f"Cost pada baris {row_number}, kolom {col_number} harus integer."
            ) from exc
        if value < 0:
            raise InputValidationError(
                f"Cost pada baris {row_number}, kolom {col_number} tidak boleh negatif."
            )
        costs.append(value)
    return tuple(costs)


def parse_file(file_path: str | Path) -> Board:
    path = Path(file_path)
    if path.suffix.lower() != ".txt":
        raise InputValidationError("File input harus berekstensi .txt.")
    if not path.exists():
        raise InputValidationError(f"File tidak ditemukan: {path}")
    if not path.is_file():
        raise InputValidationError(f"Path bukan file: {path}")

    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise InputValidationError(f"Gagal membaca file: {exc}") from exc

    while raw_lines and raw_lines[-1].strip() == "":
        raw_lines.pop()

    if not raw_lines:
        raise InputValidationError("File kosong.")

    header = raw_lines[0].strip().split()
    if len(header) != 2:
        raise InputValidationError("Baris pertama harus berisi tepat dua integer: N M.")

    rows = parse_positive_int(header[0], "N")
    cols = parse_positive_int(header[1], "M")
    expected_line_count = 1 + rows + rows

    if len(raw_lines) < expected_line_count:
        raise InputValidationError(
            f"Jumlah baris tidak lengkap. Dibutuhkan {rows} baris board dan {rows} baris cost."
        )
    if len(raw_lines) > expected_line_count:
        raise InputValidationError("File memiliki baris tambahan setelah matrix cost.")

    board_lines = [line.strip() for line in raw_lines[1 : 1 + rows]]
    cost_lines = [line.strip() for line in raw_lines[1 + rows : expected_line_count]]

    start_positions: list[Position] = []
    goal_positions: list[Position] = []
    digit_positions: dict[int, list[Position]] = {}
    base_grid: list[str] = []

    for row_index, line in enumerate(board_lines):
        display_row = row_index + 1
        if len(line) != cols:
            raise InputValidationError(
                f"Baris board ke-{display_row} harus memiliki panjang tepat {cols} karakter."
            )

        chars = list(line)
        for col_index, char in enumerate(chars):
            if char not in VALID_TILES:
                raise InputValidationError(
                    f"Karakter '{char}' pada baris {display_row}, kolom {col_index + 1} tidak valid."
                )
            if char == "Z":
                start_positions.append((row_index, col_index))
                chars[col_index] = "*"
            elif char == "O":
                goal_positions.append((row_index, col_index))
            elif char.isdigit():
                digit_positions.setdefault(int(char), []).append((row_index, col_index))
        base_grid.append("".join(chars))

    if len(start_positions) != 1:
        raise InputValidationError("Board harus memiliki tepat satu posisi awal Z.")
    if len(goal_positions) != 1:
        raise InputValidationError("Board harus memiliki tepat satu titik tujuan O.")

    if digit_positions:
        max_digit = max(digit_positions)
        missing = [str(digit) for digit in range(max_digit + 1) if digit not in digit_positions]
        if missing:
            raise InputValidationError(
                "Angka pada board harus lengkap dari 0 sampai max digit. "
                f"Angka yang hilang: {', '.join(missing)}."
            )

    costs = tuple(parse_cost_row(line, cols, idx) for idx, line in enumerate(cost_lines, start=1))

    passable_costs: list[int] = []
    for row_index, row_text in enumerate(base_grid):
        for col_index, char in enumerate(row_text):
            if char not in {"X", "L"}:
                passable_costs.append(costs[row_index][col_index])

    min_passable_cost = min(passable_costs) if passable_costs else 0
    frozen_digit_positions = {
        digit: tuple(positions) for digit, positions in digit_positions.items()
    }

    return Board(
        rows=rows,
        cols=cols,
        base_grid=tuple(base_grid),
        costs=costs,
        start_pos=start_positions[0],
        goal_pos=goal_positions[0],
        digit_positions=frozen_digit_positions,
        source_path=str(path),
        min_passable_cost=min_passable_cost,
    )
