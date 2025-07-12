import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime

class AplikasiServisKendaraan:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Servis Kendaraan")
        self.root.geometry("800x600")
        
        # Struktur data
        self.daftar_servis = []
        self.peta_servis = {}
        
        # Gaya tampilan
        self.gaya = ttk.Style()
        self.gaya.theme_use('clam')
        
        # Inisialisasi GUI
        self.inisialisasi_gui()
        
        # Muat data saat aplikasi dimulai
        self.muat_dari_csv()
    
    def inisialisasi_gui(self):
        # Frame utama
        frame_utama = ttk.Frame(self.root, padding="10")
        frame_utama.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Judul aplikasi
        label_judul = ttk.Label(frame_utama, text="Sistem Servis Kendaraan", font=("Arial", 16, "bold"))
        label_judul.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame input data
        frame_input = ttk.LabelFrame(frame_utama, text="Input Data Servis", padding="10")
        frame_input.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Kolom-kolom input
        ttk.Label(frame_input, text="Plat Nomor:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.input_plat = ttk.Entry(frame_input, width=30)
        self.input_plat.grid(row=0, column=1, padx=(10, 0), pady=2)
        
        ttk.Label(frame_input, text="Merk Kendaraan:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.input_merk = ttk.Entry(frame_input, width=30)
        self.input_merk.grid(row=1, column=1, padx=(10, 0), pady=2)
        
        ttk.Label(frame_input, text="Tanggal Servis:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.input_tanggal = ttk.Entry(frame_input, width=30)
        self.input_tanggal.grid(row=2, column=1, padx=(10, 0), pady=2)
        self.input_tanggal.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Label(frame_input, text="Jenis Servis:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.input_jenis = ttk.Entry(frame_input, width=30)
        self.input_jenis.grid(row=3, column=1, padx=(10, 0), pady=2)
        
        # Tombol-tombol aksi
        frame_tombol = ttk.Frame(frame_input)
        frame_tombol.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(frame_tombol, text="Tambah", command=self.tambah_servis).grid(row=0, column=0, padx=5)
        ttk.Button(frame_tombol, text="Ubah", command=self.ubah_servis).grid(row=0, column=1, padx=5)
        ttk.Button(frame_tombol, text="Hapus", command=self.hapus_servis).grid(row=0, column=2, padx=5)
        ttk.Button(frame_tombol, text="Bersihkan", command=self.bersihkan_input).grid(row=0, column=3, padx=5)
        
        # Frame pencarian
        frame_cari = ttk.LabelFrame(frame_utama, text="Pencarian", padding="10")
        frame_cari.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(frame_cari, text="Cari berdasarkan Plat:").grid(row=0, column=0, sticky=tk.W)
        self.input_cari = ttk.Entry(frame_cari, width=30)
        self.input_cari.grid(row=0, column=1, padx=(10, 0))
        ttk.Button(frame_cari, text="Cari", command=self.cari_servis).grid(row=0, column=2, padx=(10, 0))
        ttk.Button(frame_cari, text="Tampilkan Semua", command=self.tampilkan_semua).grid(row=0, column=3, padx=(10, 0))
        
        # Frame tampilan data
        frame_data = ttk.LabelFrame(frame_utama, text="Data Servis", padding="10")
        frame_data.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        kolom = ('Plat', 'Merk', 'Tanggal', 'Jenis Servis')
        self.tree = ttk.Treeview(frame_data, columns=kolom, show='headings', height=10)
        for k in kolom:
            self.tree.heading(k, text=k)
            self.tree.column(k, width=150)
        
        scrollbar = ttk.Scrollbar(frame_data, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.tree.bind('<Double-1>', self.pilih_item)
        
        # Frame file
        frame_file = ttk.Frame(frame_utama)
        frame_file.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(frame_file, text="Simpan ke CSV", command=self.simpan_ke_csv).grid(row=0, column=0, padx=5)
        ttk.Button(frame_file, text="Muat dari CSV", command=self.muat_dari_csv).grid(row=0, column=1, padx=5)
        ttk.Button(frame_file, text="Ekspor CSV", command=self.ekspor_csv).grid(row=0, column=2, padx=5)
        ttk.Button(frame_file, text="Impor CSV", command=self.impor_csv).grid(row=0, column=3, padx=5)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame_utama.columnconfigure(1, weight=1)
        frame_utama.rowconfigure(3, weight=1)
        frame_data.columnconfigure(0, weight=1)
        frame_data.rowconfigure(0, weight=1)

    def bersihkan_input(self):
        """Bersihkan semua kolom input"""
        self.input_plat.delete(0, tk.END)
        self.input_merk.delete(0, tk.END)
        self.input_tanggal.delete(0, tk.END)
        self.input_jenis.delete(0, tk.END)
        self.input_tanggal.insert(0, datetime.now().strftime("%Y-%m-%d"))
    
    def validasi_input(self):
        """Validasi isian input"""
        if not self.input_plat.get().strip():
            messagebox.showerror("Error", "Plat nomor harus diisi!")
            return False
        if not self.input_merk.get().strip():
            messagebox.showerror("Error", "Merk kendaraan harus diisi!")
            return False
        if not self.input_tanggal.get().strip():
            messagebox.showerror("Error", "Tanggal servis harus diisi!")
            return False
        if not self.input_jenis.get().strip():
            messagebox.showerror("Error", "Jenis servis harus diisi!")
            return False
        try:
            datetime.strptime(self.input_tanggal.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Format tanggal harus YYYY-MM-DD!")
            return False
        return True
    
    def tambah_servis(self):
        """Tambah entri servis baru"""
        if not self.validasi_input():
            return
        plat = self.input_plat.get().strip().upper()
        entri = {
            "plat_nomor": plat,
            "merk_kendaraan": self.input_merk.get().strip(),
            "tanggal_servis": self.input_tanggal.get().strip(),
            "jenis_servis": self.input_jenis.get().strip()
        }
        self.daftar_servis.append(entri)
        self.peta_servis.setdefault(plat, []).append(entri)
        self.perbarui_tampilan()
        self.bersihkan_input()
        messagebox.showinfo("Sukses", "Data servis berhasil ditambahkan!")
    
    def ubah_servis(self):
        """Perbarui data servis yang dipilih"""
        pilihan = self.tree.selection()
        if not pilihan:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diperbarui!")
            return
        if not self.validasi_input():
            return
        indeks = self.tree.index(pilihan[0])
        data_lama = self.daftar_servis[indeks]
        plat_lama = data_lama["plat_nomor"]
        entri_baru = {
            "plat_nomor": self.input_plat.get().strip().upper(),
            "merk_kendaraan": self.input_merk.get().strip(),
            "tanggal_servis": self.input_tanggal.get().strip(),
            "jenis_servis": self.input_jenis.get().strip()
        }
        self.daftar_servis[indeks] = entri_baru
        self.peta_servis[plat_lama].remove(data_lama)
        if not self.peta_servis[plat_lama]:
            del self.peta_servis[plat_lama]
        self.peta_servis.setdefault(entri_baru["plat_nomor"], []).append(entri_baru)
        self.perbarui_tampilan()
        self.bersihkan_input()
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
    
    def hapus_servis(self):
        """Hapus data servis yang dipilih"""
        pilihan = self.tree.selection()
        if not pilihan:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus!")
            return
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?"):
            indeks = self.tree.index(pilihan[0])
            entri = self.daftar_servis.pop(indeks)
            self.peta_servis[entri["plat_nomor"]].remove(entri)
            if not self.peta_servis[entri["plat_nomor"]]:
                del self.peta_servis[entri["plat_nomor"]]
            self.perbarui_tampilan()
            self.bersihkan_input()
            messagebox.showinfo("Sukses", "Data berhasil dihapus!")

    def cari_servis(self):
        """Cari data servis berdasarkan plat nomor"""
        plat = self.input_cari.get().strip().upper()
        if not plat:
            messagebox.showwarning("Peringatan", "Masukkan plat nomor untuk pencarian!")
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        if plat in self.peta_servis:
            for entri in self.peta_servis[plat]:
                self.tree.insert('', 'end', values=(entri["plat_nomor"], entri["merk_kendaraan"],
                                                    entri["tanggal_servis"], entri["jenis_servis"]))
        else:
            messagebox.showinfo("Info", f"Tidak ditemukan data servis untuk plat: {plat}")

    def tampilkan_semua(self):
        """Tampilkan semua data servis"""
        self.perbarui_tampilan()
        self.input_cari.delete(0, tk.END)

    def perbarui_tampilan(self):
        """Perbarui tampilan data di tabel"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entri in self.daftar_servis:
            self.tree.insert('', 'end', values=(entri["plat_nomor"], entri["merk_kendaraan"],
                                                entri["tanggal_servis"], entri["jenis_servis"]))

    def pilih_item(self, event):
        """Isi kolom input saat item dipilih"""
        pilihan = self.tree.selection()
        if pilihan:
            nilai = self.tree.item(pilihan[0])['values']
            self.bersihkan_input()
            self.input_plat.insert(0, nilai[0])
            self.input_merk.insert(0, nilai[1])
            self.input_tanggal.insert(0, nilai[2])
            self.input_jenis.insert(0, nilai[3])

    def simpan_ke_csv(self):
        """Simpan data ke file CSV"""
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/servis.csv', 'w', newline='', encoding='utf-8') as f:
                penulis = csv.DictWriter(f, fieldnames=["plat_nomor", "merk_kendaraan", "tanggal_servis", "jenis_servis"])
                penulis.writeheader()
                for entri in self.daftar_servis:
                    penulis.writerow(entri)
            messagebox.showinfo("Sukses", "Data berhasil disimpan ke data/servis.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {str(e)}")

    def muat_dari_csv(self):
        """Muat data dari file CSV"""
        try:
            with open('data/servis.csv', 'r', encoding='utf-8') as f:
                pembaca = csv.DictReader(f)
                self.daftar_servis.clear()
                self.peta_servis.clear()
                for baris in pembaca:
                    self.daftar_servis.append(baris)
                    self.peta_servis.setdefault(baris["plat_nomor"], []).append(baris)
                self.perbarui_tampilan()
                messagebox.showinfo("Sukses", "Data berhasil dimuat dari data/servis.csv")
        except FileNotFoundError:
            messagebox.showinfo("Info", "File data/servis.csv tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {str(e)}")

    def ekspor_csv(self):
        """Ekspor data ke file CSV yang dipilih pengguna"""
        if not self.daftar_servis:
            messagebox.showwarning("Peringatan", "Tidak ada data untuk diekspor!")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    penulis = csv.DictWriter(f, fieldnames=["plat_nomor", "merk_kendaraan", "tanggal_servis", "jenis_servis"])
                    penulis.writeheader()
                    for entri in self.daftar_servis:
                        penulis.writerow(entri)
                messagebox.showinfo("Sukses", f"Data berhasil diekspor ke {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengekspor data: {str(e)}")

    def impor_csv(self):
        """Impor data dari file CSV"""
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    pembaca = csv.DictReader(f)
                    if self.daftar_servis:
                        ganti = messagebox.askyesno("Import Data", "Apakah Anda ingin mengganti data yang ada?")
                        if ganti:
                            self.daftar_servis.clear()
                            self.peta_servis.clear()
                    for baris in pembaca:
                        if all(k in baris and baris[k].strip() for k in ["plat_nomor", "merk_kendaraan", "tanggal_servis", "jenis_servis"]):
                            self.daftar_servis.append(baris)
                            self.peta_servis.setdefault(baris["plat_nomor"], []).append(baris)
                    self.perbarui_tampilan()
                    messagebox.showinfo("Sukses", f"Data berhasil diimpor dari {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal mengimpor data: {str(e)}")

def main():
    root = tk.Tk()
    app = AplikasiServisKendaraan(root)
    root.mainloop()

if __name__ == "__main__":
    main()
