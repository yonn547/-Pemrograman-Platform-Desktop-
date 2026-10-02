# Mengimpor library tkinter
import tkinter as tk

# Membuat jendela utama
window = tk.Tk()

# Memberikan judul pada jendela
window.title("Form Biodata Mahasiswa")

# Mengatur ukuran jendela (lebar x tinggi)
window.geometry("500x600")
# Mencegah jendela dapat diubah ukurannya
window.resizable(False, False)

# Mengatur warna latar belakang jendela
window.configure(bg="black")

# Membuat label judul
label_judul = tk.Label(
    master=window,
    text="FORM BIODATA MAHASISWA",
    font=("Arial", 16, "bold")
)

# Menampilkan label dengan pack
label_judul.pack(pady=20)
# Label untuk input nama
label_nama = tk.Label(master=window, text="Nama Lengkap:", font=("Arial", 12))
label_nama.pack(pady=5)

# Entry untuk input nama
entry_nama = tk.Entry(master=window, width=50)
entry_nama.pack(pady=5)

# Input NIM
label_nim = tk.Label(master=window, text="NIM:", font=("Arial", 12))
label_nim.pack(pady=5)
entry_nim = tk.Entry(master=window, width=50)
entry_nim.pack(pady=5)

# Input Jurusan  
label_jurusan = tk.Label(master=window, text="Jurusan:", font=("Arial", 12))
label_jurusan.pack(pady=5)
entry_jurusan = tk.Entry(master=window, width=50)
entry_jurusan.pack(pady=5)



# Menjalankan event loop
window.mainloop()