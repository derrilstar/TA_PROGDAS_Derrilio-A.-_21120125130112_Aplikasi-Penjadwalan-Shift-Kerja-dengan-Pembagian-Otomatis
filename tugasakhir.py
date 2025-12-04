import tkinter as tk                   # Modul 5 (GUI): import tkinter dasar sebagai alias tk
from tkinter import ttk, messagebox    # Modul 5 (GUI): ttk untuk Treeview, messagebox untuk popup
import customtkinter as ctk            # Modul 5 (GUI): customtkinter sebagai GUI modern
import random, math                    # Modul 1 (Variabel & tipe data) + logika umum: random & operasi matematika

# =========================
#  MODEL KARYAWAN
# =========================
class Karyawan:                        # Modul 6 (OOP 1 - Class & Constructor): definisi class Karyawan
    def __init__(self, nama: str):     # Modul 6 (OOP 1 - Constructor): method konstruktor dengan parameter nama
        self.__nama = nama             # Modul 1 (Variabel) + Modul 7 (Encapsulation): atribut privat __nama

    def get_nama(self):                # Modul 4 (Function & Method) + Modul 7 (Getter): method untuk ambil nama
        return self.__nama             # Mengembalikan nilai atribut __nama


# =========================
#  SCHEDULER (ROTASI SHIFT)
# =========================
class ShiftScheduler:                                                      # Modul 6 (OOP 1): class untuk logika penjadwalan
    def __init__(self, daftar_karyawan, jumlah_shift=4, kapasitas_per_shift=1, mode="normal"):
        base_shifts = ["Pagi", "Siang", "Sore", "Malam"]                  # Modul 1 (Array/List): list nama-nama shift

        jumlah_shift = max(1, min(jumlah_shift, len(base_shifts)))       # Modul 2 (Pengkondisian tak langsung) + 1: batasi jumlah shift antara 1–4
        kapasitas_per_shift = max(1, int(kapasitas_per_shift))           # Modul 1 (tipe data & casting int): kapasitas minimal 1

        self.daftar_karyawan = daftar_karyawan                           # Simpan list objek Karyawan (Modul 1 & 6)
        self.mode = mode                                                 # Mode penjadwalan: "normal" atau "random"
        self.shifts = base_shifts[:jumlah_shift]                         # Modul 1 (List slicing): ambil sejumlah shift yang dipakai
        self.kapasitas = kapasitas_per_shift                             # Kapasitas tiap shift
        self.jadwal = []                                                 # List kosong untuk menampung hasil jadwal

    def generate(self, jumlah_hari: int):                                 # Modul 4 (Function & Method): method generate jadwal
        self.jadwal = []                                                 # Reset list jadwal setiap kali generate dipanggil
        jumlah_hari = max(1, jumlah_hari)                                # Pastikan minimal 1 hari (Modul 2: logika)

        daftar = self.daftar_karyawan.copy()                             # Copy list karyawan supaya aslinya tidak berubah
        if not daftar:                                                   # Modul 2 (IF): jika tidak ada karyawan
            return []                                                    # Kembalikan list kosong (tidak ada jadwal)

        if self.mode == "random":                                        # Modul 2 (IF): jika mode random dipilih
            random.shuffle(daftar)                                       # Modul random: acak urutan karyawan

        idx = 0  # pointer global (muter terus)                          # Modul 1: variabel index untuk rotasi karyawan
        for hari in range(1, jumlah_hari + 1):                           # Modul 3 (Perulangan for): loop untuk tiap hari
            for shift_name in self.shifts:                               # Modul 3: loop untuk tiap shift dalam 1 hari
                for slot_ke in range(1, self.kapasitas + 1):             # Modul 3: loop untuk setiap slot dalam shift
                    karyawan = daftar[idx]                               # Ambil karyawan berdasarkan index saat ini
                    self.jadwal.append({                                 # Tambahkan satu record jadwal ke list (Modul 1: dictionary/list)
                        "hari": hari,                                    # Simpan info hari
                        "shift": shift_name,                             # Simpan nama shift
                        "slot": slot_ke,                                 # Simpan nomor petugas di shift
                        "nama": karyawan.get_nama()                      # Panggil method get_nama() (Modul 4 & 6)
                    })
                    idx = (idx + 1) % len(daftar)                        # Modul 3 + aritmatika: index berputar (rotasi karyawan)

        return self.jadwal                                               # Kembalikan list jadwal yang sudah dibuat


