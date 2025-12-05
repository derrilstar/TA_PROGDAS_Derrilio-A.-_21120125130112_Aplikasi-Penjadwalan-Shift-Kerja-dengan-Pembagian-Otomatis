import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import random, math

# =========================
#  MODEL KARYAWAN
# =========================
class Karyawan:
    def __init__(self, nama: str):
        self.__nama = nama

    def get_nama(self):
        return self.__nama


# =========================
#  SCHEDULER (ROTASI SHIFT)
# =========================
class ShiftScheduler:
    def __init__(self, daftar_karyawan, jumlah_shift=4, kapasitas_per_shift=1, mode="normal"):
        base_shifts = ["Pagi", "Siang", "Sore", "Malam"]

        jumlah_shift = max(1, min(jumlah_shift, len(base_shifts)))
        kapasitas_per_shift = max(1, int(kapasitas_per_shift))

        self.daftar_karyawan = daftar_karyawan
        self.mode = mode
        self.shifts = base_shifts[:jumlah_shift]
        self.kapasitas = kapasitas_per_shift
        self.jadwal = []

    def generate(self, jumlah_hari: int):
        self.jadwal = []
        jumlah_hari = max(1, jumlah_hari)

        daftar = self.daftar_karyawan.copy()
        if not daftar:
            return []

        if self.mode == "random":
            random.shuffle(daftar)

        idx = 0  # pointer global (muter terus)
        for hari in range(1, jumlah_hari + 1):
            for shift_name in self.shifts:
                for slot_ke in range(1, self.kapasitas + 1):
                    karyawan = daftar[idx]
                    self.jadwal.append({
                        "hari": hari,
                        "shift": shift_name,
                        "slot": slot_ke,
                        "nama": karyawan.get_nama()
                    })
                    idx = (idx + 1) % len(daftar)

        return self.jadwal


