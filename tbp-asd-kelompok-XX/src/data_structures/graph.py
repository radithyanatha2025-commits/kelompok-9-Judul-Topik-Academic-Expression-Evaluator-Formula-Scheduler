from typing import Dict, List, Set, Optional
from collections import deque

# Import dari modul lain (asumsi sudah ada)
from modul1_stack import infix_to_postfix, FUNCS
from modul4_expr_tree import build_expr_tree, eval_tree, ExprNode

def tokenize(expr: str) -> List[str]:
    """Memecah ekspresi menjadi token-token"""
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or (ch == '.' and i+1 < n and expr[i+1].isdigit()):
            j = i
            while j < n and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue
        if ch.isalpha():
            j = i
            while j < n and expr[j].isalpha():
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue
        if ch in '+-*/^()':
            tokens.append(ch)
            i += 1
            continue
        raise ValueError(f"Karakter tidak dikenal: '{ch}'")
    return tokens


class FormulaDAG:
    """
    Directed Acyclic Graph (DAG) untuk manajemen dependensi formula.
    
    Contoh:
        Formula A = B + C  (A bergantung pada B dan C)
        Formula B = D * 2   (B bergantung pada D)
        
        Maka graph:
            D → B → A
            C → A
    
    Aturan:
        - Node = nama formula
        - Edge X → Y berarti Y bergantung pada X
        - Graph harus DAG (tidak boleh ada siklus)
    """
    
    def __init__(self):
        # ========== STRUKTUR DATA GRAPH ==========
        self.graph: Dict[str, List[str]] = {}    # Adjacency list
        self.formulas: Dict[str, str] = {}       # Node → ekspresi
        self.trees: Dict[str, ExprNode] = {}     # Node → expression tree
        # =========================================
    
    def _extract_dependencies(self, expr: str) -> Set[str]:
        """
        Ekstrak semua dependensi (variabel/formula) dari sebuah ekspresi.
        
        Contoh:
            expr = "v^2 * sin(2*rad) / g"
            return = {'v', 'rad', 'g'}
        
        Big-O: O(m) di mana m = jumlah token
        """
        tokens = tokenize(expr)
        deps = set()
        
        for tok in tokens:
            # Lewati fungsi bawaan (sin, cos, dll)
            if tok in FUNCS:
                continue
            
            # Lewati angka (bisa di-parse ke float)
            try:
                float(tok)
                continue
            except ValueError:
                pass
            
            # Jika token adalah huruf (variabel/formula), tambahkan sebagai dependensi
            if tok.isalpha():
                deps.add(tok)
        
        return deps
    
    def define(self, name: str, expr: str) -> None:
        """
        Mendefinisikan formula baru dan menambahkannya ke graph.
        
        Proses:
            1. Validasi ekspresi (build tree)
            2. Ekstrak dependensi
            3. Tambahkan node dan edge ke graph
            4. Cek apakah masih DAG (tidak ada siklus)
        
        Contoh:
            dag.define('jarak', '(v^2 * sin(2*rad)) / g')
        
        Args:
            name: Nama formula (node)
            expr: Ekspresi matematika dalam string
        
        Raises:
            ValueError: Jika terjadi siklus dependensi
        """
        print(f"\n[DEBUG] Mendefinisikan formula: {name} = {expr}")
        
        # ========== STEP 1: Validasi Ekspresi ==========
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        tree = build_expr_tree(postfix)
        print(f"  → Ekspresi valid, tree berhasil dibangun")
        
        # ========== STEP 2: Ekstrak Dependensi ==========
        deps = self._extract_dependencies(expr)
        deps.discard(name)  # Hapus self-dependency jika ada
        print(f"  → Dependensi ditemukan: {deps if deps else 'tidak ada'}")
        
        # ========== STEP 3: Simpan Formula ==========
        self.formulas[name] = expr
        self.trees[name] = tree
        
        # ========== STEP 4: Tambahkan Edge ke Graph ==========
        # Edge: dep → name (name bergantung pada dep)
        for dep in deps:
            if dep in self.formulas:
                self.graph.setdefault(dep, []).append(name)
                print(f"  → Edge: {dep} → {name}")
        
        # Pastikan node memiliki entry di graph (untuk node tanpa dependensi)
        self.graph.setdefault(name, [])
        
        # ========== STEP 5: Cek Siklus (Validasi DAG) ==========
        try:
            order = self.topological_sort()
            print(f"  → Urutan evaluasi: {' → '.join(order)}")
            print(f"  → Formula '{name}' berhasil ditambahkan (DAG valid)")
        except ValueError as e:
            # Rollback jika terjadi siklus
            del self.formulas[name]
            del self.trees[name]
            for dep in deps:
                if dep in self.graph and name in self.graph.get(dep, []):
                    self.graph[dep].remove(name)
            if name in self.graph:
                del self.graph[name]
            raise ValueError(f"Siklus terdeteksi: {e}")
    
    def topological_sort(self) -> List[str]:
        """
        Topological Sort menggunakan algoritma Kahn (BFS).
        
        Prinsip:
            1. Hitung in-degree (jumlah edge yang masuk) setiap node
            2. Masukkan node dengan in-degree = 0 ke queue
            3. Keluarkan node dari queue, kurangi in-degree tetangganya
            4. Ulangi hingga queue kosong
        
        Returns:
            List node dalam urutan evaluasi yang valid
        
        Raises:
            ValueError: Jika ada siklus (graph bukan DAG)
        
        Big-O: O(V + E)
        
        Contoh:
            Graph: D → B → A
                   C → A
            
            In-degree: A=2, B=1, C=0, D=0
            Queue awal: [C, D]
            
            Step 1: ambil C → order=[C], kurangi in-degree A=1
            Step 2: ambil D → order=[C,D], kurangi in-degree B=0
            Step 3: ambil B → order=[C,D,B], kurangi in-degree A=0
            Step 4: ambil A → order=[C,D,B,A]
        """
        nodes = set(self.formulas.keys())
        
        if not nodes:
            return []
        print(f"\n[DEBUG] Topological Sort pada {len(nodes)} node")
        # ========== STEP 1: Hitung In-Degree ==========
        in_degree = {n: 0 for n in nodes}
        
        for u in nodes:
            for v in self.graph.get(u, []):
                if v in nodes:
                    in_degree[v] += 1
        
        print(f"  → In-degree: {in_degree}")
        # ========== STEP 2: Inisialisasi Queue ==========
        q = deque([n for n in nodes if in_degree[n] == 0])
        print(f"  → Queue awal (in-degree 0): {list(q)}")
        # ========== STEP 3: Proses Queue ==========
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            print(f"  → Mengeluarkan '{u}' dari queue, order: {order}")
            
            for v in self.graph.get(u, []):
                if v in nodes:
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        q.append(v)
                        print(f"    → '{v}' in-degree menjadi 0, masuk queue")
        # ========== STEP 4: Deteksi Siklus ==========
        if len(order) != len(nodes):
            remaining = nodes - set(order)
            raise ValueError(f"Siklus terdeteksi pada node: {remaining}")
        print(f"  → Topological sort selesai: {order}")
        return order
    def evaluate_one(self, name: str, var_table: Dict[str, float]) -> float:
        """
        Mengevaluasi satu formula beserta semua dependensinya.
        Proses:
            1. Lakukan topological sort untuk urutan evaluasi
            2. Evaluasi formula sesuai urutan, simpan hasil di memory
        Args:
            name: Nama formula yang akan dievaluasi
            var_table: Tabel variabel dari user (BST)
        Returns:
            Hasil evaluasi formula
        
        Big-O: O(V + E) untuk sort + O(n) untuk evaluasi tree
        """
        print(f"\n[DEBUG] Evaluasi formula: {name}")
        # Dapatkan urutan evaluasi
        order = self.topological_sort()
        print(f"  → Urutan evaluasi: {order}")
        # Dictionary untuk menyimpan hasil antar formula
        results = {}
        # Evaluasi setiap formula sesuai urutan
        for f in order:
            # Gabungkan variabel user dengan hasil formula sebelumnya
            local_table = {**var_table, **results}
            # Evaluasi expression tree
            value = eval_tree(self.trees[f], local_table)
            results[f] = value
            print(f"  → {f} = {value}")
        return results[name]
    def get_dependencies(self, name: str) -> List[str]:
        """
        Mendapatkan daftar dependensi dari suatu formula.
        (Edge yang masuk ke node tersebut)
        """
        deps = []
        for dep, targets in self.graph.items():
            if name in targets:
                deps.append(dep)
        return deps
    def get_dependents(self, name: str) -> List[str]:
        """
        Mendapatkan daftar formula yang bergantung pada suatu formula.
        (Edge yang keluar dari node tersebut)
        """
        return self.graph.get(name, [])
    def show_graph(self) -> None:
        """Menampilkan struktur graph"""
        print("\n" + "="*50)
        print("STRUKTUR GRAPH (DAG)")
        print("="*50)
        if not self.formulas:
            print("Tidak ada formula.")
            return
        for node in self.formulas:
            deps = self.get_dependencies(node)
            deps_str = ", ".join(deps) if deps else "(tidak ada)"
            print(f"  {node} = {self.formulas[node]}")
            print(f"    ← bergantung pada: {deps_str}")
            print()
    def is_valid_dag(self) -> bool:
        """Memeriksa apakah graph adalah DAG yang valid"""
        try:
            self.topological_sort()
            return True
        except ValueError:
            return False
