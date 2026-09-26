import numpy as np
from stream import Stream

class FlashDrum:
    # 1. Update __init__ untuk menerima df_interaksi
    def __init__(self, feed_stream, df_database, df_interaksi):
        self.feed = feed_stream  
        self.db = df_database    
        self.db_interaksi = df_interaksi # Menangkap dataframe Van Laar
        
        self.vapor_stream = None
        self.liquid_stream = None
        
    def hitung_Psat(self):
        print(f"Menghitung Tekanan Uap Murni pada T = {self.feed.T} °C...")
        P_sat = {}
        for komponen in self.feed.komposisi.keys():
            data = self.db.loc[self.db['nama_komponen'] == komponen].iloc[0]
            A, B, C = data['A'], data['B'], data['C']
            Psat_val = np.exp(A - (B / (self.feed.T + C)))
            P_sat[komponen] = Psat_val
            print(f"Psat {komponen}: {Psat_val:.3f} {data['satuan_P']}")
        return P_sat
    
    # 2. Update algoritma pencarian matriks Van Laar via Pandas
    def hitung_gamma_van_laar(self, k1, k2, x1_val, x2_val):
        
        # Mencari konfigurasi A-B
        match1 = self.db_interaksi[(self.db_interaksi['komponen_1'] == k1) & 
                                   (self.db_interaksi['komponen_2'] == k2)]
        # Mencari konfigurasi B-A (jika urutan dibalik)
        match2 = self.db_interaksi[(self.db_interaksi['komponen_1'] == k2) & 
                                   (self.db_interaksi['komponen_2'] == k1)]
        
        if not match1.empty:
            A12 = match1.iloc[0]['A12']
            A21 = match1.iloc[0]['A21']
        elif not match2.empty:
            # Jika tabel berisi A-B tapi user mencari B-A, balik nilai A12 dan A21
            A12 = match2.iloc[0]['A21']
            A21 = match2.iloc[0]['A12']
        else:
            A12, A21 = 0.0, 0.0 # Asumsi ideal jika pasangan tidak ada di database
        
        x1 = max(x1_val, 1e-10)
        x2 = max(x2_val, 1e-10)
        
        g1 = np.exp(A12 / (1 + (A12 * x1) / (A21 * x2))**2) if A12 != 0 else 1.0
        g2 = np.exp(A21 / (1 + (A21 * x2) / (A12 * x1))**2) if A21 != 0 else 1.0
        
        return g1, g2
        
    def selesaikan_neraca(self, ideal=True):
        P_sat = self.hitung_Psat()
        
        # Mengekstrak nama komponen secara otomatis dari Feed
        daftar_komp = list(self.feed.komposisi.keys())
        k1 = daftar_komp[0]
        k2 = daftar_komp[1]
        
        # Inisialisasi tebakan awal komposisi cair secara dinamis
        x_aktual = {k: self.feed.komposisi.get(k, 0.0) for k in daftar_komp}
        
        for iterasi_outer in range(50):
            
            # Kalkulasi Koefisien Aktivitas (Gamma)
            if ideal:
                gamma = {k1: 1.0, k2: 1.0}
            else:
                g1, g2 = self.hitung_gamma_van_laar(k1, k2, x_aktual[k1], x_aktual[k2])
                gamma = {k1: g1, k2: g2}
                
            K = {}
            for komp in daftar_komp:
                K[komp] = (gamma[komp] * P_sat[komp]) / self.feed.P
                
            def rachford_rice(VF):
                sigma = 0
                for komp, z_i in self.feed.komposisi.items():
                    sigma += (z_i * (K[komp] - 1)) / (1 + VF * (K[komp] - 1))
                return sigma
                
            batas_bawah = 0.0
            batas_atas = 1.0
            
            if rachford_rice(batas_bawah) < 0 or rachford_rice(batas_atas) > 0:
                print(f"\n[Mode Ideal={ideal}] PERINGATAN: Di luar kesetimbangan dua fasa.")
                return None
                
            for iterasi_inner in range(100):
                VF_tebakan = (batas_bawah + batas_atas) / 2
                error_rr = rachford_rice(VF_tebakan)
                
                if abs(error_rr) < 1e-6:
                    break
                elif rachford_rice(batas_bawah) * error_rr < 0:
                    batas_atas = VF_tebakan
                else:
                    batas_bawah = VF_tebakan
                    
            VF_final = (batas_bawah + batas_atas) / 2
            
            x_baru = {}
            for komp, z_i in self.feed.komposisi.items():
                x_baru[komp] = z_i / (1 + VF_final * (K[komp] - 1))
                
            # Evaluasi error berbasis komponen pertama secara dinamis
            error_x = abs(x_baru[k1] - x_aktual[k1])
            x_aktual = x_baru  
            
            if ideal or error_x < 1e-5:
                break 
                
        # --- PERHITUNGAN FINAL ---
        V = VF_final * self.feed.flow_rate
        L = self.feed.flow_rate - V
        y = {k: K[k] * v for k, v in x_aktual.items()}
        
        # Cetak Hasil
        tipe = "IDEAL (HUKUM RAOULT)" if ideal else "NON-IDEAL (VAN LAAR)"
        print(f"\n--- HASIL SIMULASI: {tipe} ---")
        print(f"Fraksi Uap (V/F)   : {VF_final:.4f}")
        print(f"Laju Uap (V)       : {V:.2f} kmol/h")
        print(f"Laju Cair (L)      : {L:.2f} kmol/h")
        
        # Mencetak Gamma dan Komposisi secara dinamis
        if not ideal:
            print(f"\nKoefisien Aktivitas (Gamma):")
            for k, v in gamma.items(): print(f" - {k}: {v:.4f}")
            
        print("\nKomposisi Cairan (x):")
        for k, v in x_aktual.items(): print(f" - {k}: {v:.4f}")
        print("Komposisi Uap (y):")
        for k, v in y.items(): print(f" - {k}: {v:.4f}")
        print("-" * 35)