# =========================
#  APLIKASI GUI
# =========================
class ShiftApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        ctk.set_widget_scaling(1.05)

        self.title("Aplikasi Penjadwalan Shift Kerja")
        self.geometry("1200x700")
        self.minsize(1000, 580)

        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Escape>", self._exit_fullscreen)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self._build_header()
        self._build_left_panel()
        self._build_right_panel()
        self._build_statusbar()

    # ========== HEADER ==========
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="#020617")
        header.grid(row=0, column=0, columnspan=2, sticky="nsew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Aplikasi Penjadwalan Shift Kerja",
            font=("Segoe UI", 26, "bold")
        ).grid(row=0, column=0, sticky="w", padx=22, pady=(14, 4))

        ctk.CTkLabel(
            header,
            text="Masukkan karyawan, atur jumlah shift, kapasitas per shift, dan jumlah hari. Jadwal akan dibagi otomatis dan berulang dengan sistem rotasi.",
            font=("Segoe UI", 13),
            text_color="#9ca3af",
            wraplength=900,
            justify="left"
        ).grid(row=1, column=0, sticky="w", padx=22, pady=(0, 10))

    # ========== LEFT PANEL ==========
    def _build_left_panel(self):
        outer = ctk.CTkFrame(self, fg_color="#020617")
        outer.grid(row=1, column=0, sticky="nsew", padx=(18, 9), pady=(10, 8))
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_rowconfigure(1, weight=0)
        outer.grid_columnconfigure(0, weight=1)

        self.left = ctk.CTkScrollableFrame(
            outer,
            corner_radius=16,
            fg_color="#020617",
            border_width=1,
            border_color="#1f2937"
        )
        self.left.grid(row=0, column=0, sticky="nsew", padx=4, pady=(4, 0))
        self.left.grid_columnconfigure(0, weight=1)
        self.left.grid_columnconfigure(1, weight=1)

        self._build_left_content()

        action_bar = ctk.CTkFrame(outer, fg_color="#020617")
        action_bar.grid(row=1, column=0, sticky="ew", padx=4, pady=(6, 4))
        action_bar.grid_columnconfigure(0, weight=1)
        action_bar.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            action_bar, text="Generate Shift", command=self._generate,
            height=40, font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, sticky="ew", padx=(6, 4), pady=2)

        ctk.CTkButton(
            action_bar, text="Clear Semua", command=self._clear_all,
            height=40, fg_color="#4b5563", font=("Segoe UI", 13)
        ).grid(row=0, column=1, sticky="ew", padx=(4, 6), pady=2)

    def _build_left_content(self):
        # --- Section: Karyawan ---
        ctk.CTkLabel(self.left, text="Karyawan", font=("Segoe UI", 15, "bold"))\
            .grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(14, 4))

        ctk.CTkLabel(
            self.left,
            text="Masukkan nama karyawan, tekan Enter atau klik Tambah.",
            font=("Segoe UI", 11),
            text_color="#9ca3af"
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 8))

        ctk.CTkLabel(self.left, text="Nama karyawan:", font=("Segoe UI", 13))\
            .grid(row=2, column=0, sticky="w", padx=16, pady=(4, 0))
        self.entry_nama = ctk.CTkEntry(
            self.left,
            placeholder_text="Contoh: Raihan",
            height=34,
            font=("Segoe UI", 13)
        )
        self.entry_nama.grid(row=3, column=0, sticky="ew", padx=16, pady=(4, 4))
        self.entry_nama.bind("<Return>", lambda e: self._tambah_karyawan())
        self.entry_nama.focus()

        ctk.CTkButton(
            self.left, text="Tambah",
            command=self._tambah_karyawan,
            height=32, font=("Segoe UI", 12, "bold")
        ).grid(row=3, column=1, sticky="w", padx=(0, 16), pady=(4, 4))

        ctk.CTkButton(
            self.left, text="Hapus Terpilih",
            fg_color="#b91c1c",
            command=self._hapus_terpilih,
            height=32, font=("Segoe UI", 11)
        ).grid(row=4, column=0, sticky="w", padx=16, pady=(2, 4))

        ctk.CTkButton(
            self.left, text="Hapus Semua",
            fg_color="#ef4444",
            command=self._hapus_semua,
            height=30, font=("Segoe UI", 11)
        ).grid(row=4, column=1, sticky="w", padx=(0, 16), pady=(2, 4))

        # Tabel karyawan
        ctk.CTkLabel(self.left, text="Daftar karyawan:", font=("Segoe UI", 13))\
            .grid(row=5, column=0, columnspan=2, sticky="w", padx=16, pady=(8, 4))

        table_frame = ctk.CTkFrame(self.left, fg_color="#020617")
        table_frame.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=16)
        self.left.grid_rowconfigure(6, weight=1)

        self.tree_karyawan = ttk.Treeview(
            table_frame,
            columns=("nama",),
            show="headings",
            height=6
        )
        self.tree_karyawan.heading("nama", text="Nama")
        self.tree_karyawan.column("nama", width=220, anchor="w")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#020617",
            fieldbackground="#020617",
            foreground="#e5e7eb",
            rowheight=30,               # lebih tinggi
            font=("Segoe UI", 13),      # isi tabel lebih besar
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#111827",
            foreground="#e5e7eb",
            font=("Segoe UI", 13, "bold")  # heading lebih besar
        )

        self.tree_karyawan.pack(side="left", fill="both", expand=True)
        scroll_k = ctk.CTkScrollbar(table_frame, command=self.tree_karyawan.yview)
        scroll_k.pack(side="right", fill="y")
        self.tree_karyawan.configure(yscrollcommand=scroll_k.set)

        # --- Section: Pengaturan Jadwal ---
        ctk.CTkLabel(self.left, text="Pengaturan Jadwal", font=("Segoe UI", 15, "bold"))\
            .grid(row=7, column=0, columnspan=2, sticky="w", padx=16, pady=(14, 4))

        ctk.CTkLabel(self.left, text="Jumlah shift (1–4):", font=("Segoe UI", 13))\
            .grid(row=8, column=0, sticky="w", padx=16, pady=(4, 0))
        self.shift_var = ctk.StringVar(value="4")
        ctk.CTkOptionMenu(
            self.left, values=["1", "2", "3", "4"],
            variable=self.shift_var, width=90, font=("Segoe UI", 12)
        ).grid(row=8, column=1, sticky="w", padx=(0, 16), pady=(4, 0))

        ctk.CTkLabel(self.left, text="Kapasitas per shift:", font=("Segoe UI", 13))\
            .grid(row=9, column=0, sticky="w", padx=16, pady=(8, 0))
        self.cap_var = ctk.StringVar(value="1")
        ctk.CTkOptionMenu(
            self.left, values=["1", "2", "3", "4", "5"],
            variable=self.cap_var, width=90, font=("Segoe UI", 12)
        ).grid(row=9, column=1, sticky="w", padx=(0, 16), pady=(8, 0))

        ctk.CTkLabel(self.left, text="Jumlah hari:", font=("Segoe UI", 13))\
            .grid(row=10, column=0, sticky="w", padx=16, pady=(8, 0))
        self.entry_hari = ctk.CTkEntry(
            self.left,
            placeholder_text="Contoh: 1 atau 7",
            width=110,
            height=32,
            font=("Segoe UI", 12)
        )
        self.entry_hari.grid(row=10, column=1, sticky="w", padx=(0, 16), pady=(8, 0))
        self.entry_hari.bind("<Return>", lambda e: self._generate())

        self.autodays_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            self.left,
            text="Auto hari (semua karyawan minimal 1x kebagian)",
            variable=self.autodays_var,
            font=("Segoe UI", 11)
        ).grid(row=11, column=0, columnspan=2, sticky="w", padx=16, pady=(6, 0))

        ctk.CTkLabel(self.left, text="Mode pembagian:", font=("Segoe UI", 13))\
            .grid(row=12, column=0, sticky="w", padx=16, pady=(8, 0))
        self.mode_var = ctk.StringVar(value="normal")
        ctk.CTkOptionMenu(
            self.left,
            values=["normal", "random"],
            variable=self.mode_var,
            width=120,
            font=("Segoe UI", 12)
        ).grid(row=12, column=1, sticky="w", padx=(0, 16), pady=(8, 0))

    # ========== RIGHT PANEL (SUMMARY CARDS + TABLE) ==========
    def _build_right_panel(self):
        right_outer = ctk.CTkFrame(self, fg_color="#020617")
        right_outer.grid(row=1, column=1, sticky="nsew", padx=(9, 18), pady=(10, 8))
        right_outer.grid_rowconfigure(0, weight=0)
        right_outer.grid_rowconfigure(1, weight=1)
        right_outer.grid_columnconfigure(0, weight=1)

        # summary cards row
        summary_frame = ctk.CTkFrame(right_outer, fg_color="#020617")
        summary_frame.grid(row=0, column=0, sticky="ew", padx=4, pady=(4, 2))
        summary_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.card_total_karyawan = self._create_summary_card(summary_frame, "Total Karyawan", "-", 0)
        self.card_total_hari = self._create_summary_card(summary_frame, "Total Hari", "-", 1)
        self.card_total_slot = self._create_summary_card(summary_frame, "Total Slot / Jadwal", "-", 2)

        # frame untuk tabel hasil
        main = ctk.CTkFrame(
            right_outer,
            corner_radius=16,
            fg_color="#020617",
            border_width=1,
            border_color="#1f2937"
        )
        main.grid(row=1, column=0, sticky="nsew", padx=4, pady=(2, 4))
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            main,
            text="Hasil Penjadwalan",
            font=("Segoe UI", 17, "bold")
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(14, 6))

        table_frame = ctk.CTkFrame(main, fg_color="#020617")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 14))

        columns = ("hari", "shift", "slot", "nama")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

        self.tree.heading("hari", text="Hari")
        self.tree.heading("shift", text="Shift")
        self.tree.heading("slot", text="Petugas#")
        self.tree.heading("nama", text="Nama Karyawan")

        self.tree.column("hari", width=60, anchor="center")
        self.tree.column("shift", width=120, anchor="center")
        self.tree.column("slot", width=80, anchor="center")
        self.tree.column("nama", width=260, anchor="w")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#020617",
            fieldbackground="#020617",
            foreground="#e5e7eb",
            rowheight=30,               # sama seperti tabel kiri
            font=("Segoe UI", 13),      # isi tabel besar
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#111827",
            foreground="#e5e7eb",
            font=("Segoe UI", 13, "bold")  # heading besar
        )

        self.tree.pack(side="left", fill="both", expand=True)
        scroll_y = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        scroll_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll_y.set)

    def _create_summary_card(self, parent, title, value, column):
        frame = ctk.CTkFrame(
            parent,
            fg_color="#020617",
            corner_radius=18,
            border_width=1,
            border_color="#1f2937"
        )
        frame.grid(row=0, column=column, sticky="ew", padx=6, pady=4)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 11),
            text_color="#9ca3af"
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(8, 0))

        label_value = ctk.CTkLabel(
            frame,
            text=value,
            font=("Segoe UI", 22, "bold")
        )
        label_value.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 10))

        return label_value

    # ========== STATUS BAR ==========
    def _build_statusbar(self):
        self.status = ctk.CTkLabel(
            self,
            text="Siap digunakan.",
            anchor="w",
            font=("Segoe UI", 11)
        )
        self.status.grid(row=2, column=0, columnspan=2, sticky="ew", padx=18, pady=(0, 8))

    # ========== EVENT HANDLER ==========
    def _tambah_karyawan(self):
        nama = self.entry_nama.get().strip()
        if not nama:
            messagebox.showwarning("Peringatan", "Nama karyawan tidak boleh kosong!")
            return

        self.tree_karyawan.insert("", tk.END, values=(nama,))
        self.entry_nama.delete(0, tk.END)
        self.entry_nama.focus()

        total = len(self.tree_karyawan.get_children())
        self.status.configure(text=f"'{nama}' ditambahkan. Total {total} karyawan.")

    def _hapus_terpilih(self):
        selected = self.tree_karyawan.selection()
        if not selected:
            messagebox.showinfo("Info", "Pilih karyawan yang ingin dihapus.")
            return
        for item_id in selected:
            self.tree_karyawan.delete(item_id)

        total = len(self.tree_karyawan.get_children())
        self.status.configure(text=f"Data karyawan diperbarui. Sisa {total} orang.")

    def _hapus_semua(self):
        if not self.tree_karyawan.get_children():
            return
        if messagebox.askyesno("Konfirmasi", "Hapus semua karyawan?"):
            for item_id in self.tree_karyawan.get_children():
                self.tree_karyawan.delete(item_id)
            self.status.configure(text="Daftar karyawan dikosongkan.")
            self.card_total_karyawan.configure(text="-")
            self.card_total_hari.configure(text="-")
            self.card_total_slot.configure(text="-")

    def _generate(self):
        rows = self.tree_karyawan.get_children()
        if not rows:
            messagebox.showwarning("Peringatan", "Tambahkan minimal satu karyawan terlebih dahulu.")
            return

        daftar_obj = []
        for item_id in rows:
            (nama,) = self.tree_karyawan.item(item_id)["values"]
            daftar_obj.append(Karyawan(nama))

        try:
            jshift = int(self.shift_var.get())
        except ValueError:
            jshift = 4

        try:
            kapasitas = int(self.cap_var.get())
        except ValueError:
            kapasitas = 1

        hari_txt = self.entry_hari.get().strip()
        jhari_input = None
        if hari_txt:
            try:
                jhari_input = int(hari_txt)
            except ValueError:
                messagebox.showwarning("Peringatan", "Jumlah hari harus berupa angka.")
                return

        slots_per_day = jshift * kapasitas
        minimal_days = max(1, math.ceil(len(daftar_obj) / slots_per_day))

        if self.autodays_var.get():
            jhari = max(jhari_input or 0, minimal_days)
        else:
            jhari = jhari_input if jhari_input and jhari_input > 0 else 1

        mode = self.mode_var.get()

        scheduler = ShiftScheduler(daftar_obj, jshift, kapasitas, mode)
        hasil = scheduler.generate(jhari)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in hasil:
            self.tree.insert(
                "",
                tk.END,
                values=(row["hari"], row["shift"], row["slot"], row["nama"])
            )

        total_slots = len(hasil)

        # update cards
        self.card_total_karyawan.configure(text=str(len(daftar_obj)))
        self.card_total_hari.configure(text=str(jhari))
        self.card_total_slot.configure(text=str(total_slots))

        self.status.configure(
            text=f"Jadwal: {jhari} hari • {len(daftar_obj)} karyawan • {len(scheduler.shifts)} shift • kapasitas {kapasitas}/shift • total slot {total_slots} • mode: {mode}"
        )

    def _clear_all(self):
        self.entry_nama.delete(0, tk.END)
        self.entry_hari.delete(0, tk.END)

        for item_id in self.tree_karyawan.get_children():
            self.tree_karyawan.delete(item_id)
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.card_total_karyawan.configure(text="-")
        self.card_total_hari.configure(text="-")
        self.card_total_slot.configure(text="-")

        self.status.configure(text="Siap digunakan.")
        self.entry_nama.focus()

    # ========== FULLSCREEN ==========
    def _toggle_fullscreen(self, event=None):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))

    def _exit_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)


if __name__ == "__main__":
    app = ShiftApp()
    app.mainloop()
