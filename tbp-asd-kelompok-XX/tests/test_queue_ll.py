import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =============================================================================
# IMPLEMENTASI QUEUE (Linked List)
# =============================================================================
class QNode:
    """Node untuk Queue berbasis Linked List"""
    __slots__ = ('data', 'next')
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    """
    Queue (Antrian) berbasis Linked List
    Operasi: enqueue (tambah di belakang), dequeue (ambil dari depan)
    FIFO: First In First Out
    Big-O: O(1) untuk enqueue dan dequeue
    """
    def __init__(self):
        self.front = None   # depan (untuk dequeue)
        self.rear = None    # belakang (untuk enqueue)
        self.size = 0

    def enqueue(self, data) -> None:
        """
        Tambah data ke belakang antrian (FIFO)
        Big-O: O(1)
        """
        node = QNode(data)
        if self.rear is None:
            # Queue kosong
            self.front = node
            self.rear = node
        else:
            self.rear.next = node
            self.rear = node
        self.size += 1

    def dequeue(self):
        """
        Hapus dan ambil data dari depan antrian
        Big-O: O(1)
        """
        if self.front is None:
            return None
        val = self.front.data
        self.front = self.front.next
        if self.front is None:
            # Queue menjadi kosong
            self.rear = None
        self.size -= 1
        return val

    def peek(self):
        """Lihat data di depan tanpa menghapus"""
        return self.front.data if self.front else None

    def is_empty(self) -> bool:
        """Cek apakah queue kosong"""
        return self.size == 0

    def get_size(self) -> int:
        """Mendapatkan jumlah elemen dalam queue"""
        return self.size


# =============================================================================
# UNIT TEST
# =============================================================================
def test_queue_node():
    """Menguji pembuatan node Queue"""
    print("\n[TEST] Queue Node")
    
    node = QNode(10)
    assert node.data == 10
    assert node.next is None
    
    node2 = QNode(20)
    node.next = node2
    assert node.next.data == 20
    
    print("✅ Queue Node test passed!")


def test_queue_enqueue():
    """Menguji operasi enqueue (tambah ke belakang)"""
    print("\n[TEST] Queue Enqueue")
    
    q = Queue()
    
    # Enqueue pertama
    q.enqueue(10)
    assert q.size == 1
    assert q.front.data == 10
    assert q.rear.data == 10
    
    # Enqueue kedua
    q.enqueue(20)
    assert q.size == 2
    assert q.front.data == 10  # depan tetap 10
    assert q.rear.data == 20   # belakang berubah jadi 20
    
    # Enqueue ketiga
    q.enqueue(30)
    assert q.size == 3
    assert q.front.data == 10
    assert q.rear.data == 30
    
    print("✅ Queue Enqueue test passed!")


def test_queue_dequeue():
    """Menguji operasi dequeue (ambil dari depan)"""
    print("\n[TEST] Queue Dequeue")
    
    q = Queue()
    
    # Dequeue dari queue kosong
    assert q.dequeue() is None
    
    # Enqueue beberapa data
    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    
    # Dequeue pertama (FIFO: yang pertama masuk, pertama keluar)
    val = q.dequeue()
    assert val == 10
    assert q.size == 2
    assert q.front.data == 20
    assert q.rear.data == 30
    
    # Dequeue kedua
    val = q.dequeue()
    assert val == 20
    assert q.size == 1
    assert q.front.data == 30
    assert q.rear.data == 30
    
    # Dequeue ketiga
    val = q.dequeue()
    assert val == 30
    assert q.size == 0
    assert q.front is None
    assert q.rear is None
    assert q.is_empty() == True
    
    # Dequeue dari queue kosong lagi
    assert q.dequeue() is None
    
    print("✅ Queue Dequeue test passed!")


