import datetime
import logging
import re
import tkinter as tk
from tkinter import messagebox

# --------------------------------------------------
# Setup Logging (Praktikum 5.1)
# --------------------------------------------------
logging.basicConfig(
    filename="aplikasi_biodata.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class AplikasiBiodata(tk.Tk):
    """Aplikasi Biodata Mahasiswa dengan Logging, Fitur Tambahan, & Validasi Lanjutan (OOP)."""

    def __init__(self):
        super().__init__()

        # --------------------------------------------------
        # 1. Konfigurasi Jendela Utama
        # --------------------------------------------------
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x820")
        self.resizable(True, True)
        self.minsize(550, 700)
        self.configure(bg="orange")

        # Database user sederhana
        self.users_db = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456",
            "yonn(24106050017)": "24106050017",  # User testing
        }

        # Status login dan manajemen frame
        self.current_user = None
        self.frame_aktif = None
        self.remember_var = tk.IntVar()
        self.saved_username = ""  # Variabel untuk fitur Remember Me

        # Variabel untuk kontrol Show/Hide Password
        self.show_password_var = tk.BooleanVar(value=False)

        # Membangun tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Tampilkan frame login di awal dan pastikan menu belum ada
        self._hapus_menu()
        self._pindah_ke(self.frame_login)

        # Log aplikasi start (Praktikum 5.4)
        logging.info("Aplikasi dimulai")

    # ==========================================================
    # 2. TAMPILAN FORM LOGIN
    # ==========================================================
    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=20, pady=60)

        # Konfigurasi grid agar tampilan berada di tengah
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)

        # Judul Login
        tk.Label(
            self.frame_login, text="HALAMAN LOGIN", font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=20)

        # Input Username
        tk.Label(self.frame_login, text="Username:", font=("Arial", 12)).grid(
            row=1, column=0, sticky="W", pady=5
        )
        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entry_username.grid(row=1, column=1, columnspan=2, pady=5, sticky="EW")

        # Input Password dengan Show/Hide Password (Tugas 2)
        tk.Label(self.frame_login, text="Password:", font=("Arial", 12)).grid(
            row=2, column=0, sticky="W", pady=5
        )
        self.entry_password = tk.Entry(
            self.frame_login, font=("Arial", 12), show="*"
        )
        self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")

        # Tombol Show/Hide Password
        self.btn_toggle_pass = tk.Button(
            self.frame_login,
            text="👁",
            font=("Arial", 10),
            command=self._toggle_password,
            width=3,
        )
        self.btn_toggle_pass.grid(row=2, column=2, padx=5, pady=5)

        # Checkbox Remember Me (Tugas 2)
        self.check_remember = tk.Checkbutton(
            self.frame_login,
            text="Remember Me",
            variable=self.remember_var,
            font=("Arial", 10),
        )
        self.check_remember.grid(
            row=3, column=1, columnspan=2, sticky="W", pady=5
        )

        # Tombol Login
        self.btn_login = tk.Button(
            self.frame_login,
            text="Login",
            font=("Arial", 12, "bold"),
            command=self._coba_login,
        )
        self.btn_login.grid(
            row=4, column=0, columnspan=3, pady=15, sticky="EW"
        )

        # Keyboard shortcuts untuk navigation login
        self.entry_username.bind(
            "<Return>", lambda e: self.entry_password.focus_set()
        )
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        # Info Kredensial untuk User
        info_label = tk.Label(
            self.frame_login,
            text=(
                "Info: Username yang tersedia:\n"
                "• admin (password: 123)\n"
                "• user1 (password: password1)\n"
                "• mahasiswa (password: 123456)\n"
                "• yonn(24106050017) (password: 24106050017)"
            ),
            font=("Arial", 9),
            fg="gray",
            justify=tk.LEFT,
        )
        info_label.grid(row=5, column=0, columnspan=3, pady=10)

    def _toggle_password(self):
        """Fitur Show/Hide Password (Tugas 2)."""
        if self.show_password_var.get():
            self.entry_password.config(show="*")
            self.show_password_var.set(False)
            self.btn_toggle_pass.config(text="👁")
        else:
            self.entry_password.config(show="")
            self.show_password_var.set(True)
            self.btn_toggle_pass.config(text="🙈")

    # ==========================================================
    # 3. TAMPILAN FORM BIODATA
    # ==========================================================
    def _buat_tampilan_biodata(self):
        # --- Variabel Kontrol Tkinter ---
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_email = tk.StringVar()  # Tugas 3
        self.var_telepon = tk.StringVar()  # Tugas 3
        self.var_tgllahir = tk.StringVar()  # Tugas 3
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        # Aktifkan trace untuk validasi real-time tombol submit
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)
        self.var_email.trace_add("write", self.validate_form)
        self.var_telepon.trace_add("write", self.validate_form)
        self.var_tgllahir.trace_add("write", self.validate_form)

        # --- Frame Biodata ---
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=10)
        self.frame_biodata.columnconfigure(1, weight=1)

        # Judul Form
        self.label_judul = tk.Label(
            master=self.frame_biodata,
            text="FORM BIODATA MAHASISWA",
            font=("Arial", 16, "bold"),
        )
        self.label_judul.grid(row=0, column=0, columnspan=2, pady=10)

        # Frame Khusus Input dengan Border
        self.frame_input = tk.Frame(
            master=self.frame_biodata,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=10,
            pady=10,
        )

        # Input Nama
        self.label_nama = tk.Label(
            master=self.frame_input, text="Nama Lengkap:", font=("Arial", 11)
        )
        self.label_nama.grid(row=0, column=0, sticky="W", pady=2)
        self.entry_nama = tk.Entry(
            master=self.frame_input,
            width=28,
            font=("Arial", 11),
            textvariable=self.var_nama,
        )
        self.entry_nama.grid(row=0, column=1, pady=2)

        # Input NIM
        self.label_nim = tk.Label(
            master=self.frame_input, text="NIM:", font=("Arial", 11)
        )
        self.label_nim.grid(row=1, column=0, sticky="W", pady=2)
        self.entry_nim = tk.Entry(
            master=self.frame_input,
            width=28,
            font=("Arial", 11),
            textvariable=self.var_nim,
        )
        self.entry_nim.grid(row=1, column=1, pady=2)

        # Input Jurusan
        self.label_jurusan = tk.Label(
            master=self.frame_input, text="Jurusan:", font=("Arial", 11)
        )
        self.label_jurusan.grid(row=2, column=0, sticky="W", pady=2)
        self.entry_jurusan = tk.Entry(
            master=self.frame_input,
            width=28,
            font=("Arial", 11),
            textvariable=self.var_jurusan,
        )
        self.entry_jurusan.grid(row=2, column=1, pady=2)

        # Input Email (Tugas 3)
        self.label_email = tk.Label(
            master=self.frame_input, text="Email:", font=("Arial", 11)
        )
        self.label_email.grid(row=3, column=0, sticky="W", pady=2)
        self.entry_email = tk.Entry(
            master=self.frame_input,
            width=28,
            font=("Arial", 11),
            textvariable=self.var_email,
        )
        self.entry_email.grid(row=3, column=1, pady=2)

        # Input Telepon (Tugas 3)
        self.label_telepon = tk.Label(
            master=self.frame_input, text="No. Telepon:", font=("Arial", 11)
        )
        self.label_telepon.grid(row=4, column=0, sticky="W", pady=2)
        self.entry_telepon = tk.Entry(
            master=self.frame_input,
            width=28,
            font=("Arial", 11),
            textvariable=self.var_telepon,
        )
        self.entry_telepon.grid(row=4, column=1, pady=2)

        # Input Tanggal Lahir (Tugas 3)
        self.label_tgllahir = tk.Label(
            master=self.frame_input,
            text="Tgl Lahir (DD-MM-YYYY):",
            font=("Arial", 11),
        )
        self.label_tgllahir.grid(row=5, column=0, sticky="W", pady=2)
        self.entry_tgllahir = tk.Entry(
            master=self.frame_input,
            width=28,
            font=("Arial", 11),
            textvariable=self.var_tgllahir,
        )
        self.entry_tgllahir.grid(row=5, column=1, pady=2)

        # Input Alamat (Text + Scrollbar)
        self.label_alamat = tk.Label(
            master=self.frame_input, text="Alamat:", font=("Arial", 11)
        )
        self.label_alamat.grid(row=6, column=0, sticky="NW", pady=2)

        self.frame_alamat = tk.Frame(
            master=self.frame_input, relief=tk.SUNKEN, borderwidth=1
        )
        self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_alamat = tk.Text(
            master=self.frame_alamat, height=3, width=26, font=("Arial", 11)
        )
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)
        self.frame_alamat.grid(row=6, column=1, pady=2)

        # Pilihan Jenis Kelamin
        self.label_jk = tk.Label(
            master=self.frame_input, text="Jenis Kelamin:", font=("Arial", 11)
        )
        self.label_jk.grid(row=7, column=0, sticky="W", pady=2)

        self.frame_jk = tk.Frame(master=self.frame_input)
        self.frame_jk.grid(row=7, column=1, sticky="W")

        self.radio_pria = tk.Radiobutton(
            master=self.frame_jk,
            text="Pria",
            variable=self.var_jk,
            value="Pria",
        )
        self.radio_pria.pack(side=tk.LEFT)

        self.radio_wanita = tk.Radiobutton(
            master=self.frame_jk,
            text="Wanita",
            variable=self.var_jk,
            value="Wanita",
        )
        self.radio_wanita.pack(side=tk.LEFT)

        # Checkbox Persetujuan
        self.check_setuju = tk.Checkbutton(
            master=self.frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 10),
            command=self.validate_form,
        )
        self.check_setuju.grid(
            row=8, column=0, columnspan=2, pady=5, sticky="W"
        )

        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")

        # Frame untuk Tombol Aksi (Submit & Reset Form)
        self.frame_tombol = tk.Frame(master=self.frame_biodata)
        self.frame_tombol.grid(row=2, column=0, columnspan=2, pady=10, sticky="EW")
        self.frame_tombol.columnconfigure(0, weight=1)
        self.frame_tombol.columnconfigure(1, weight=1)

        # Tombol Submit Biodata
        self.btn_submit = tk.Button(
            master=self.frame_tombol,
            text="Submit Biodata",
            font=("Arial", 11, "bold"),
            command=self.submit_data,
            state=tk.DISABLED,
        )
        self.btn_submit.grid(row=0, column=0, sticky="EW", padx=(0, 5))

        # Tombol Reset Form (Tugas 2)
        self.btn_reset = tk.Button(
            master=self.frame_tombol,
            text="Reset Form",
            font=("Arial", 11),
            bg="#ff9800",
            fg="white",
            command=self._reset_form_biodata,
        )
        self.btn_reset.grid(row=0, column=1, sticky="EW", padx=(5, 0))

        # Event Binding Mouse Hover & Keyboard
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)

        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)
        self.entry_email.bind("<Return>", self.submit_shortcut)
        self.entry_telepon.bind("<Return>", self.submit_shortcut)
        self.entry_tgllahir.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)

        # Label Tampilan Hasil
        self.label_hasil = tk.Label(
            master=self.frame_biodata,
            text="",
            font=("Arial", 9, "italic"),
            justify=tk.LEFT,
        )
        self.label_hasil.grid(
            row=3, column=0, columnspan=2, sticky="W", padx=5, pady=2
        )

    # ==========================================================
    # 4. LOGIC LOGIN & NAVIGATION (Praktikum 5.2)
    # ==========================================================
    def _coba_login(self):
        """Method untuk memproses attempt login dengan logging."""
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        # Log attempt login
        logging.info(f"Login attempt for username: {username}")

        # Validasi input kosong
        if not username or not password:
            logging.warning(
                f"Empty credentials attempt for username: {username}"
            )
            messagebox.showwarning(
                "Login Gagal", "Username dan Password tidak boleh kosong."
            )
            self.entry_username.focus_set()
            return

        # Validasi panjang minimum
        if len(username) < 3:
            logging.warning(f"Username too short: {username}")
            messagebox.showwarning(
                "Login Gagal", "Username minimal 3 karakter."
            )
            self.entry_username.focus_set()
            return

        # Cek kredensial di database
        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            logging.info(f"Successful login for user: {username}")
            messagebox.showinfo(
                "Login Berhasil", f"Selamat Datang, {username}!"
            )
            self._reset_form_biodata()
            self._update_title_with_user()
            self._buat_menu()  # Tampilkan Menu Bar lengkap
            self._pindah_ke(self.frame_biodata)

            # Cek Remember Me (Tugas 2)
            if self.remember_var.get() == 1:
                self.saved_username = username
            else:
                self.saved_username = ""

            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            messagebox.showerror(
                "Login Gagal", "Username atau Password salah."
            )
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    def _reset_form_biodata(self):
        """Reset semua field di form biodata."""
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.var_email.set("")
        self.var_telepon.set("")
        self.var_tgllahir.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.label_hasil.config(text="")

    def _update_title_with_user(self):
        """Update judul window dengan nama user yang login."""
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")

    def _pindah_ke(self, frame_tujuan):
        """Method untuk berpindah antar tampilan."""
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        if frame_tujuan == self.frame_login:
            if self.saved_username:
                self.entry_username.insert(0, self.saved_username)
                self.remember_var.set(1)
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())

    # ==========================================================
    # 5. LOGIC LOGOUT, FILE SAVING, & MENU BAR (Praktikum 5.3 - 5.4)
    # ==========================================================
    def simpan_hasil(self):
        """Simpan hasil biodata ke file dengan error handling."""
        try:
            hasil_tersimpan = self.label_hasil.cget("text")
            if (
                not hasil_tersimpan
                or "BIODATA TERSIMPAN" not in hasil_tersimpan
            ):
                messagebox.showwarning(
                    "Peringatan",
                    (
                        "Tidak ada data untuk disimpan. Mohon submit terlebih"
                        " dahulu."
                    ),
                )
                return

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{self.current_user}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Data disimpan oleh: {self.current_user}\n")
                file.write(
                    "Waktu penyimpanan:"
                    f" {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                file.write("-" * 50 + "\n")
                file.write(hasil_tersimpan)

            logging.info(
                f"Data successfully saved to file '{filename}' by"
                f" {self.current_user}"
            )
            messagebox.showinfo(
                "Info", f"Data berhasil disimpan ke file '{filename}'."
            )
        except PermissionError:
            logging.error(f"Permission error saving file by {self.current_user}")
            messagebox.showerror(
                "Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini."
            )
        except Exception as e:
            logging.error(
                f"Error saving file by {self.current_user}: {str(e)}"
            )
            messagebox.showerror(
                "Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}"
            )

    def _logout(self):
        """Method untuk logout dengan logging."""
        if messagebox.askyesno(
            "Logout", f"Apakah {self.current_user} yakin ingin logout?"
        ):
            logging.info(f"User logout: {self.current_user}")
            self.current_user = None
            self._hapus_menu()
            self._update_title_with_user()
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self._reset_form_biodata()
            self._pindah_ke(self.frame_login)
            self.entry_username.focus_set()

    def keluar_aplikasi(self):
        """Keluar dari aplikasi dengan konfirmasi dan logging (Praktikum 5.4)."""
        if messagebox.askokcancel(
            "Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"
        ):
            logging.info(
                f"Application closed by user: {self.current_user or 'Guest'}"
            )
            self.destroy()

    def _buat_menu(self):
        """Membuat menu bar untuk aplikasi."""
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)

        menu_bar.add_cascade(label="File", menu=file_menu)

    def _hapus_menu(self):
        """Menghapus menu bar dari window."""
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

    # ==========================================================
    # 6. CALLBACKS & VALIDASI LANJUTAN FORM BIODATA (Tugas 3)
    # ==========================================================
    def submit_data(self):
        """Submit data biodata dengan validasi lengkap dan logging."""
        try:
            if self.var_setuju.get() == 0:
                messagebox.showwarning(
                    "Peringatan", "Anda harus menyetujui pengumpulan data!"
                )
                return

            nama = self.entry_nama.get().strip()
            nim = self.entry_nim.get().strip()
            jurusan = self.entry_jurusan.get().strip()
            email = self.entry_email.get().strip()
            telepon = self.entry_telepon.get().strip()
            tgl_lahir = self.entry_tgllahir.get().strip()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()

            # Validasi field kosong
            if (
                not nama
                or not nim
                or not jurusan
                or not email
                or not telepon
                or not tgl_lahir
                or not alamat
            ):
                messagebox.showwarning(
                    "Input Kosong", "Semua field wajib diisi!"
                )
                return

            # Validasi format NIM
            if not nim.isdigit() or len(nim) < 8:
                messagebox.showwarning(
                    "Format NIM Salah", "NIM harus berupa angka minimal 8 digit!"
                )
                self.entry_nim.focus_set()
                return

            # Validasi nama
            if nama.isdigit():
                messagebox.showwarning(
                    "Format Nama Salah", "Nama tidak boleh hanya berupa angka!"
                )
                self.entry_nama.focus_set()
                return

            # Validasi Email (Tugas 3)
            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_pattern, email):
                messagebox.showwarning(
                    "Format Email Salah",
                    "Format email tidak valid (contoh: nama@domain.com)!",
                )
                self.entry_email.focus_set()
                return

            # Validasi Telepon Indonesia (Tugas 3: diawali 08 atau +62, panjang 10-13 digit)
            phone_pattern = r"^(\+62|08)[0-9]{8,11}$"
            if not re.match(phone_pattern, telepon):
                messagebox.showwarning(
                    "Format Telepon Salah",
                    (
                        "Nomor telepon harus format Indonesia (diawali 08/+62,"
                        " total 10-13 digit)!"
                    ),
                )
                self.entry_telepon.focus_set()
                return

            # Validasi Tanggal Lahir (Tugas 3: DD-MM-YYYY)
            date_pattern = r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$"
            if not re.match(date_pattern, tgl_lahir):
                messagebox.showwarning(
                    "Format Tanggal Salah",
                    "Format tanggal lahir harus DD-MM-YYYY (contoh:"
                    " 17-08-2003)!",
                )
                self.entry_tgllahir.focus_set()
                return

            # Format teks hasil
            hasil = (
                f"Nama: {nama}\n"
                f"NIM: {nim}\n"
                f"Jurusan: {jurusan}\n"
                f"Email: {email}\n"
                f"Telepon: {telepon}\n"
                f"Tgl Lahir: {tgl_lahir}\n"
                f"Alamat: {alamat}\n"
                f"Jenis Kelamin: {jenis_kelamin}"
            )

            messagebox.showinfo("Data Tersimpan", hasil)

            # Log successful data submission (Praktikum 5.3)
            logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}")

            hasil_lengkap = (
                f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
            )
            self.label_hasil.config(text=hasil_lengkap)

        except Exception as e:
            logging.error(
                f"Error in submit_data by {self.current_user}: {str(e)}"
            )
            messagebox.showerror(
                "Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}"
            )

    def validate_form(self, *args):
        """Validasi real-time tombol submit."""
        nama_v = self.var_nama.get().strip() != ""
        nim_v = self.var_nim.get().strip() != ""
        jurusan_v = self.var_jurusan.get().strip() != ""
        email_v = self.var_email.get().strip() != ""
        telp_v = self.var_telepon.get().strip() != ""
        tgl_v = self.var_tgllahir.get().strip() != ""
        setuju_v = self.var_setuju.get() == 1

        if (
            nama_v
            and nim_v
            and jurusan_v
            and email_v
            and telp_v
            and tgl_v
            and setuju_v
        ):
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def on_enter(self, event):
        if self.btn_submit["state"] == tk.NORMAL:
            self.btn_submit.config(bg="lightblue")

    def on_leave(self, event):
        self.btn_submit.config(bg="SystemButtonFace")

    def submit_shortcut(self, event=None):
        if self.btn_submit["state"] == tk.NORMAL:
            self.submit_data()


# ==========================================================
# 7. BLOK EKSEKUSI
# ==========================================================
if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()