# =========================
#  APLIKASI GUI
# =========================
class ShiftApp(ctk.CTk):                                                 # Modul 6 (OOP 1) + Modul 5 (GUI): class turunan CTk (CustomTkinter)
    def __init__(self):
        super().__init__()                                               # Panggil constructor parent (CTk)

        ctk.set_appearance_mode("dark")                                  # Modul 5 (GUI): set tema dark
        ctk.set_default_color_theme("blue")                              # Modul 5 (GUI): set tema warna biru
        ctk.set_widget_scaling(1.05)                                     # Modul 5 (GUI): scaling widget 105%

        self.title("Aplikasi Penjadwalan Shift Kerja")                   # Set judul window
        self.geometry("1200x700")                                        # Set ukuran awal window
        self.minsize(1000, 580)                                          # Set ukuran minimal window

        self.bind("<F11>", self._toggle_fullscreen)                      # Modul 5: binding event F11 untuk toggle fullscreen
        self.bind("<Escape>", self._exit_fullscreen)                     # Modul 5: binding ESC untuk keluar fullscreen

        self.grid_rowconfigure(1, weight=1)                              # Atur grid: baris 1 bisa melar (panel utama)
        self.grid_columnconfigure(0, weight=1)                           # Kolom kiri bobot 1
        self.grid_columnconfigure(1, weight=2)                           # Kolom kanan bobot 2 (lebih besar)

        self._build_header()                                             # Panggil method untuk membuat header (Modul 4 & 5)
        self._build_left_panel()                                         # Panggil method untuk panel kiri
        self._build_right_panel()                                        # Panggil method untuk panel kanan
        self._build_statusbar()                                          # Panggil method untuk status bar

    # ========== HEADER ==========
    def _build_header(self):                                             # Method private untuk membangun header
        header = ctk.CTkFrame(self, fg_color="#020617")                # Modul 5: frame header dengan warna gelap
        header.grid(row=0, column=0, columnspan=2, sticky="nsew")        # Tempatkan di baris 0, melebar ke 2 kolom
        header.grid_columnconfigure(0, weight=1)                         # Kolom 0 di header bisa melar

        ctk.CTkLabel(
            header,
            text="Aplikasi Penjadwalan Shift Kerja",                     # Teks judul utama
            font=("Segoe UI", 26, "bold")
        ).grid(row=0, column=0, sticky="w", padx=22, pady=(14, 4))       # Tempatkan judul di kiri header

        ctk.CTkLabel(
            header,
            text="Masukkan karyawan, atur jumlah shift, kapasitas per shift, dan jumlah hari. Jadwal akan dibagi otomatis dan berulang dengan sistem rotasi.",
            font=("Segoe UI", 13),
            text_color="#9ca3af",
            wraplength=900,
            justify="left"
        ).grid(row=1, column=0, sticky="w", padx=22, pady=(0, 10))       # Label deskripsi singkat di bawah judul

    # ========== LEFT PANEL ==========
    def _build_left_panel(self):                                         # Method untuk membangun panel kiri (input)
        outer = ctk.CTkFrame(self, fg_color="#020617")                   # Frame pembungkus panel kiri
        outer.grid(row=1, column=0, sticky="nsew", padx=(18, 9), pady=(10, 8))
        outer.grid_rowconfigure(0, weight=1)                             # Baris 0 (isi) bisa melar
        outer.grid_rowconfigure(1, weight=0)                             # Baris 1 (tombol bawah) tinggi tetap
        outer.grid_columnconfigure(0, weight=1)                          # Satu kolom yang melar penuh

        self.left = ctk.CTkScrollableFrame(                              # Modul 5: frame scrollable untuk isi panel kiri
            outer,
            corner_radius=16,
            fg_color="#020617",
            border_width=1,
            border_color="#1f2937"
        )
        self.left.grid(row=0, column=0, sticky="nsew", padx=4, pady=(4, 0))
        self.left.grid_columnconfigure(0, weight=1)                      # Dua kolom di dalam scrollable frame
        self.left.grid_columnconfigure(1, weight=1)

        self._build_left_content()                                       # Isi panel kiri (input + tabel karyawan)

        action_bar = ctk.CTkFrame(outer, fg_color="#020617")             # Frame untuk tombol bawah (Generate & Clear)
        action_bar.grid(row=1, column=0, sticky="ew", padx=4, pady=(6, 4))
        action_bar.grid_columnconfigure(0, weight=1)                     # Kolom tombol kiri melar
        action_bar.grid_columnconfigure(1, weight=1)                     # Kolom tombol kanan melar

        ctk.CTkButton(
            action_bar, text="Generate Shift", command=self._generate,   # Tombol untuk menghasilkan jadwal
            height=40, font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, sticky="ew", padx=(6, 4), pady=2)

        ctk.CTkButton(
            action_bar, text="Clear Semua", command=self._clear_all,     # Tombol untuk mengosongkan semua data
            height=40, fg_color="#4b5563", font=("Segoe UI", 13)
        ).grid(row=0, column=1, sticky="ew", padx=(4, 6), pady=2)

    def _build_left_content(self):                                       # Method untuk membuat isi panel kiri
        # --- Section: Karyawan ---
        ctk.CTkLabel(self.left, text="Karyawan", font=("Segoe UI", 15, "bold"))\
            .grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(14, 4))   # Judul section Karyawan

        ctk.CTkLabel(
            self.left,
            text="Masukkan nama karyawan, tekan Enter atau klik Tambah.",             # Instruksi singkat
            font=("Segoe UI", 11),
            text_color="#9ca3af"
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 8))

        ctk.CTkLabel(self.left, text="Nama karyawan:", font=("Segoe UI", 13))\
            .grid(row=2, column=0, sticky="w", padx=16, pady=(4, 0))                  # Label untuk input nama
        self.entry_nama = ctk.CTkEntry(
            self.left,
            placeholder_text="Contoh: Raihan",                                        # Placeholder contoh nama
            height=34,
            font=("Segoe UI", 13)
        )
        self.entry_nama.grid(row=3, column=0, sticky="ew", padx=16, pady=(4, 4))      # Entry nama karyawan
        self.entry_nama.bind("<Return>", lambda e: self._tambah_karyawan())           # Enter = panggil _tambah_karyawan
        self.entry_nama.focus()                                                       # Fokus awal di input nama

        ctk.CTkButton(
            self.left, text="Tambah",
            command=self._tambah_karyawan,                                            # Tombol tambah karyawan
            height=32, font=("Segoe UI", 12, "bold")
        ).grid(row=3, column=1, sticky="w", padx=(0, 16), pady=(4, 4))

        ctk.CTkButton(
            self.left, text="Hapus Terpilih",
            fg_color="#b91c1c",                                                       # Warna merah gelap
            command=self._hapus_terpilih,                                             # Hapus baris yang diseleksi
            height=32, font=("Segoe UI", 11)
        ).grid(row=4, column=0, sticky="w", padx=16, pady=(2, 4))

        ctk.CTkButton(
            self.left, text="Hapus Semua",
            fg_color="#ef4444",                                                       # Warna merah terang
            command=self._hapus_semua,                                                # Hapus semua karyawan
            height=30, font=("Segoe UI", 11)
        ).grid(row=4, column=1, sticky="w", padx=(0, 16), pady=(2, 4))

        # Tabel karyawan
        ctk.CTkLabel(self.left, text="Daftar karyawan:", font=("Segoe UI", 13))\
            .grid(row=5, column=0, columnspan=2, sticky="w", padx=16, pady=(8, 4))    # Label di atas tabel karyawan

        table_frame = ctk.CTkFrame(self.left, fg_color="#020617")                     # Frame pembungkus Treeview karyawan
        table_frame.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=16)
        self.left.grid_rowconfigure(6, weight=1)                                      # Baris tabel bisa melar

        self.tree_karyawan = ttk.Treeview(                                            # Modul 5 + ttk: tabel daftar karyawan
            table_frame,
            columns=("nama",),
            show="headings",
            height=6
        )
        self.tree_karyawan.heading("nama", text="Nama")                               # Header kolom Nama
        self.tree_karyawan.column("nama", width=220, anchor="w")                      # Kolom Nama rata kiri

        style = ttk.Style()                                                           # Objek Style ttk untuk mengatur tampilan
        style.theme_use("clam")                                                       # Gunakan tema 'clam'
        style.configure(
            "Treeview",
            background="#020617",
            fieldbackground="#020617",
            foreground="#e5e7eb",
            rowheight=30,               # Tinggi baris diperbesar
            font=("Segoe UI", 13),      # Font isi tabel diperbesar
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#111827",
            foreground="#e5e7eb",
            font=("Segoe UI", 13, "bold")  # Font header tabel lebih besar & bold
        )

        self.tree_karyawan.pack(side="left", fill="both", expand=True)                # Tampilkan Treeview di kiri frame
        scroll_k = ctk.CTkScrollbar(table_frame, command=self.tree_karyawan.yview)    # Scrollbar vertikal untuk tabel karyawan
        scroll_k.pack(side="right", fill="y")                                         # Tempatkan scrollbar di kanan
        self.tree_karyawan.configure(yscrollcommand=scroll_k.set)                     # Sinkronkan scrollbar dengan Treeview

        # --- Section: Pengaturan Jadwal ---
        ctk.CTkLabel(self.left, text="Pengaturan Jadwal", font=("Segoe UI", 15, "bold"))\
            .grid(row=7, column=0, columnspan=2, sticky="w", padx=16, pady=(14, 4))   # Judul section pengaturan jadwal

        ctk.CTkLabel(self.left, text="Jumlah shift (1–4):", font=("Segoe UI", 13))\
            .grid(row=8, column=0, sticky="w", padx=16, pady=(4, 0))                  # Label jumlah shift
        self.shift_var = ctk.StringVar(value="4")                                     # Modul 1: variabel String utk jumlah shift
        ctk.CTkOptionMenu(
            self.left, values=["1", "2", "3", "4"],
            variable=self.shift_var, width=90, font=("Segoe UI", 12)
        ).grid(row=8, column=1, sticky="w", padx=(0, 16), pady=(4, 0))                # Dropdown pilihan jumlah shift

        ctk.CTkLabel(self.left, text="Kapasitas per shift:", font=("Segoe UI", 13))\
            .grid(row=9, column=0, sticky="w", padx=16, pady=(8, 0))                  # Label kapasitas per shift
        self.cap_var = ctk.StringVar(value="1")                                       # Variabel String untuk kapasitas
        ctk.CTkOptionMenu(
            self.left, values=["1", "2", "3", "4", "5"],
            variable=self.cap_var, width=90, font=("Segoe UI", 12)
        ).grid(row=9, column=1, sticky="w", padx=(0, 16), pady=(8, 0))                # Dropdown kapasitas per shift

        ctk.CTkLabel(self.left, text="Jumlah hari:", font=("Segoe UI", 13))\
            .grid(row=10, column=0, sticky="w", padx=16, pady=(8, 0))                 # Label jumlah hari
        self.entry_hari = ctk.CTkEntry(
            self.left,
            placeholder_text="Contoh: 1 atau 7",                                      # Placeholder input hari
            width=110,
            height=32,
            font=("Segoe UI", 12)
        )
        self.entry_hari.grid(row=10, column=1, sticky="w", padx=(0, 16), pady=(8, 0)) # Entry untuk jumlah hari
        self.entry_hari.bind("<Return>", lambda e: self._generate())                  # Enter = generate jadwal

        self.autodays_var = ctk.BooleanVar(value=True)                                # Variabel boolean untuk Auto hari
        ctk.CTkCheckBox(
            self.left,
            text="Auto hari (semua karyawan minimal 1x kebagian)",                   # Jika aktif, hitung hari minimal otomatis
            variable=self.autodays_var,
            font=("Segoe UI", 11)
        ).grid(row=11, column=0, columnspan=2, sticky="w", padx=16, pady=(6, 0))

        ctk.CTkLabel(self.left, text="Mode pembagian:", font=("Segoe UI", 13))\
            .grid(row=12, column=0, sticky="w", padx=16, pady=(8, 0))                # Label mode pembagian
        self.mode_var = ctk.StringVar(value="normal")                                # Variabel String untuk mode ("normal"/"random")
        ctk.CTkOptionMenu(
            self.left,
            values=["normal", "random"],
            variable=self.mode_var,
            width=120,
            font=("Segoe UI", 12)
        ).grid(row=12, column=1, sticky="w", padx=(0, 16), pady=(8, 0))              # Dropdown mode pembagian

    # ========== RIGHT PANEL (SUMMARY CARDS + TABLE) ==========
    def _build_right_panel(self):                                                    # Method untuk membangun panel kanan
        right_outer = ctk.CTkFrame(self, fg_color="#020617")                         # Frame pembungkus kanan
        right_outer.grid(row=1, column=1, sticky="nsew", padx=(9, 18), pady=(10, 8))
        right_outer.grid_rowconfigure(0, weight=0)                                   # Baris 0: summary cards
        right_outer.grid_rowconfigure(1, weight=1)                                   # Baris 1: tabel hasil (melar)
        right_outer.grid_columnconfigure(0, weight=1)

        # summary cards row
        summary_frame = ctk.CTkFrame(right_outer, fg_color="#020617")                # Frame untuk 3 kartu ringkasan
        summary_frame.grid(row=0, column=0, sticky="ew", padx=4, pady=(4, 2))
        summary_frame.grid_columnconfigure((0, 1, 2), weight=1)                      # 3 kolom kartu sama lebar

        self.card_total_karyawan = self._create_summary_card(summary_frame, "Total Karyawan", "-", 0)  # Kartu total karyawan
        self.card_total_hari = self._create_summary_card(summary_frame, "Total Hari", "-", 1)          # Kartu total hari
        self.card_total_slot = self._create_summary_card(summary_frame, "Total Slot / Jadwal", "-", 2) # Kartu total slot/jadwal

        # frame untuk tabel hasil
        main = ctk.CTkFrame(
            right_outer,
            corner_radius=16,
            fg_color="#020617",
            border_width=1,
            border_color="#1f2937"
        )
        main.grid(row=1, column=0, sticky="nsew", padx=4, pady=(2, 4))               # Frame utama tabel hasil
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            main,
            text="Hasil Penjadwalan",                                                # Judul bagian hasil
            font=("Segoe UI", 17, "bold")
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(14, 6))

        table_frame = ctk.CTkFrame(main, fg_color="#020617")                         # Frame pembungkus tabel hasil
        table_frame.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 14))

        columns = ("hari", "shift", "slot", "nama")                                  # Nama kolom tabel hasil
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

        self.tree.heading("hari", text="Hari")                                       # Header kolom Hari
        self.tree.heading("shift", text="Shift")                                     # Header kolom Shift
        self.tree.heading("slot", text="Petugas#")                                   # Header kolom Petugas#
        self.tree.heading("nama", text="Nama Karyawan")                              # Header kolom Nama Karyawan

        self.tree.column("hari", width=60, anchor="center")                          # Kolom Hari, rata tengah
        self.tree.column("shift", width=120, anchor="center")                        # Kolom Shift
        self.tree.column("slot", width=80, anchor="center")                          # Kolom Petugas#
        self.tree.column("nama", width=260, anchor="w")                              # Kolom Nama, rata kiri

        style = ttk.Style()                                                          # Style ttk (dipakai lagi di sini)
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#020617",
            fieldbackground="#020617",
            foreground="#e5e7eb",
            rowheight=30,               # Tinggi baris tabel hasil
            font=("Segoe UI", 13),      # Font isi tabel hasil
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#111827",
            foreground="#e5e7eb",
            font=("Segoe UI", 13, "bold")  # Font header tabel hasil
        )

        self.tree.pack(side="left", fill="both", expand=True)                        # Tampilkan Treeview hasil
        scroll_y = ctk.CTkScrollbar(table_frame, command=self.tree.yview)            # Scrollbar vertikal tabel hasil
        scroll_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll_y.set)                             # Sinkron scrollbar & Treeview

    def _create_summary_card(self, parent, title, value, column):                    # Method bantu untuk membuat 1 kartu summary
        frame = ctk.CTkFrame(
            parent,
            fg_color="#020617",
            corner_radius=18,
            border_width=1,
            border_color="#1f2937"
        )
        frame.grid(row=0, column=column, sticky="ew", padx=6, pady=4)                # Tempatkan kartu pada kolom tertentu
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text=title,                                                               # Judul kecil kartu (misal "Total Karyawan")
            font=("Segoe UI", 11),
            text_color="#9ca3af"
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(8, 0))

        label_value = ctk.CTkLabel(
            frame,
            text=value,                                                               # Nilai angka pada kartu
            font=("Segoe UI", 22, "bold")
        )
        label_value.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 10))

        return label_value                                                            # Kembalikan label agar bisa di-update

    # ========== STATUS BAR ==========
    def _build_statusbar(self):                                                      # Method untuk membuat status bar bawah
        self.status = ctk.CTkLabel(
            self,
            text="Siap digunakan.",                                                  # Pesan status awal
            anchor="w",
            font=("Segoe UI", 11)
        )
        self.status.grid(row=2, column=0, columnspan=2, sticky="ew", padx=18, pady=(0, 8))

    # ========== EVENT HANDLER ==========
    def _tambah_karyawan(self):                                                      # Handler tombol/Enter untuk tambah karyawan
        nama = self.entry_nama.get().strip()                                         # Ambil teks dari entry, hilangkan spasi pinggir
        if not nama:                                                                 # Modul 2 (IF): jika nama kosong
            messagebox.showwarning("Peringatan", "Nama karyawan tidak boleh kosong!")# Tampilkan peringatan
            return

        self.tree_karyawan.insert("", tk.END, values=(nama,))                        # Tambah baris baru ke tabel karyawan
        self.entry_nama.delete(0, tk.END)                                            # Kosongkan entry
        self.entry_nama.focus()                                                      # Fokus lagi ke entry nama

        total = len(self.tree_karyawan.get_children())                               # Hitung ulang jumlah karyawan
        self.status.configure(text=f"'{nama}' ditambahkan. Total {total} karyawan.") # Update status bar

    def _hapus_terpilih(self):                                                       # Handler untuk menghapus baris yang dipilih
        selected = self.tree_karyawan.selection()                                    # Ambil daftar item terpilih
        if not selected:                                                             # Jika tidak ada yang dipilih
            messagebox.showinfo("Info", "Pilih karyawan yang ingin dihapus.")        # Informasikan ke pengguna
            return
        for item_id in selected:                                                     # Modul 3 (for): loop tiap item terpilih
            self.tree_karyawan.delete(item_id)                                       # Hapus baris tersebut

        total = len(self.tree_karyawan.get_children())                               # Hitung ulang jumlah karyawan
        self.status.configure(text=f"Data karyawan diperbarui. Sisa {total} orang.") # Update status bar

    def _hapus_semua(self):                                                          # Handler untuk hapus semua karyawan
        if not self.tree_karyawan.get_children():                                    # Jika tabel sudah kosong
            return
        if messagebox.askyesno("Konfirmasi", "Hapus semua karyawan?"):               # Tampilkan dialog konfirmasi
            for item_id in self.tree_karyawan.get_children():                        # Loop semua baris karyawan
                self.tree_karyawan.delete(item_id)                                   # Hapus baris
            self.status.configure(text="Daftar karyawan dikosongkan.")               # Update status text
            self.card_total_karyawan.configure(text="-")                             # Reset kartu ringkasan kanan
            self.card_total_hari.configure(text="-")
            self.card_total_slot.configure(text="-")

    def _generate(self):                                                             # Handler tombol Generate Shift
        rows = self.tree_karyawan.get_children()                                     # Ambil semua baris karyawan
        if not rows:                                                                 # Jika belum ada karyawan
            messagebox.showwarning("Peringatan", "Tambahkan minimal satu karyawan terlebih dahulu.")
            return

        daftar_obj = []                                                              # List untuk objek Karyawan
        for item_id in rows:                                                         # Loop setiap baris di tabel karyawan
            (nama,) = self.tree_karyawan.item(item_id)["values"]                     # Ambil nilai nama dari baris
            daftar_obj.append(Karyawan(nama))                                        # Buat objek Karyawan dan tambahkan ke list

        try:
            jshift = int(self.shift_var.get())                                       # Ambil jumlah shift dan ubah ke int
        except ValueError:
            jshift = 4                                                               # Jika gagal, pakai default 4

        try:
            kapasitas = int(self.cap_var.get())                                      # Ambil kapasitas per shift
        except ValueError:
            kapasitas = 1                                                            # Default 1 jika input tidak valid

        hari_txt = self.entry_hari.get().strip()                                     # Ambil teks jumlah hari
        jhari_input = None
        if hari_txt:                                                                 # Jika user mengisi jumlah hari
            try:
                jhari_input = int(hari_txt)                                          # Coba ubah ke integer
            except ValueError:
                messagebox.showwarning("Peringatan", "Jumlah hari harus berupa angka.")
                return

        slots_per_day = jshift * kapasitas                                           # Slot per hari = jumlah shift x kapasitas
        minimal_days = max(1, math.ceil(len(daftar_obj) / slots_per_day))            # Hitung minimal hari agar semua kebagian

        if self.autodays_var.get():                                                  # Jika checkbox Auto hari aktif
            jhari = max(jhari_input or 0, minimal_days)                              # Pakai max antara input & minimal_days
        else:
            jhari = jhari_input if jhari_input and jhari_input > 0 else 1            # Kalau tidak auto, pakai input atau 1

        mode = self.mode_var.get()                                                   # Ambil mode pembagian ("normal"/"random")

        scheduler = ShiftScheduler(daftar_obj, jshift, kapasitas, mode)              # Buat objek ShiftScheduler dengan parameter
        hasil = scheduler.generate(jhari)                                            # Panggil generate untuk membuat jadwal

        for item in self.tree.get_children():                                        # Hapus semua jadwal lama di tabel hasil
            self.tree.delete(item)

        for row in hasil:                                                            # Isi tabel hasil dengan jadwal baru
            self.tree.insert(
                "",
                tk.END,
                values=(row["hari"], row["shift"], row["slot"], row["nama"])
            )

        total_slots = len(hasil)                                                     # Hitung total slot/jadwal yang dibuat

        # update cards
        self.card_total_karyawan.configure(text=str(len(daftar_obj)))                # Update kartu Total Karyawan
        self.card_total_hari.configure(text=str(jhari))                              # Update kartu Total Hari
        self.card_total_slot.configure(text=str(total_slots))                        # Update kartu Total Slot/Jadwal

        self.status.configure(
            text=f"Jadwal: {jhari} hari • {len(daftar_obj)} karyawan • {len(scheduler.shifts)} shift • kapasitas {kapasitas}/shift • total slot {total_slots} • mode: {mode}"
        )                                                                            # Tampilkan ringkasan di status bar

    def _clear_all(self):                                                           # Handler tombol Clear Semua
        self.entry_nama.delete(0, tk.END)                                           # Kosongkan input nama
        self.entry_hari.delete(0, tk.END)                                           # Kosongkan input hari

        for item_id in self.tree_karyawan.get_children():                           # Hapus semua baris di tabel karyawan
            self.tree_karyawan.delete(item_id)
        for item in self.tree.get_children():                                       # Hapus semua baris di tabel hasil
            self.tree.delete(item)

        self.card_total_karyawan.configure(text="-")                                # Reset kartu ringkasan
        self.card_total_hari.configure(text="-")
        self.card_total_slot.configure(text="-")

        self.status.configure(text="Siap digunakan.")                                # Status kembali default
        self.entry_nama.focus()                                                     # Fokus lagi ke input nama

    # ========== FULLSCREEN ==========
    def _toggle_fullscreen(self, event=None):                                       # Handler F11: toggle fullscreen
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))

    def _exit_fullscreen(self, event=None):                                         # Handler ESC: keluar fullscreen
        self.attributes("-fullscreen", False)


if __name__ == "__main__":                                                          # Blok utama saat file dijalankan langsung
    app = ShiftApp()                                                                # Buat instance aplikasi ShiftApp
    app.mainloop()                                                                  # Jalankan event loop (tkinter/customtkinter)
  