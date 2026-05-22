import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modul1_stack import Stack, LNode


def test_node_creation():
    """TEST 1: Membuat Node Linked List"""
    print("\n" + "="*60)
    print("TEST 1: MEMBUAT NODE LINKED LIST")
    print("="*60)
    
    # Buat node dengan data 10
    node1 = LNode(10)
    
    print(f"Node dibuat dengan data: {node1.data}")
    print(f"Pointer next: {node1.next}")
    
    assert node1.data == 10, "Data node harus 10"
    assert node1.next is None, "Pointer next harus None untuk node baru"
    
    print("\n✅ Node berhasil dibuat")
    print("   - Memiliki atribut 'data' untuk menyimpan nilai")
    print("   - Memiliki atribut 'next' untuk menunjuk node berikutnya")


def test_node_linking():
    """TEST 2: Menghubungkan Node (Linking)"""
    print("\n" + "="*60)
    print("TEST 2: MENGHUBUNGKAN NODE (LINKING)")
    print("="*60)
    
    # Buat 3 node
    node1 = LNode(10)
    node2 = LNode(20)
    node3 = LNode(30)
    
    print("Node yang dibuat:")
    print(f"   Node1: data={node1.data}, next={node1.next}")
    print(f"   Node2: data={node2.data}, next={node2.next}")
    print(f"   Node3: data={node3.data}, next={node3.next}")
    
    # Hubungkan node: node1 → node2 → node3 → None
    node1.next = node2
    node2.next = node3
    # node3.next sudah None (default)
    
    print("\nSetelah dihubungkan:")
    print(f"   Node1.next = node2 (data={node1.next.data})")
    print(f"   Node2.next = node3 (data={node2.next.data})")
    print(f"   Node3.next = {node3.next}")
    
    assert node1.next is node2, "Node1 harus menunjuk ke Node2"
    assert node2.next is node3, "Node2 harus menunjuk ke Node3"
    assert node3.next is None, "Node3 harus menunjuk ke None"
    
    print("\n✅ Node berhasil dihubungkan membentuk rantai:")
    print(f"   {node1.data} → {node2.data} → {node3.data} → None")


def test_traverse_linked_list():
    """TEST 3: Melintasi Linked List (Traversal)"""
    print("\n" + "="*60)
    print("TEST 3: MELINTASI LINKED LIST (TRAVERSAL)")
    print("="*60)
    
    # Membuat linked list: 10 → 20 → 30 → 40 → 50 → None
    head = LNode(10)
    head.next = LNode(20)
    head.next.next = LNode(30)
    head.next.next.next = LNode(40)
    head.next.next.next.next = LNode(50)
    
    print("Linked List yang dibuat:")
    print(f"   {head.data} → {head.next.data} → {head.next.next.data} → {head.next.next.next.data} → {head.next.next.next.next.data} → None")
    
    # Traversal
    result = []
    current = head
    position = 1
    
    while current:
        result.append(current.data)
        print(f"   Posisi {position}: data={current.data}, next={'ada' if current.next else 'None'}")
        current = current.next
        position += 1
    
    print(f"\nHasil traversal: {result}")
    assert result == [10, 20, 30, 40, 50], f"Traversal harus [10,20,30,40,50], tapi dapat {result}"
    
    print("\n✅ Linked List dapat dilintasi dari awal hingga akhir")
    print("   Setiap node mengarah ke node berikutnya, node terakhir ke None")


def test_push_creates_linked_list():
    """TEST 4: Push menggunakan Linked List (Stack)"""
    print("\n" + "="*60)
    print("TEST 4: PUSH MEMBENTUK LINKED LIST (STACK)")
    print("="*60)
    
    stack = Stack()
    
    print("\nProses push:")
    print("Push 10:")
    stack.push(10)
    print_linked_list(stack, "   ")
    
    print("Push 20:")
    stack.push(20)
    print_linked_list(stack, "   ")
    
    print("Push 30:")
    stack.push(30)
    print_linked_list(stack, "   ")
    
    print("Push 40:")
    stack.push(40)
    print_linked_list(stack, "   ")
    
    # Verifikasi struktur linked list
    assert stack.top.data == 40, "Top harus berisi data terakhir (40)"
    assert stack.top.next.data == 30, "Node kedua harus berisi 30"
    assert stack.top.next.next.data == 20, "Node ketiga harus berisi 20"
    assert stack.top.next.next.next.data == 10, "Node keempat harus berisi 10"
    assert stack.top.next.next.next.next is None, "Node terakhir harus None"
    
    print("\n✅ Push membentuk linked list dengan benar")
    print("   Data baru selalu menjadi HEAD (top)")
    print("   Setiap push menambahkan node baru di depan")


