KELOMPOK-9_Academic-Expression-Evaluator-Formula-Scheduler
topik 5 Academic Expression Evaluator & Formula Scheduler
Team
1.	Radithya natha syandana_25051030042
2.	Aruf Abidzar Atthohiri_25051030047
3.	Ragil Anam Winarya_25051030053
4.	M Brian Endra Nata Safit_25051030056

________________________________________
Mata Kuliah
Algoritma dan Struktur Data
S1 Teknik Elektro
Universitas Negeri Yogyakarta
________________________________________
# Deskripsi Project
Project ini merupakan pengembangan sistem cerdas berbasis Python yang dirancang untuk melakukan evaluasi ekspresi akademik serta pengelolaan jadwal formula secara efisien dengan menerapkan konsep Algoritma dan Struktur Data.

Sistem ini bertujuan membantu mahasiswa maupun pengguna dalam menyelesaikan berbagai kebutuhan akademik, seperti:
- melakukan evaluasi ekspresi matematika secara otomatis
- mengonversi bentuk ekspresi matematika
- menyimpan dan mengelola formula akademik
- mengatur jadwal penggunaan rumus dan tugas
- memantau riwayat evaluasi dan aktivitas pengguna
- memberikan pengingat deadline tugas akademik

Dengan memanfaatkan berbagai struktur data seperti Stack, Queue, Linked List, BST, Priority Queue, dan Graph, sistem mampu memberikan proses pengolahan data yang lebih cepat, terstruktur, dan optimal.
________________________________________
Struktur Data yang Digunakan
Project ini menggunakan beberapa struktur data utama, yaitu:
•	Stack 
o	Digunakan untuk evaluasi ekspresi matematika (infix, postfix, prefix). 
•	Queue 
o	Mengatur antrean proses evaluasi formula. 
•	Linked List 
o	Menyimpan riwayat perhitungan pengguna. 
•	Binary Search Tree (BST) 
o	Mengelola penyimpanan dan pencarian formula akademik. 
•	Priority Queue 
o	Mengatur prioritas jadwal tugas atau formula berdasarkan deadline. 
•	Graph 
o	Merepresentasikan hubungan antar topik atau formula pembelajaran. 
________________________________________
Fitur Program
No	Fitur	Keterangan
1	Evaluasi ekspresi matematika	Mendukung infix, postfix, prefix
2	Konversi infix ↔ postfix/prefix	Menggunakan algoritma Shunting-yard
3	Penyimpanan formula akademik	BST dengan nama formula sebagai key
4	Pencarian formula cepat	BST search O(log n)
5	Penjadwalan tugas akademik	Priority Queue berdasarkan deadline
6	Pengingat deadline tugas	Notifikasi tugas dengan prioritas tertinggi
7	Riwayat perhitungan pengguna	Doubly Linked List dengan timestamp
8	Laporan aktivitas evaluasi formula	Ekspor ke file teks/CSV
9	Antrean proses evaluasi	Queue untuk batch processing
10	Topik pembelajaran dependency	Graph + DFS/BFS traversal
11	Tambahan: Undo/redo riwayat	Stack untuk navigasi history
12	Tambahan: Visualisasi dependency	Graph dengan matplotlib (opsional)
________________________________________
Struktur Folder
KELOMPOK-9_Academic-Expression-Evaluator-Formula-Scheduler/
│
├── docs/                                    # laporan dan slide presentasi
│   ├── Laporan_Proyek.pdf
│   ├── Slide_Presentasi.pptx
│   ├── Flowchart_Diagram.pdf
│   ├── UML_Diagram.pdf
│   └── Analisis_Kompleksitas.pdf
│
├── src/                                     # source code utama
│   ├── main.py                              # entry point program
│   ├── stack_evaluator.py                   # Stack untuk evaluasi & konversi ekspresi
│   ├── queue_processor.py                   # Queue untuk antrean evaluasi
│   ├── linked_list_history.py               # Doubly Linked List untuk riwayat
│   ├── bst_formula.py                       # BST untuk penyimpanan formula
│   ├── priority_queue_scheduler.py          # Priority Queue untuk penjadwalan tugas
│   ├── graph_topics.py                      # Graph untuk hubungan antar topik
│   ├── formula.py                           # Class Formula
│   ├── task.py                              # Class Task (tugas akademik)
│   ├── history_node.py                      # Class Node untuk Linked List
│   └── utils.py                             # Fungsi bantu & visualisasi
│
├── tests/                                   # pengujian program
│   ├── test_stack.py
│   ├── test_queue.py
│   ├── test_linked_list.py
│   ├── test_bst.py
│   ├── test_priority_queue.py
│   ├── test_graph.py
│   └── test_integration.py
│
├── experiments/                             # eksperimen dan analisis
│   ├── kompleksitas_waktu.md
│   ├── benchmark_evaluasi.csv
│   ├── analisis_performa.ipynb
│   └── simulasi_jadwal.py
│
├── data/                                    # data penyimpanan
│   ├── formulas.json                        # database formula akademik
│   ├── tasks.json                           # database tugas
│   ├── topics.json                          # data dependency topik
│   └── history.log                          # riwayat perhitungan
│
├── requirements.txt                         # dependensi Python
└── README.md                                # panduan singkat


