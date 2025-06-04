import tkinter as tk
from tkinter import messagebox
import random

# Simulasi database akun dan tagihan (email: {password, tagihan})
akun_mahasiswa = {
    "230212060@student.ar-raniy.ac.id": {"password": "123456", "tagihan": 2500000},
    "230212061@student.ar-raniy.ac.id": {"password": "111111", "tagihan": 3500000},
}

# Status login dan email aktif
is_logged_in = False
email_aktif = ""

# Fungsi login dengan email dan password
def login():
    global is_logged_in, email_aktif
    email = email_entry.get()
    password = password_entry.get()

    if email in akun_mahasiswa and akun_mahasiswa[email]["password"] == password:
        is_logged_in = True
        email_aktif = email
        messagebox.showinfo("Login", f"Login berhasil sebagai {email}")
    elif email in akun_mahasiswa:
        messagebox.showerror("Login Gagal", "Password salah.")
    else:
        messagebox.showerror("Login Gagal", "Email tidak terdaftar di sistem.")

# Fungsi cek tagihan
def cek_tagihan():
    if not is_logged_in:
        messagebox.showwarning("Akses Ditolak", "Silakan login terlebih dahulu.")
        return
    tagihan = akun_mahasiswa[email_aktif]["tagihan"]
    tagihan_label.config(text=f"Tagihan UKT Anda: Rp {tagihan:,}")

# Fungsi generate nomor virtual account
def generate_va():
    if not is_logged_in:
        messagebox.showwarning("Akses Ditolak", "Silakan login terlebih dahulu.")
        return
    va_label.config(text="Nomor Virtual Account: 1234567890123456")

# Fungsi buka aplikasi m-banking
def buka_mbanking():
    if not is_logged_in:
        messagebox.showwarning("Akses Ditolak", "Silakan login terlebih dahulu.")
        return
    messagebox.showinfo("M-Banking", "Aplikasi m-banking dibuka.")

# Fungsi bayar UKT
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

        # Generate nomor invoice unik
        random_number = random.randint(1000, 9999)
        kode_email = email_aktif[-2:]
        invoice_number = f"INV-{random_number}-{kode_email.upper()}"

        invoice_label.config(text=f"Nomor Invoice: {invoice_number}")
        messagebox.showinfo("Pembayaran", f"Pembayaran berhasil!\nNomor Invoice Anda: {invoice_number}")

# ================= GUI =================

root = tk.Tk()
root.title("Aplikasi Pembayaran UKT - Edlink")
root.geometry("450x580")

# Judul
tk.Label(root, text="Pembayaran UKT Mahasiswa", font=("Helvetica", 16, "bold")).pack(pady=15)

# Input Email
tk.Label(root, text="Masukkan Email Akun Edlink Anda:").pack()
email_entry = tk.Entry(root, width=40)
email_entry.pack(pady=5)

# Input Password
tk.Label(root, text="Masukkan Password:").pack()
password_entry = tk.Entry(root, width=40, show="*")
password_entry.pack(pady=5)

# Tombol Login
tk.Button(root, text="Login", command=login, bg="lightblue", width=20).pack(pady=10)

# Tombol Cek Tagihan
tk.Button(root, text="Cek Tagihan UKT", command=cek_tagihan, width=25).pack(pady=5)
tagihan_label = tk.Label(root, text="", font=("Helvetica", 12))
tagihan_label.pack(pady=5)

# Tombol Generate VA
tk.Button(root, text="Generate Nomor Virtual Account", command=generate_va, width=30).pack(pady=5)
va_label = tk.Label(root, text="", font=("Helvetica", 12))
va_label.pack(pady=5)

# Tombol Buka M-Banking
tk.Button(root, text="Buka Aplikasi M-Banking", command=buka_mbanking, width=25).pack(pady=5)

# Tombol Bayar UKT
tk.Button(root, text="Bayar UKT", command=bayar_ukt, bg="lightgreen", width=20).pack(pady=20)

# Label Invoice
invoice_label = tk.Label(root, text="", font=("Helvetica", 12, "italic"), fg="darkgreen")
invoice_label.pack(pady=10)

# Jalankan GUI
root.mainloop()
