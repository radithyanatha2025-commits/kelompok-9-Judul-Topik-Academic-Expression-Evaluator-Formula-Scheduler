from collections import deque

# Di dalam topological_sort():
q = deque([u for u, d in in_degree.items() if d == 0])  # inisialisasi queue
while q:
    u = q.popleft()    # DEQUEUE (ambil dari depan)
    # ... proses ...
    for v in self.adj.get(u, []):
        in_degree[v] -= 1
        if in_degree[v] == 0:
            q.append(v)  # ENQUEUE (tambah ke belakang)