def test_pop_removes_from_linked_list():
    """TEST 5: Pop menghapus node dari Linked List"""
    print("\n" + "="*60)
    print("TEST 5: POP MENGHAPUS NODE DARI LINKED LIST")
    print("="*60)
    
    stack = Stack()
    
    # Push beberapa data
    for val in [10, 20, 30, 40, 50]:
        stack.push(val)
    
    print("\nLinked List awal:")
    print_linked_list(stack, "   ")
    
    print("\nProses pop:")
    
    # Pop 1
    popped = stack.pop()
    print(f"Pop 1 → {popped}")
    print_linked_list(stack, "   ")
    assert popped == 50, "Pop pertama harus 50"
    
    # Pop 2
    popped = stack.pop()
    print(f"Pop 2 → {popped}")
    print_linked_list(stack, "   ")
    assert popped == 40, "Pop kedua harus 40"
    
    # Pop 3
    popped = stack.pop()
    print(f"Pop 3 → {popped}")
    print_linked_list(stack, "   ")
    assert popped == 30, "Pop ketiga harus 30"
    
    # Verifikasi sisa linked list
    assert stack.top.data == 20, "Top sekarang harus 20"
    assert stack.top.next.data == 10, "Node berikutnya harus 10"
    assert stack.top.next.next is None, "Node terakhir harus None"
    
    print("\n✅ Pop menghapus node HEAD (top) dari linked list")
    print("   Node yang dihapus = node paling depan")
    print("   Top berpindah ke node berikutnya")


def test_pointer_reference():
    """TEST 6: Memahami Pointer/Reference pada Linked List"""
    print("\n" + "="*60)
    print("TEST 6: MEMAHAMI POINTER/REFERENCE PADA LINKED LIST")
    print("="*60)
    
    # Buat node
    node_a = LNode(100)
    node_b = LNode(200)
    node_c = LNode(300)
    
    print("Node dibuat:")
    print(f"   node_a: data={node_a.data}, next={node_a.next}")
    print(f"   node_b: data={node_b.data}, next={node_b.next}")
    print(f"   node_c: data={node_c.data}, next={node_c.next}")
    
    # Hubungkan: node_a → node_b → node_c
    node_a.next = node_b
    node_b.next = node_c
    
    print("\nSetelah linking:")
    print(f"   node_a.next menunjuk ke node_b (data={node_a.next.data})")
    print(f"   node_b.next menunjuk ke node_c (data={node_b.next.data})")
    
    # Demonstrasi pointer: node_a.next adalah node_b
    print("\nDemonstrasi pointer:")
    print(f"   node_a.next == node_b : {node_a.next is node_b}")
    print(f"   node_a.next.data == node_b.data : {node_a.next.data == node_b.data}")
    
    # Jika node_b berubah, node_a.next juga ikut berubah
    node_b.data = 999
    print(f"\nSetelah node_b.data diubah menjadi 999:")
    print(f"   node_b.data = {node_b.data}")
    print(f"   node_a.next.data = {node_a.next.data} (ikut berubah karena referensi)")
    
    assert node_a.next is node_b, "node_a.next harus mereferensi node_b"
    assert node_a.next.data == node_b.data, "Data harus sama karena referensi"
    
    print("\n✅ Linked List menggunakan konsep reference/pointer")
    print("   node.next menyimpan referensi ke node lain, bukan copy")


def test_linked_list_visualization():
    """TEST 7: Visualisasi Linked List"""
    print("\n" + "="*60)
    print("TEST 7: VISUALISASI LINKED LIST")
    print("="*60)
    
    stack = Stack()
    
    # Push data
    for val in [5, 15, 25, 35]:
        stack.push(val)
    
    print("\n" + "="*50)
    print("      STRUKTUR LINKED LIST (STACK)")
    print("="*50)
    
    current = stack.top
    position = 1
    nodes = []
    
    while current:
        nodes.append(str(current.data))
        arrow = "→" if current.next else "None"
        print(f"   Node {position}: [data: {current.data:3d}] {arrow}")
        current = current.next
        position += 1
    
    print("\n" + "="*50)
    print(f"   Representasi: {' → '.join(nodes)} → None")
    print("="*50)
    
    print("\n✅ Visualisasi linked list:")
    print("   - Node teratas (top) adalah data terakhir yang di-push")
    print("   - Setiap node memiliki pointer ke node berikutnya")
    print("   - Node terakhir menunjuk ke None")


def print_linked_list(stack, prefix=""):
    """Helper: Mencetak struktur linked list dari stack"""
    current = stack.top
    nodes = []
    while current:
        nodes.append(str(current.data))
        current = current.next
    print(f"{prefix}{' → '.join(nodes)} → None")


def run_all_tests():
    """Menjalankan semua test linked list"""
    print("\n" + "="*70)
    print("   TEST FOKUS: LINKED LIST PADA STACK")
    print("="*70)
    
    tests = [
        ("Membuat Node Linked List", test_node_creation),
        ("Menghubungkan Node (Linking)", test_node_linking),
        ("Melintasi Linked List (Traversal)", test_traverse_linked_list),
        ("Push Membentuk Linked List", test_push_creates_linked_list),
        ("Pop Menghapus dari Linked List", test_pop_removes_from_linked_list),
        ("Memahami Pointer/Reference", test_pointer_reference),
        ("Visualisasi Linked List", test_linked_list_visualization),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ GAGAL: {test_name}")
            print(f"   Error: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ ERROR: {test_name}")
            print(f"   {type(e).__name__}: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f" HASIL: {passed} berhasil, {failed} gagal")
    print("="*70)
    
    if failed == 0:
        print("\n🎉 SEMUA TEST LINKED LIST BERHASIL!")
        print("   Implementasi Linked List sudah benar:")
        print("   ✓ Node memiliki data dan pointer next")
        print("   ✓ Node dapat dihubungkan membentuk rantai")
        print("   ✓ Traversal dari head hingga None")
        print("   ✓ Push menambah node di depan")
        print("   ✓ Pop menghapus node dari depan")
        print("   ✓ Menggunakan konsep reference/pointer")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
