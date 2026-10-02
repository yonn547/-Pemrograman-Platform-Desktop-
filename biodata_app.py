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

# Menjalankan event loop
window.mainloop()