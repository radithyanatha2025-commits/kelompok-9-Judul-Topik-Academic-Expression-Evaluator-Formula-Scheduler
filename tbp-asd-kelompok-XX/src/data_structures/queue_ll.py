def topological_sort(self) -> List[str]:
    nodes = set(self.formulas.keys())
    in_degree = {n: 0 for n in nodes}
    
    # Hitung in-degree setiap node
    for u in nodes:
        for v in self.graph.get(u, []):
            if v in nodes:
                in_degree[v] += 1
    
    # ========== QUEUE DI SINI ==========
    q = deque([n for n in nodes if in_degree[n] == 0])  # inisialisasi queue
    
    order = []
    while q:                              # while queue tidak kosong
        u = q.popleft()                   # dequeue: ambil dari depan
        order.append(u)
        for v in self.graph.get(u, []):   # untuk setiap tetangga
            if v in nodes:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    q.append(v)           # enqueue: tambah ke belakang
    # ===================================
    
    if len(order) != len(nodes):
        raise ValueError("Siklus dependensi terdeteksi")
    return order
