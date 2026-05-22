from typing import Dict, List, Set, Optional

# =============================================================================
# KONSTANTA UNTUK DFS TOPOLOGICAL SORT
# =============================================================================
WHITE = 0  # Belum dikunjungi
GRAY = 1   # Sedang dikunjungi (masih di stack rekursif)
BLACK = 2  # Sudah selesai dikunjungi


class FormulaDAG:
    """
    Directed Acyclic Graph (DAG) untuk manajemen dependensi formula.
    Implementasi murni tanpa Queue - menggunakan DFS recursion stack.
    
    Contoh penggunaan:
        dag = FormulaDAG()
        dag.add_node('jarak', '(v^2 * sin(2*rad)) / g')
        dag.add_node('rad', 'theta * pi / 180')
        dag.add_edge('rad', 'jarak')      # jarak bergantung pada rad
        order = dag.topological_sort()    # ['rad', 'jarak']
    """
    
    def __init__(self):
        """Inisialisasi graph kosong"""
        self.adjacency_list: Dict[str, List[str]] = {}    # Adjacency list
        self.node_data: Dict[str, str] = {}               # Data tiap node (formula)
    
    # ========== OPERASI DASAR GRAPH ==========
    
    def add_node(self, node: str, data: str = "") -> None:
        """
        Menambahkan node baru ke graph.
        
        Args:
            node: Nama node (identifier)
            data: Data yang terkait dengan node (misal ekspresi formula)
        """
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            self.node_data[node] = data
    
    def add_edge(self, from_node: str, to_node: str) -> None:
        """
        Menambahkan edge dari from_node ke to_node.
        Edge A → B berarti B bergantung pada A.
        
        Args:
            from_node: Node sumber (dependensi)
            to_node: Node tujuan (yang bergantung)
        
        Raises:
            ValueError: Jika node tidak ditemukan
        """
        if from_node not in self.adjacency_list:
            raise ValueError(f"Node '{from_node}' tidak ditemukan")
        if to_node not in self.adjacency_list:
            raise ValueError(f"Node '{to_node}' tidak ditemukan")
        
        self.adjacency_list[from_node].append(to_node)
    
    def remove_node(self, node: str) -> None:
        """
        Menghapus node dan semua edge yang terhubung.
        """
        if node in self.adjacency_list:
            del self.adjacency_list[node]
        
        # Hapus edge yang mengarah ke node ini
        for u in self.adjacency_list:
            if node in self.adjacency_list[u]:
                self.adjacency_list[u].remove(node)
        
        if node in self.node_data:
            del self.node_data[node]
    
    def remove_edge(self, from_node: str, to_node: str) -> None:
        """
        Menghapus edge dari from_node ke to_node.
        """
        if from_node in self.adjacency_list:
            if to_node in self.adjacency_list[from_node]:
                self.adjacency_list[from_node].remove(to_node)
    
    def get_neighbors(self, node: str) -> List[str]:
        """
        Mendapatkan semua tetangga (dependen) dari suatu node.
        """
        return self.adjacency_list.get(node, [])
    
    def get_predecessors(self, node: str) -> List[str]:
        """
        Mendapatkan semua node yang memiliki edge ke node ini (dependensi).
        """
        predecessors = []
        for u, neighbors in self.adjacency_list.items():
            if node in neighbors:
                predecessors.append(u)
        return predecessors
    
    # ========== TOPOLOGICAL SORT (DFS - TANPA QUEUE) ==========
    
    def topological_sort(self) -> List[str]:
        """
        Topological Sort menggunakan DFS (Depth-First Search).
        Tanpa Queue - menggunakan recursion stack dan 3 warna.
        
        Algoritma:
            1. Lakukan DFS pada setiap node
            2. Node yang sudah selesai diproses ditambahkan ke stack
            3. Hasil akhir adalah stack yang dibalik
        
        Returns:
            List node dalam urutan topological (dependensi terlebih dahulu)
        
        Raises:
            ValueError: Jika terdeteksi siklus (graph bukan DAG)
        
        Big-O: O(V + E)
        """
        nodes = list(self.adjacency_list.keys())
        state = {node: WHITE for node in nodes}
        result = []
        
        def dfs(node: str):
            """
            DFS rekursif untuk topological sort.
            Mengembalikan True jika tidak ada siklus.
            """
            state[node] = GRAY  # Sedang diproses
            
            for neighbor in self.adjacency_list[node]:
                if state[neighbor] == WHITE:
                    dfs(neighbor)
                elif state[neighbor] == GRAY:
                    # Mendeteksi back edge → ada siklus!
                    raise ValueError(f"Siklus terdeteksi: node '{neighbor}' sudah ada di stack")
            
            state[node] = BLACK  # Selesai diproses
            result.append(node)  # Tambahkan ke hasil
        
        for node in nodes:
            if state[node] == WHITE:
                dfs(node)
        
        # Balik hasil (karena kita menambahkan setelah selesai)
        return result[::-1]
    
    # ========== DETEKSI SIKLUS (CYCLE DETECTION) ==========
    
    def has_cycle(self) -> bool:
        """
        Memeriksa apakah graph memiliki siklus.
        
        Returns:
            True jika ada siklus, False jika DAG valid
        """
        try:
            self.topological_sort()
            return False
        except ValueError:
            return True
    
    def find_cycle(self) -> Optional[List[str]]:
        """
        Mencari siklus dalam graph.
        
        Returns:
            List node yang membentuk siklus, atau None jika tidak ada siklus
        """
        nodes = list(self.adjacency_list.keys())
        state = {node: WHITE for node in nodes}
        parent = {node: None for node in nodes}
        cycle = []
        
        def dfs_find_cycle(node: str) -> bool:
            state[node] = GRAY
            
            for neighbor in self.adjacency_list[node]:
                if state[neighbor] == WHITE:
                    parent[neighbor] = node
                    if dfs_find_cycle(neighbor):
                        return True
                elif state[neighbor] == GRAY:
                    # Siklus ditemukan
                    curr = node
                    while curr != neighbor:
                        cycle.append(curr)
                        curr = parent[curr]
                    cycle.append(neighbor)
                    cycle.append(node)
                    return True
            
            state[node] = BLACK
            return False
        
        for node in nodes:
            if state[node] == WHITE:
                if dfs_find_cycle(node):
                    return cycle[::-1]
        
        return None
    
    # ========== OPERASI FORMULA (INTEGRASI DENGAN FORMULA) ==========
    
    def define_formula(self, name: str, expr: str, dependencies: List[str]) -> None:
        """
        Mendefinisikan formula dengan dependensinya.
        
        Args:
            name: Nama formula (node)
            expr: Ekspresi formula
            dependencies: Daftar node yang menjadi dependensi
        
        Raises:
            ValueError: Jika definisi menyebabkan siklus
        """
        # Simpan data formula
        self.add_node(name, expr)
        
        # Tambahkan edge dari setiap dependensi ke formula ini
        for dep in dependencies:
            if dep in self.adjacency_list:
                self.add_edge(dep, name)
            else:
                # Jika dependensi belum ada, buat node kosong dulu
                self.add_node(dep, "")
                self.add_edge(dep, name)
        
        # Validasi: cek apakah masih DAG
        if self.has_cycle():
            # Rollback jika menyebabkan siklus
            self.remove_node(name)
            raise ValueError(f"Definisi '{name}' menyebabkan siklus dependensi")
    
    def get_evaluation_order(self, target_node: str) -> List[str]:
        """
        Mendapatkan urutan evaluasi untuk mencapai target node.
        Hanya node yang diperlukan (relevant nodes).
        
        Returns:
            List node dalam urutan evaluasi (dependensi terlebih dahulu)
        """
        # Dapatkan semua node yang diperlukan (reachable dari target)
        needed_nodes = set()
        
        def collect_dependencies(node: str):
            needed_nodes.add(node)
            for pred in self.get_predecessors(node):
                if pred not in needed_nodes:
                    collect_dependencies(pred)
        
        collect_dependencies(target_node)
        
        # Buat subgraph dari node yang diperlukan
        subgraph_nodes = [n for n in self.adjacency_list.keys() if n in needed_nodes]
        
        # Lakukan topological sort pada subgraph
        temp_state = {n: WHITE for n in subgraph_nodes}
        result = []
        
        def dfs_sub(node: str):
            temp_state[node] = GRAY
            for neighbor in self.adjacency_list[node]:
                if neighbor in temp_state:
                    if temp_state[neighbor] == WHITE:
                        dfs_sub(neighbor)
                    elif temp_state[neighbor] == GRAY:
                        raise ValueError(f"Siklus terdeteksi")
            temp_state[node] = BLACK
            result.append(node)
        
        for node in subgraph_nodes:
            if temp_state[node] == WHITE:
                dfs_sub(node)
        
        return result[::-1]
    
    # ========== VISUALISASI GRAPH ==========
    
    def display(self) -> None:
        """
        Menampilkan struktur graph secara visual.
        """
        print("\n" + "="*60)
        print("STRUKTUR GRAPH DAG")
        print("="*60)
        
        if not self.adjacency_list:
            print("Graph kosong.")
            return
        
        for node, neighbors in self.adjacency_list.items():
            data_info = f" = {self.node_data[node]}" if self.node_data[node] else ""
            print(f"\n📌 {node}{data_info}")
            
            if neighbors:
                print(f"   → dependen dari: {', '.join(neighbors)}")
            else:
                print(f"   → tidak memiliki dependen (leaf node)")
            
            predecessors = self.get_predecessors(node)
            if predecessors:
                print(f"   ← bergantung pada: {', '.join(predecessors)}")
    
    def print_adjacency_matrix(self) -> None:
        """
        Menampilkan adjacency matrix.
        """
        nodes = sorted(self.adjacency_list.keys())
        n = len(nodes)
        node_index = {node: i for i, node in enumerate(nodes)}
        
        print("\n" + "="*60)
        print("ADJACENCY MATRIX")
        print("="*60)
        
        # Header
        print("    ", end="")
        for node in nodes:
            print(f"{node:>4}", end="")
        print()
        
        # Matrix
        for i, u in enumerate(nodes):
            print(f"{u:>3} |", end="")
            for v in nodes:
                if v in self.adjacency_list.get(u, []):
                    print("   1", end="")
                else:
                    print("   0", end="")
            print()