# =============================================================================
# CONTOH PENGGUNAAN
# =============================================================================
if __name__ == "__main__":
    print("="*70)
    print(" CONTOH PENGGUNAAN GRAPH DAG")
    print("="*70)
    # Buat instance DAG
    dag = FormulaDAG()
    # Definisikan beberapa formula
    print("\n--- Mendefinisikan Formula ---")
    dag.define('rad', 't * 3.141592653589793 / 180')
    dag.define('jarak', '(v^2 * sin(2*rad)) / g')
    dag.define('waktu', 'v * sin(rad) / g')
    dag.define('tinggi', 'v * sin(rad) * waktu - 0.5 * g * waktu^2')
    # Tampilkan struktur graph
    dag.show_graph()
    # Siapkan tabel variabel
    var_table = {'v': 25.0, 'g': 9.81, 't': 45.0}
    # Evaluasi formula
    print("\n--- Evaluasi Formula ---")
    hasil = dag.evaluate_one('jarak', var_table)
    print(f"\nHasil akhir jarak = {hasil:.2f} meter")
    # Coba buat siklus (akan error)
    print("\n--- Deteksi Siklus ---")
    try:
        dag.define('siklus_a', 'siklus_b + 1')
        dag.define('siklus_b', 'siklus_a + 1')
    except ValueError as e:
        print(f"Error: {e}")
