# Simulasi Pemungutan Suara dengan Metode Tideman
Terdapat 2 program 
1. tideman.py
   Program ini digunakan untuk menentukan pemenang dari suatu pemungutan suara, di mana kandidat dan suara masing-masing pemilih terdapat dalam file input csv.
   Contoh penggunaan : python tideman.py <namaFile.csv>
2. visualisasi_tideman.py
   Program ini digunakan untuk memvisualiasikan directed acyclic graph yang terbentuk berdasarkan hasil pemungutan suara pada program tideman.py.
   Oleh karena itu, untuk menjalankan program ini, perlu untuk menjalakan tideman.py terlebih dahulu
   Contoh penggunaan : python visualisasi_tideman.py
Selain itu, terdapat CSV file yang menjadi input dari tideman.py
Format CSV File:
  Baris 1 : Nama-nama kandidat
  Baris 2 dan seterusnya : Preferensi masing-masing pemilih berdasarkan kandidat yang ada
