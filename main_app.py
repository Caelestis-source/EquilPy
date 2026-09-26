import sys
import io
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QFormLayout, QLineEdit, QPushButton, 
                             QTextEdit, QComboBox)

# Import modul yang sudah dipecah
from db_handler import get_databases
from stream import Stream
from units import FlashDrum

# Panggil database sekali saat aplikasi mulai
df_komponen, df_interaksi = get_databases('properties.db')

class SimulatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flash Drum Simulator")
        self.resize(500, 600)
        
        layout_utama = QVBoxLayout()
        layout_form = QFormLayout()
        
        self.combo_k1 = QComboBox()
        self.combo_k2 = QComboBox()
        
        daftar_komponen = df_komponen['nama_komponen'].tolist()
        self.combo_k1.addItems(daftar_komponen)
        self.combo_k2.addItems(daftar_komponen)
        
        if "Etanol" in daftar_komponen: self.combo_k1.setCurrentText("Etanol")
        if "Air" in daftar_komponen: self.combo_k2.setCurrentText("Air")
        
        self.input_T = QLineEdit("92.0")
        self.input_P = QLineEdit("101.325")
        self.input_F = QLineEdit("100.0")
        self.input_z1 = QLineEdit("0.3") 
        
        layout_form.addRow("Komponen 1 (Lebih Volatil):", self.combo_k1)
        layout_form.addRow("Komponen 2 (Kurang Volatil):", self.combo_k2)
        layout_form.addRow("Suhu Operasi (°C):", self.input_T)
        layout_form.addRow("Tekanan (kPa):", self.input_P)
        layout_form.addRow("Laju Alir (kmol/h):", self.input_F)
        layout_form.addRow("Fraksi Mol Komp. 1:", self.input_z1)
        
        self.btn_ideal = QPushButton("Simulasi Ideal (Raoult)")
        self.btn_nonideal = QPushButton("Simulasi Non-Ideal (Van Laar)")
        
        self.layar_output = QTextEdit()
        self.layar_output.setReadOnly(True)
        
        layout_utama.addLayout(layout_form)
        layout_utama.addWidget(self.btn_ideal)
        layout_utama.addWidget(self.btn_nonideal)
        layout_utama.addWidget(self.layar_output)
        
        self.setLayout(layout_utama)
        
        self.btn_ideal.clicked.connect(lambda: self.jalankan_simulasi(ideal=True))
        self.btn_nonideal.clicked.connect(lambda: self.jalankan_simulasi(ideal=False))

    def jalankan_simulasi(self, ideal):
        self.layar_output.clear()
        try:
            k1 = self.combo_k1.currentText()
            k2 = self.combo_k2.currentText()
            
            if k1 == k2:
                self.layar_output.setText("ERROR: Komponen 1 dan Komponen 2 tidak boleh sama!")
                return
                
            T_op = float(self.input_T.text())
            P_op = float(self.input_P.text())
            F_op = float(self.input_F.text())
            z1 = float(self.input_z1.text())
            z2 = 1.0 - z1
            
            feed = Stream("Feed GUI", T_op, P_op, F_op, {k1: z1, k2: z2})
            
            unit = FlashDrum(feed, df_komponen, df_interaksi)
            
            output_tangkap = io.StringIO()
            sys.stdout = output_tangkap
            
            unit.selesaikan_neraca(ideal=ideal)
            
            sys.stdout = sys.__stdout__
            self.layar_output.setText(output_tangkap.getvalue())
            
        except ValueError:
            self.layar_output.setText("ERROR: Pastikan seluruh kotak input terisi angka yang valid!")
        except Exception as e:
            self.layar_output.setText(f"ERROR SISTEM:\n{str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    jendela = SimulatorApp()
    jendela.show()
    sys.exit(app.exec())