import tkinter as tk
from tkinter import messagebox
import random
import sqlite3

# ====== DATABASE SETUP ======
conn = sqlite3.connect('ukt_pembayaran.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS histori_pembayaran (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        invoice TEXT
    )
''')
conn.commit()

# ====== VARIABEL ======
akun_mahasiswa = {}
is_logged_in = False
email_aktif = ""

# ====== FUNGSI ======
def login():
    global is_logged_in, email_aktif

    email = email_entry.get().strip()
    if email == "":
        messagebox.showerror("Login Gagal", "Email tidak boleh kosong.")
        return

    if email not in akun_mahasiswa:
        akun_mahasiswa[email] = {"tagihan": 2500000}

    is_logged_in = True
    email_aktif = email
    messagebox.showinfo("Login", f"Login berhasil sebagai {email}")

def cek_tagihan():
    if not is_logged_in:
        messagebox.showwarning("Akses Ditolak", "Silakan login terlebih dahulu.")
        return
    tagihan = akun_mahasiswa[email_aktif]["tagihan"]
    tagihan_label.config(text=f"Tagihan UKT Anda: Rp {tagihan:,}")

def buka_mbanking():
    if not is_logged_in:
        messagebox.showwarning("Akses Ditolak", "Silakan login terlebih dahulu.")
        return
    messagebox.showinfo("M-Banking", "Aplikasi m-banking dibuka.")

def generate_va():
    if not is_logged_in:
        messagebox.showwarning("Akses Ditolak", "Silakan login terlebih dahulu.")
        return

    bank = bank_var.get()
    if bank == "":
        messagebox.showwarning("Bank", "Silakan pilih bank terlebih dahulu.")
        return

    bank_kode = {
        "BNI": "8808",
        "BRI": "002",
        "Mandiri": "008",
        "BCA": "014"
    }

    kode_bank = bank_kode.get(bank, "999")
    va_number = f"{kode_bank}{random.randint(1000000000, 9999999999)}"
    va_label.config(text=f"Nomor VA ({bank}): {va_number}")

def bayar_ukt():
    if not is_logged_in:
        messagebox.showwarning("Akses Ditolak", "Silakan login terlebih dahulu.")
        return

    tagihan = akun_mahasiswa[email_aktif]["tagihan"]
    if tagihan <= 0:
        messagebox.showinfo("Pembayaran", "Anda sudah membayar UKT.")
    else:
        akun_mahasiswa[email_aktif]["tagihan"] = 0
        tagihan_label.config(text="Tagihan UKT Anda: Rp 0")

        random_number = random.randint(1000, 9999)
        kode_email = email_aktif[-2:]
        invoice_number = f"INV-{random_number}-{kode_email.upper()}"

        cursor.execute("INSERT INTO histori_pembayaran (email, invoice) VALUES (?, ?)", 
                       (email_aktif, invoice_number))
        conn.commit()

        invoice_label.config(text=f"Nomor Invoice: {invoice_number}")
        messagebox.showinfo("Pembayaran", f"Pembayaran berhasil!\nNomor Invoice Anda: {invoice_number}")

def tampilkan_histori():
    if not is_logged_in:
        messagebox.showwarning("Akses Ditolak", "Silakan login terlebih dahulu.")
        return

    cursor.execute("SELECT invoice FROM histori_pembayaran WHERE email = ?", (email_aktif,))
    hasil = cursor.fetchall()
    if not hasil:
        messagebox.showinfo("Histori", "Belum ada histori pembayaran.")
    else:
        histori_text = "\n".join([f"- {row[0]}" for row in hasil])
        messagebox.showinfo("Histori Pembayaran", f"Histori Pembayaran:\n{histori_text}")

def tampilkan_histori_semua():
    histori_window = tk.Toplevel(root)
    histori_window.title("Histori Pembayaran Semua Mahasiswa")
    histori_window.geometry("500x400")

    tk.Label(histori_window, text="Histori Pembayaran Semua Mahasiswa", font=("Helvetica", 14, "bold")).pack(pady=10)

    text_area = tk.Text(histori_window, wrap=tk.WORD)
    text_area.pack(expand=True, fill="both", padx=10, pady=5)

    cursor.execute("SELECT email, invoice FROM histori_pembayaran ORDER BY id DESC")
    hasil = cursor.fetchall()
    if not hasil:
        text_area.insert(tk.END, "Belum ada histori pembayaran.")
    else:
        for row in hasil:
            text_area.insert(tk.END, f"{row[0]} - {row[1]}\n")

    def simpan_histori():
        with open("histori_pembayaran.txt", "w") as f:
            histori = text_area.get("1.0", tk.END).strip()
            f.write(histori)
        messagebox.showinfo("Sukses", "Histori berhasil disimpan ke file 'histori_pembayaran.txt'.")

    tk.Button(histori_window, text="Simpan ke File", command=simpan_histori, bg="lightblue").pack(pady=10)

# ====== GUI ======
root = tk.Tk()
root.title("Aplikasi Pembayaran UKT - Edlink")
root.geometry("480x650")

tk.Label(root, text="Pembayaran UKT Mahasiswa", font=("Helvetica", 16, "bold")).pack(pady=15)

tk.Label(root, text="Masukkan Email Akun Edlink Anda:").pack()
email_entry = tk.Entry(root, width=40)
email_entry.pack(pady=5)

tk.Button(root, text="Login", command=login, bg="lightblue", width=20).pack(pady=10)

tk.Button(root, text="Cek Tagihan UKT", command=cek_tagihan, width=25).pack(pady=5)
tagihan_label = tk.Label(root, text="", font=("Helvetica", 12))
tagihan_label.pack(pady=5)

tk.Label(root, text="Pilih Bank:").pack()
bank_var = tk.StringVar()
bank_dropdown = tk.OptionMenu(root, bank_var, "BNI", "BRI", "Mandiri", "BCA")
bank_dropdown.pack(pady=5)

tk.Button(root, text="Generate Nomor Virtual Account", command=generate_va, width=30).pack(pady=10)
va_label = tk.Label(root, text="", font=("Helvetica", 12))
va_label.pack(pady=5)

tk.Button(root, text="Buka Aplikasi M-Banking", command=buka_mbanking, width=25).pack(pady=5)

tk.Button(root, text="Bayar UKT", command=bayar_ukt, bg="lightgreen", width=20).pack(pady=20)
invoice_label = tk.Label(root, text="", font=("Helvetica", 12, "italic"), fg="darkgreen")
invoice_label.pack(pady=10)

tk.Button(root, text="Tampilkan Histori Pembayaran", command=tampilkan_histori, bg="orange", width=30).pack(pady=10)

tk.Button(root, text="Tampilkan Histori Semua Mahasiswa", command=tampilkan_histori_semua, bg="lightgray", width=35).pack(pady=5)

root.mainloop()