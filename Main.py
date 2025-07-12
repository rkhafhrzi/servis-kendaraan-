
import csv

# Struktur data
servis_list = []  # menggunakan list untuk semua data
servis_map = {}   # menggunakan hashmap (dict) untuk pencarian cepat

# Fungsi tambah servis
def tambah_servis():
    plat = input("Plat Nomor: ")
    merk = input("Merk Kendaraan: ")
    tanggal = input("Tanggal Servis (YYYY-MM-DD): ")
    jenis = input("Jenis Servis: ")
    
    entri = {
        "plat_nomor": plat,
        "merk_kendaraan": merk,
        "tanggal_servis": tanggal,
        "jenis_servis": jenis
    }
    
    servis_list.append(entri)
    
    if plat in servis_map:
        servis_map[plat].append(entri)
    else:
        servis_map[plat] = [entri]

    print("✅ Entri servis berhasil ditambahkan.")

# Fungsi cari servis
def cari_servis():
    plat = input("Masukkan plat nomor: ")
    if plat in servis_map:
        print(f"Data servis untuk {plat}:")
        for data in servis_map[plat]:
            print(data)
    else:
        print("❌ Data tidak ditemukan.")

# Fungsi tampilkan semua servis
def tampilkan_semua():
    print("📋 Semua Data Servis:")
    for entri in servis_list:
        print(entri)

# Fungsi simpan ke file CSV
def simpan_ke_csv():
    with open('data/servis.csv', 'w', newline='') as file:
        fieldnames = ["plat_nomor", "merk_kendaraan", "tanggal_servis", "jenis_servis"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entri in servis_list:
            writer.writerow(entri)
    print("💾 Data berhasil disimpan ke servis.csv")

# Fungsi muat dari CSV
def muat_dari_csv():
    try:
        with open('data/servis.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                servis_list.append(row)
                plat = row["plat_nomor"]
                if plat in servis_map:
                    servis_map[plat].append(row)
                else:
                    servis_map[plat] = [row]
        print("📂 Data berhasil dimuat dari servis.csv")
    except FileNotFoundError:
        print("⚠️ File servis.csv belum ditemukan. Mulai dengan data kosong.")

# Main loop
def menu():
    muat_dari_csv()
    while True:
        print("\n=== Sistem Servis Kendaraan ===")
        print("1. Tambah Entri Servis")
        print("2. Cari Servis berdasarkan Plat Nomor")
        print("3. Tampilkan Semua Servis")
        print("4. Simpan dan Keluar")
        
        pilihan = input("Pilih menu (1-4): ")
        if pilihan == "1":
            tambah_servis()
        elif pilihan == "2":
            cari_servis()
        elif pilihan == "3":
            tampilkan_semua()
        elif pilihan == "4":
            simpan_ke_csv()
            break
        else:
            print("❌ Pilihan tidak valid.")

if __name__ == "__main__":
    menu()