def test_queue_peek():
    """Menguji operasi peek (melihat depan tanpa menghapus)"""
    print("\n[TEST] Queue Peek")
    
    q = Queue()
    
    # Peek queue kosong
    assert q.peek() is None
    
    q.enqueue(100)
    assert q.peek() == 100
    assert q.size == 1  # size tidak berubah
    
    q.enqueue(200)
    assert q.peek() == 100  # depan tetap 100
    assert q.size == 2
    
    q.dequeue()
    assert q.peek() == 200
    assert q.size == 1
    
    print("✅ Queue Peek test passed!")


def test_queue_is_empty():
    """Menguji operasi is_empty"""
    print("\n[TEST] Queue Is Empty")
    
    q = Queue()
    assert q.is_empty() == True
    
    q.enqueue(10)
    assert q.is_empty() == False
    
    q.dequeue()
    assert q.is_empty() == True
    
    print("✅ Queue Is Empty test passed!")


def test_queue_fifo_order():
    """Menguji bahwa Queue benar-benar FIFO (First In First Out)"""
    print("\n[TEST] Queue FIFO Order")
    
    q = Queue()
    
    # Masukkan data secara berurutan
    for i in range(1, 6):
        q.enqueue(i)
    
    # Keluarkan harus sesuai urutan 1,2,3,4,5
    expected = [1, 2, 3, 4, 5]
    actual = []
    
    while not q.is_empty():
        actual.append(q.dequeue())
    
    assert actual == expected, f"Expected {expected}, got {actual}"
    
    print(f"✅ Queue FIFO order test passed! Order: {actual}")


def test_queue_implementation_in_topological_sort():
    """
    Menguji bahwa Queue digunakan dengan benar dalam topological sort
    (Seperti yang digunakan di Modul 5)
    """
    print("\n[TEST] Queue Usage in Topological Sort Simulation")
    
    # Simulasi graph sederhana: a → b → c
    # topological sort dengan Kahn's algorithm menggunakan Queue
    
    graph = {
        'a': ['b'],
        'b': ['c'],
        'c': []
    }
    
    in_degree = {'a': 0, 'b': 1, 'c': 1}
    
    # Inisialisasi queue dengan node yang in_degree = 0
    q = Queue()
    for node, degree in in_degree.items():
        if degree == 0:
            q.enqueue(node)
    
    order = []
    while not q.is_empty():
        u = q.dequeue()
        order.append(u)
        for v in graph.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.enqueue(v)
    
    # Hasil topological sort harus ['a', 'b', 'c']
    assert order == ['a', 'b', 'c'], f"Expected ['a','b','c'], got {order}"
    
    print(f"✅ Queue in topological sort test passed! Order: {order}")


def test_queue_visualization():
    """Menampilkan visualisasi Queue untuk pemahaman"""
    print("\n[TEST] Queue Visualization")
    
    q = Queue()
    
    print("\n   === VISUALISASI QUEUE (FIFO) ===")
    print("   Enqueue: tambah di BELAKANG")
    print("   Dequeue: ambil dari DEPAN\n")
    
    for i in range(1, 6):
        q.enqueue(i * 10)
        print(f"   enqueue({i*10}) → Queue: depan[{q.peek()}] ... belakang[{i*10}] | size={q.size}")
    
    print()
    while not q.is_empty():
        val = q.dequeue()
        print(f"   dequeue() → {val} | Queue sekarang: depan[{q.peek() if q.peek() else 'None'}] | size={q.size}")
    
    print("\n✅ Queue visualization test passed!")


if __name__ == "__main__":
    print("=" * 60)
    print("UNIT TEST: QUEUE (LINKED LIST)")
    print("=" * 60)
    print("\nQueue adalah struktur data FIFO (First In First Out)")
    print("Digunakan dalam Topological Sort (algoritma Kahn) di Modul 5\n")
    
    test_queue_node()
    test_queue_enqueue()
    test_queue_dequeue()
    test_queue_peek()
    test_queue_is_empty()
    test_queue_fifo_order()
    test_queue_implementation_in_topological_sort()
    test_queue_visualization()
    
    print("\n" + "=" * 60)
    print("✅ SEMUA TEST QUEUE BERHASIL!")
    print("=" * 60)
