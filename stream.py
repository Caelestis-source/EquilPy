class Stream:
    # Fungsi __init__ adalah konstruktor untuk membangun objek aliran baru
    def __init__(self, nama, T, P, flow_rate, komposisi):
        self.nama = nama
        self.T = T                  # Suhu operasi (Celcius)
        self.P = P                  # Tekanan operasi (kPa)
        self.flow_rate = flow_rate  # Total laju alir (kmol/jam)
        
        # Komposisi menggunakan struktur data Dictionary {'Komponen': fraksi_mol}
        self.komposisi = komposisi  
        
        # Validasi dasar Asas Teknik Kimia: Total fraksi mol harus = 1
        total_fraksi = sum(self.komposisi.values())
        if abs(total_fraksi - 1.0) > 1e-6: # Toleransi error kecil
            print(f"Peringatan: Total fraksi mol di stream '{self.nama}' tidak sama dengan 1!")

    # Fungsi/Metode untuk menampilkan status aliran
    def tampilkan_info(self):
        print(f"--- Data Aliran: {self.nama} ---")
        print(f"Suhu       : {self.T} °C")
        print(f"Tekanan    : {self.P} kPa")
        print(f"Laju Alir  : {self.flow_rate} kmol/h")
        print(f"Komposisi  : {self.komposisi}\n")