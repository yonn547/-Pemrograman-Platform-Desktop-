import tkinter as tk
from tkinter import messagebox, ttk
import random

class QuizApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quiz Interaktif - Tugas Akhir")
        self.window.geometry("700x550")
        self.window.configure(bg="#f0f0f0")

        # 1. DATA QUIZ (10 Soal, ada unsur Web3/Security agar relevan denganmu)
        self.questions = [
            {"question": "Apa itu event-driven programming?", "options": ["Program berjalan berurutan", "Program merespons kejadian", "Program tanpa GUI", "Program berbasis web"], "correct": 1},
            {"question": "Method Tkinter untuk eksekusi non-blocking adalah?", "options": ["time.sleep()", "root.after()", "root.block()", "root.wait()"], "correct": 1},
            {"question": "Apa fungsi utama dari 'Event Loop'?", "options": ["Menghentikan program", "Mendengarkan dan memproses event", "Menghapus memori", "Membuat variabel"], "correct": 1},
            {"question": "Variabel Tkinter untuk data boolean adalah?", "options": ["StringVar", "IntVar", "BooleanVar", "DoubleVar"], "correct": 2},
            {"question": "Dalam keamanan Web3, apa itu 'Reentrancy Attack'?", "options": ["Serangan phishing", "Memanggil fungsi kontrak berulang sebelum state diperbarui", "Mencuri private key", "DDoS pada node"], "correct": 1},
            {"question": "Widget Tkinter yang paling cocok untuk animasi grafis adalah?", "options": ["Label", "Button", "Canvas", "Entry"], "correct": 2},
            {"question": "Bagaimana cara membatalkan timer yang sedang berjalan di Tkinter?", "options": ["root.stop()", "root.after_cancel(id)", "root.destroy()", "root.break()"], "correct": 1},
            {"question": "Validasi yang terjadi saat pengguna mengetik disebut?", "options": ["Submit-time", "Real-time", "Post-validation", "Batch validation"], "correct": 1},
            {"question": "Apa kepanjangan dari RPL dalam konteks kuliah?", "options": ["Rekayasa Perangkat Lunak", "Rancangan Program Logika", "Routing Protokol Layer", "Remote Python Lab"], "correct": 0},
            {"question": "Shortcut keyboard untuk 'Submit' di aplikasi ini adalah?", "options": ["Ctrl+S", "Enter", "Space", "Tab"], "correct": 1}
        ]
        random.shuffle(self.questions) # Acak soal setiap kali dijalankan

        # 2. STATE MANAGEMENT
        self.current_question = 0
        self.score = 0
        self.time_left = 15 # 15 detik per soal
        self.timer_id = None
        self.selected_answer = tk.IntVar(value=-1) # -1 artinya belum memilih

        self.buat_interface()
        self.bind_keyboard()
        self.load_question()

    def buat_interface(self):
        # Frame Utama
        main_frame = tk.Frame(self.window, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header: Score & Timer
        header_frame = tk.Frame(main_frame, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.score_label = tk.Label(header_frame, text="Skor: 0", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="blue")
        self.score_label.pack(side=tk.LEFT)
        
        self.timer_label = tk.Label(header_frame, text="Waktu: 15s", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="red")
        self.timer_label.pack(side=tk.RIGHT)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100, length=600)
        self.progress_bar.pack(fill=tk.X, pady=(0, 15))

        # Area Soal (Dengan background untuk animasi feedback)
        self.question_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        self.question_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.question_label = tk.Label(self.question_frame, text="", font=("Arial", 14, "bold"), bg="white", wraplength=600, justify="center")
        self.question_label.pack(pady=20)

        # Area Opsi Jawaban
        self.options_frame = tk.Frame(self.question_frame, bg="white")
        self.options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.option_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.options_frame, text="", variable=self.selected_answer, value=i, font=("Arial", 12), bg="white", anchor="w")
            rb.pack(fill=tk.X, pady=5)
            self.option_buttons.append(rb)

        # Tombol Kontrol
        btn_frame = tk.Frame(main_frame, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.btn_submit = tk.Button(btn_frame, text="Jawab (Enter)", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=self.submit_answer)
        self.btn_submit.pack(side=tk.RIGHT, padx=5)
        
        self.btn_skip = tk.Button(btn_frame, text="Lewati (Esc)", font=("Arial", 12), bg="#f44336", fg="white", command=self.skip_question)
        self.btn_skip.pack(side=tk.RIGHT, padx=5)

    def bind_keyboard(self):
        # Event handling untuk keyboard shortcuts
        self.window.bind('<Return>', lambda event: self.submit_answer())
        self.window.bind('<Escape>', lambda event: self.skip_question())

    def load_question(self):
        # Reset state per soal
        self.time_left = 15
        self.selected_answer.set(-1)
        self.question_frame.config(bg="white") # Reset warna animasi
        self.question_label.config(bg="white")
        
        # Update UI
        q_data = self.questions[self.current_question]
        self.question_label.config(text=f"Soal {self.current_question + 1}/{len(self.questions)}\n\n{q_data['question']}")
        
        for i, rb in enumerate(self.option_buttons):
            rb.config(text=q_data['options'][i])

        # Update Progress Bar
        progress = (self.current_question / len(self.questions)) * 100
        self.progress_var.set(progress)

        # Mulai Timer
        self.start_timer()

    def start_timer(self):
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Waktu: {self.time_left}s")
            self.timer_id = self.window.after(1000, self.update_timer)
        else:
            # Waktu habis, otomatis anggap salah/lewati
            self.show_feedback(False)

    def submit_answer(self):
        # Validasi: Pastikan user memilih jawaban
        if self.selected_answer.get() == -1:
            messagebox.showwarning("Peringatan", "Pilih salah satu jawaban terlebih dahulu!")
            return
        
        # Cek jawaban
        is_correct = (self.selected_answer.get() == self.questions[self.current_question]['correct'])
        
        if is_correct:
            self.score += 10
            self.score_label.config(text=f"Skor: {self.score}")
        
        self.show_feedback(is_correct)

    def skip_question(self):
        self.show_feedback(False, is_skip=True)

    def show_feedback(self, is_correct, is_skip=False):
        # Hentikan timer
        if self.timer_id:
            self.window.after_cancel(self.timer_id)

        # Animasi Visual Feedback
        color = "green" if is_correct else "red"
        msg = "Benar!" if is_correct else ("Dilewati" if is_skip else "Salah!")
        
        self.question_frame.config(bg=color)
        self.question_label.config(bg=color)
        
        # Delay 800ms agar user melihat feedback, lalu lanjut
        self.window.after(800, self.next_question)

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.show_result()

    def show_result(self):
        self.progress_var.set(100)
        final_score = self.score
        max_score = len(self.questions) * 10
        
        # Evaluasi hasil
        if final_score >= 80:
            msg = f"LUAR BIASA! Skor Anda: {final_score}/{max_score}\nLogika pemrograman Anda sudah solid."
        elif final_score >= 50:
            msg = f"CUKUP BAIK. Skor Anda: {final_score}/{max_score}\nTingkatkan lagi pemahaman tentang event loop dan state."
        else:
            msg = f"PERLU BELAJAR LAGI. Skor Anda: {final_score}/{max_score}\nJangan menyerah, ulangi materinya."

        messagebox.showinfo("Hasil Akhir", msg)
        self.window.quit()

    def jalankan(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = QuizApp()
    app.jalankan()