# Sliding Ice Puzzle Solver

## Penjelasan Singkat

Sliding Ice Puzzle Solver adalah program CLI berbasis Python untuk mencari solusi
puzzle sliding ice. Aktor `Z` bergerak horizontal atau vertikal dan terus
meluncur sampai berhenti tepat sebelum rintangan `X`.

Program mendukung algoritma UCS, GBFS, dan A*. Untuk GBFS dan A*, tersedia
heuristic H1, H2, dan H3. Solusi valid jika aktor berhenti di goal `O` dan semua
tile angka `0-9` yang ada pada papan dilewati sesuai urutan.

## Requirement dan Instalasi

Requirement:

- Python 3.10 atau lebih baru.

Instalasi:

```bash
git clone https://github.com/wzlyy/Tucil3_13524054.git
cd Tucil3_13524054
```

## Cara Menjalankan

Jalankan program dari root project:

```bash
python src/main.py
```

## Cara Menggunakan

Setelah program dijalankan, ikuti prompt di terminal:

```text
>> Masukan file input :
>> Algoritma apa yang anda pilih? (UCS/GBFS/A*)
>> Heuristic apa yang anda pilih? (H1/H2/H3)
```

Prompt heuristic hanya muncul jika algoritma yang dipilih adalah GBFS atau A*.

Contoh penggunaan:

```text
>> Masukan file input :
test/testcase1.txt

>> Algoritma apa yang anda pilih? (UCS/GBFS/A*)
A*

>> Heuristic apa yang anda pilih? (H1/H2/H3)
H2
```

Program akan menampilkan:

- solusi gerakan,
- cost solusi,
- visualisasi board initial dan setiap step,
- waktu eksekusi,
- banyak iterasi,
- opsi playback,
- opsi menyimpan solusi ke file `.txt`.

Command playback CLI:

```text
[n] next, [p] previous, [j] jump, [q] quit
```

## Format File Input

File input harus berekstensi `.txt` dengan format:

```text
N M
<N baris board>
<N baris matrix cost>
```

Simbol board:

- `*`: path yang bisa dilewati.
- `X`: rintangan/batu.
- `L`: lava.
- `Z`: posisi awal aktor.
- `O`: goal.
- `0` sampai `9`: tile angka yang harus dilewati berurutan.

## Tabel Pengerjaan
   <table border = "1">
    <tr>
        <th>No</th>
        <th>Poin</th>
        <th>Ya</th>
        <th>Tidak</th>
    </tr>
    <tr>
        <td>1</td>
        <td>Program berhasil di kompilasi tanpa kesalahan</td>
        <td>✓</td>
        <td></td>
    </tr>
    <tr>
        <td>2</td>
        <td>Program berhasil dijalankan</td>
        <td>✓</td>
        <td></td>
    </tr>
    <tr>
        <td>3</td>
        <td>Solusi yang diberikan program benar dan mematuhi aturan permainan</td>
        <td>✓</td>
        <td></td>
    </tr>
    <tr>
        <td>4</td>
        <td>Program dapat membaca masukan berkas .txt serta menyimpan solusi dalam berkas .txt</td>
        <td>✓</td>
        <td></td>
    </tr>
    <tr>
        <td>5</td>
        <td>Program memiliki Graphical User Interface (GUI)</td>
        <td></td>
        <td>✓</td>
    </tr>
    <tr>
        <td>6</td>
        <td>Ada algoritma pathfinding alternatif selain dari spesifikasi wajib (Algoritma X dan Algoritma Y)</td>
        <td></td>
        <td>✓</td>
    </tr>
    <tr>
        <td>7</td>
        <td>Ada tambahkan dua alternatif heuristik selain yang utama (Heuristik X dan Heuristik Y)</td>
        <td>✓</td>
        <td></td>
    </tr>
</table>




Wildan Abdurrahman Ghazali

NIM 13524054