# =============================================================================
# CONTOH PENGGUNAAN (Langsung Bisa Dijalankan)
# =============================================================================
if __name__ == "__main__":
    print("="*70)
    print(" DEMO GRAPH DAG (DIRECTED ACYCLIC GRAPH) - TANPA QUEUE")
    print("="*70)
    
    # ========== CONTOH 1: MEMBANGUN GRAPH ==========
    print("\n" + "-"*50)
    print("CONTOH 1: MEMBANGUN GRAPH DAG")
    print("-"*50)
    
    dag = FormulaDAG()
    
    # Tambahkan node (formula)
    dag.add_node("theta", "sudut dalam derajat")
    dag.add_node("rad", "theta * pi / 180")
    dag.add_node("v0", "kecepatan awal")
    dag.add_node("g", "gravitasi")
    dag.add_node("jarak", "(v0^2 * sin(2*rad)) / g")
    
    # Tambahkan edge (dependensi)
    dag.add_edge("theta", "rad")   # rad bergantung pada theta
    dag.add_edge("rad", "jarak")    # jarak bergantung pada rad
    dag.add_edge("v0", "jarak")     # jarak bergantung pada v0
    dag.add_edge("g", "jarak")      # jarak bergantung pada g
    
    # Tampilkan graph
    dag.display()
    
    # ========== CONTOH 2: TOPOLOGICAL SORT ==========
    print("\n" + "-"*50)
    print("CONTOH 2: TOPOLOGICAL SORT (Urutan Evaluasi)")
    print("-"*50)
    
    try:
        order = dag.topological_sort()
        print(f"Urutan topological: {' → '.join(order)}")
        print("\nPenjelasan: Node yang menjadi dependensi dievaluasi terlebih dahulu")
    except ValueError as e:
        print(f"Error: {e}")
    
    # ========== CONTOH 3: DETEKSI SIKLUS ==========
    print("\n" + "-"*50)
    print("CONTOH 3: DETEKSI SIKLUS")
    print("-"*50)
    
    # Buat graph dengan siklus
    dag_cycle = FormulaDAG()
    dag_cycle.add_node("A", "")
    dag_cycle.add_node("B", "")
    dag_cycle.add_node("C", "")
    
    dag_cycle.add_edge("A", "B")
    dag_cycle.add_edge("B", "C")
    dag_cycle.add_edge("C", "A")  # Siklus: A → B → C → A
    
    print("Graph dengan siklus: A → B → C → A")
    print(f"Memiliki siklus? {dag_cycle.has_cycle()}")
    
    cycle = dag_cycle.find_cycle()
    if cycle:
        print(f"Siklus ditemukan: {' → '.join(cycle)}")
    
    # ========== CONTOH 4: URUTAN EVALUASI UNTUK TARGET ==========
    print("\n" + "-"*50)
    print("CONTOH 4: URUTAN EVALUASI UNTUK FORMULA 'jarak'")
    print("-"*50)
    
    order_for_jarak = dag.get_evaluation_order("jarak")
    print(f"Evaluasi '{'jarak'}' perlu memproses: {' → '.join(order_for_jarak)}")
    
    # ========== CONTOH 5: MENGGUNAKAN DEFINE_FORMULA ==========
    print("\n" + "-"*50)
    print("CONTOH 5: DEFINE FORMULA DENGAN DEPENDENSI")
    print("-"*50)
    
    dag2 = FormulaDAG()
    
    # Definisikan formula dengan dependensi otomatis
    try:
        dag2.define_formula("rad", "theta * pi / 180", ["theta"])
        dag2.define_formula("jarak", "(v0^2 * sin(2*rad)) / g", ["v0", "rad", "g"])
        
        print("✅ Formula berhasil didefinisikan:")
        dag2.display()
        
        order = dag2.get_evaluation_order("jarak")
        print(f"\nUrutan evaluasi 'jarak': {' → '.join(order)}")
        
    except ValueError as e:
        print(f"Error: {e}")
    
    # ========== CONTOH 6: ADJACENCY MATRIX ==========
    print("\n" + "-"*50)
    print("CONTOH 6: ADJACENCY MATRIX")
    print("-"*50)
    
    dag.print_adjacency_matrix()
    
    print("\n" + "="*70)
    print("✅ SEMUA CONTOH SELESAI")
    print("="*70)
