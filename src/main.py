import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    __package__ = "src"

from .models import BoardFrame, InputValidationError, SearchResult
from .output import save_solution
from .parser import parse_file
from .search import solve

HEURISTIC_CHOICES = ("H1", "H2", "H3")


def format_number(value: float) -> str:
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.3f}"


def read_line(prompt: str) -> str:
    print(prompt)
    return input().strip().strip('"')


def normalize_algorithm(raw: str) -> str | None:
    normalized = raw.strip().upper()
    if normalized in {"UCS", "GBFS", "A*"}:
        return normalized
    return None


def prompt_algorithm() -> str:
    while True:
        raw = read_line(">> Algoritma apa yang anda pilih? (UCS/GBFS/A*)")
        algorithm = normalize_algorithm(raw)
        if algorithm is not None:
            return algorithm
        print("Pilihan algoritma tidak valid. Pilihan: UCS, GBFS, A*.")


def prompt_heuristic() -> str:
    while True:
        raw = read_line(">> Heuristic apa yang anda pilih? (H1/H2/H3)")
        heuristic = raw.strip().upper()
        if heuristic in HEURISTIC_CHOICES:
            return heuristic
        print("Pilihan heuristic tidak valid. Pilihan: H1, H2, H3.")


def prompt_yes_no(prompt: str) -> bool:
    while True:
        answer = read_line(prompt).lower()
        if answer == "ya":
            return True
        if answer in "tidak":
            return False
        print("Jawaban tidak valid. Masukkan Ya atau Tidak.")


def print_frame(frame: BoardFrame) -> None:
    print(frame.title)
    print(frame.board_text)


def print_result(result: SearchResult) -> None:
    print()
    if result.found:
        print(f"Solusi Yang Ditemukan : {result.solution_string}")
        print(f"Cost dari Solusi : {result.total_cost}")
        print()
        for frame in result.solution_frames:
            print_frame(frame)
            print()
    else:
        print("Solusi tidak ditemukan.")
        if result.error_message:
            print(result.error_message)
        print()

    print(f">> Waktu eksekusi: {format_number(result.execution_time_ms)} ms")
    print(f">> Banyak iterasi yang dilakukan: {result.iterations} iterasi")
    print()


def read_step(max_step: int, prompt: str) -> int:
    while True:
        raw = read_line(prompt)
        try:
            step = int(raw)
        except ValueError:
            print("Step harus berupa integer.")
            continue
        if 0 <= step <= max_step:
            return step
        print(f"Step harus berada pada rentang 0 sampai {max_step}.")


def show_playback_step(frames: list[BoardFrame], current_step: int) -> None:
    max_step = len(frames) - 1
    print()
    print(f"Playback Step {current_step} / {max_step}")
    print_frame(frames[current_step])
    print()


def run_playback(frames: list[BoardFrame]) -> None:
    if not frames:
        print("Playback solusi tidak tersedia karena solusi tidak ditemukan.")
        return

    max_step = len(frames) - 1
    current_step = read_step(max_step, ">> Pada step berapa anda ingin melakukan playback :")
    show_playback_step(frames, current_step)

    while True:
        print("Playback command:")
        print("[n] next, [p] previous, [j] jump, [q] quit")
        command = read_line(">>").lower()

        if command == "q":
            print("Playback selesai.")
            return
        if command == "n":
            if current_step < max_step:
                current_step += 1
            else:
                print("Sudah berada di step terakhir.")
            show_playback_step(frames, current_step)
            continue
        if command == "p":
            if current_step > 0:
                current_step -= 1
            else:
                print("Sudah berada di step awal.")
            show_playback_step(frames, current_step)
            continue
        if command == "j":
            current_step = read_step(max_step, ">> Masukan step tujuan :")
            show_playback_step(frames, current_step)
            continue

        print("Command tidak valid. Gunakan n, p, j, atau q.")


def normalize_output_path(raw_path: str, default_path: Path) -> Path:
    path = default_path if not raw_path else Path(raw_path.strip().strip('"'))
    if path.suffix == "":
        path = path.with_suffix(".txt")
    if path.suffix.lower() != ".txt":
        raise ValueError("File output harus berekstensi .txt.")
    return path


def save_result(result: SearchResult, input_path: str) -> bool:
    if not prompt_yes_no(">> Apakah Anda ingin menyimpan solusi? (Ya/Tidak) :"):
        return True

    default_path = Path("test") / "solution.txt"
    while True:
        raw_path = read_line(
            ">> Masukan path file output (.txt), kosongkan untuk default test/solution.txt :"
        )
        try:
            output_path = normalize_output_path(raw_path, default_path)
            save_solution(result, output_path, input_path=input_path)
        except (OSError, ValueError) as exc:
            print(f"Gagal menyimpan solusi: {exc}")
            retry = prompt_yes_no(">> Coba path lain? (Ya/Tidak) :")
            if not retry:
                return False
            continue

        print(f">> Solusi disimpan pada {output_path.resolve()}")
        return True


def run_cli() -> int:
    try:
        file_path = read_line(">> Masukan file input :")
        board = parse_file(file_path)

        algorithm = prompt_algorithm()
        heuristic = None
        if algorithm in {"GBFS", "A*"}:
            heuristic = prompt_heuristic()

        result = solve(
            board,
            algorithm=algorithm,
            heuristic_name=heuristic,
            collect_iteration_frames=False,
        )

        print_result(result)

        if prompt_yes_no(">> Apakah Anda ingin melakukan playback? (Ya/Tidak) :"):
            run_playback(result.solution_frames)

        if not save_result(result, board.source_path or file_path):
            return 1
        return 0

    except (InputValidationError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1
    except KeyboardInterrupt:
        print("\nProgram dihentikan")
        return 1

if __name__ == "__main__":
    raise SystemExit(run_cli())
