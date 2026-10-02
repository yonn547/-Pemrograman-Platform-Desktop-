import tkinter as tk
from tkinter import messagebox

# --- FUNGSI SUBMIT (PERTEMUAN 2 & 3) ---
def submit_data():
    if var_setuju.get() == 0:
        messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
        return
    
    nama = entry_nama.get()
    nim = entry_nim.get()
    jurusan = entry_jurusan.get()
    alamat = text_alamat.get("1.0", tk.END).strip()
    jenis_kelamin = var_jk.get()
    
    if not nama or not nim or not jurusan or not alamat:
        messagebox.showwarning("doksli Kosong", "Semua doksli harus diisi!")
        return
    
    hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
    messagebox.showinfo("doksli Tersimpan", hasil)


# --- INISIALISASI JENDELA (PERTEMUAN 1 & 3) ---
window = tk.Tk()
window.title("Form Doksli Mahasiswa")      # Dari Praktikum 1.2
window.geometry("500x650")                  # Dari Praktikum 1.2
window.minsize(500, 650)                    # Dari Praktikum 3.10
window.resizable(True, True)                # Dari Praktikum 3.10

# Variabel Warna agar mudah diganti-ganti (Praktikum 1.4)
warna_bg_utama = "#E4CF98"
warna_bg_form = "white"

# Mengatur warna latar belakang jendela utama
window.configure(bg=warna_bg_utama)

# Variabel kontrol
var_jk = tk.StringVar(value="Pria")
var_setuju = tk.IntVar()


# --- FRAME UTAMA ---
main_frame = tk.Frame(master=window, padx=20, pady=20, bg=warna_bg_utama)
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame.grid_columnconfigure(1, weight=1)


# --- JUDUL ---
label_judul = tk.Label(master=main_frame, text="FORM DOKSLI MAHASISWA", font=("Arial", 16, "bold"), bg=warna_bg_utama)
label_judul.grid(row=0, column=0, columnspan=2, pady=20)


# --- FRAME KHUSUS INPUT ---
frame_input = tk.Frame(master=main_frame, relief=tk.GROOVE, borderwidth=2, padx=10, pady=10, bg=warna_bg_form)
frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")
frame_input.grid_columnconfigure(1, weight=1)


# --- WIDGET INPUT (Semua teks disamakan dengan warna_bg_form) ---
# Nama
label_nama = tk.Label(master=frame_input, text="Nama Lengkap:", font=("Arial", 12), bg=warna_bg_form)
label_nama.grid(row=0, column=0, sticky="W", pady=2)
entry_nama = tk.Entry(master=frame_input, width=30, font=("Arial", 12))
entry_nama.grid(row=0, column=1, pady=2, sticky="EW")

# NIM
label_nim = tk.Label(master=frame_input, text="NIM:", font=("Arial", 12), bg=warna_bg_form)
label_nim.grid(row=1, column=0, sticky="W", pady=2)
entry_nim = tk.Entry(master=frame_input, width=30, font=("Arial", 12))
entry_nim.grid(row=1, column=1, pady=2, sticky="EW")

# Jurusan
label_jurusan = tk.Label(master=frame_input, text="Jurusan:", font=("Arial", 12), bg=warna_bg_form)
label_jurusan.grid(row=2, column=0, sticky="W", pady=2)
entry_jurusan = tk.Entry(master=frame_input, width=30, font=("Arial", 12))
entry_jurusan.grid(row=2, column=1, pady=2, sticky="EW")

# Alamat
label_alamat = tk.Label(master=frame_input, text="Alamat:", font=("Arial", 12), bg=warna_bg_form)
label_alamat.grid(row=3, column=0, sticky="NW", pady=2)

frame_alamat = tk.Frame(master=frame_input, relief=tk.SUNKEN, borderwidth=1)
frame_alamat.grid(row=3, column=1, pady=2, sticky="EW")

scrollbar_alamat = tk.Scrollbar(master=frame_alamat)
scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

text_alamat = tk.Text(master=frame_alamat, height=5, width=28, font=("Arial", 12))
text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_alamat.config(command=text_alamat.yview)
text_alamat.config(yscrollcommand=scrollbar_alamat.set)

# Jenis Kelamin
label_jk = tk.Label(master=frame_input, text="Jenis Kelamin:", font=("Arial", 12), bg=warna_bg_form)
label_jk.grid(row=4, column=0, sticky="W", pady=2)

frame_jk = tk.Frame(master=frame_input, bg=warna_bg_form)
frame_jk.grid(row=4, column=1, sticky="W")

radio_pria = tk.Radiobutton(master=frame_jk, text="Pria", variable=var_jk, value="Pria", bg=warna_bg_form)
radio_pria.pack(side=tk.LEFT)
radio_wanita = tk.Radiobutton(master=frame_jk, text="Wanita", variable=var_jk, value="Wanita", bg=warna_bg_form)
radio_wanita.pack(side=tk.LEFT)

# Checkbox
check_setuju = tk.Checkbutton(
    master=frame_input,
    text="Saya menyetujui pengumpulan DOKSLI ini.",
    variable=var_setuju,
    font=("Arial", 10),
    bg=warna_bg_form
)
check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")


# --- TOMBOL SUBMIT ---
btn_submit = tk.Button(
    master=main_frame, 
    text="Submit DOKSLI", 
    font=("Arial", 12, "bold"),
    command=submit_data
)
btn_submit.grid(row=2, column=0, columnspan=2, pady=20, sticky="EW")


# --- MENJALANKAN EVENT LOOP ---
window.mainloop()