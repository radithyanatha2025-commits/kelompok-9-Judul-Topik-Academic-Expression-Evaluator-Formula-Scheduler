"""
UNIT TEST: BST (BINARY SEARCH TREE)
Menguji implementasi BST untuk tabel variabel
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_structures.bst import VarBST, VarBSTNode


def test_bst_node():
    """Menguji pembuatan node BST"""
    print("\n[TEST] BST Node")
    
    node = VarBSTNode('a', 10.0)
    assert node.key == 'a'
    assert node.val == 10.0
    assert node.left is None
    assert node.right is None
    
    print("✅ BST Node test passed!")


def test_bst_set_insert():
    """Menguji operasi SET (insert) pada BST"""
    print("\n[TEST] BST Set (Insert)")
    
    bst = VarBST()
    
    # Insert variabel
    bst.set('c', 30.0)
    bst.set('a', 10.0)
    bst.set('b', 20.0)
    
    # Verifikasi struktur BST
    assert bst.root.key == 'c'
    assert bst.root.left.key == 'a'
    assert bst.root.left.right.key == 'b'
    
    print("✅ BST Set (Insert) test passed!")


def test_bst_set_update():
    """Menguji operasi SET (update) pada BST"""
    print("\n[TEST] BST Set (Update)")
    
    bst = VarBST()
    
    bst.set('x', 100.0)
    assert bst.get('x') == 100.0
    
    # Update nilai
    bst.set('x', 200.0)
    assert bst.get('x') == 200.0
    
    # Ukuran tetap 1 (update, bukan insert baru)
    assert bst.root.key == 'x'
    assert bst.root.left is None
    assert bst.root.right is None
    
    print("✅ BST Set (Update) test passed!")


def test_bst_get():
    """Menguji operasi GET pada BST"""
    print("\n[TEST] BST Get")
    
    bst = VarBST()
    
    # Get dari BST kosong
    assert bst.get('a') is None
    
    # Insert beberapa data
    bst.set('b', 20.0)
    bst.set('a', 10.0)
    bst.set('c', 30.0)
    
    # Get nilai yang ada
    assert bst.get('a') == 10.0
    assert bst.get('b') == 20.0
    assert bst.get('c') == 30.0
    
    # Get nilai yang tidak ada
    assert bst.get('z') is None
    
    print("✅ BST Get test passed!")


def test_bst_delete_leaf():
    """Menguji DELETE node daun (tidak punya anak) pada BST"""
    print("\n[TEST] BST Delete - Leaf Node")
    
    bst = VarBST()
    bst.set('b', 20.0)
    bst.set('a', 10.0)
    bst.set('c', 30.0)
    
    # Hapus node daun 'a'
    bst.delete('a')
    assert bst.get('a') is None
    assert bst.root.left is None  # Tidak ada left child lagi
    
    # Hapus node daun 'c'
    bst.delete('c')
    assert bst.get('c') is None
    assert bst.root.right is None  # Tidak ada right child lagi
    
    print("✅ BST Delete - Leaf Node test passed!")


def test_bst_delete_one_child():
    """Menguji DELETE node dengan satu anak pada BST"""
    print("\n[TEST] BST Delete - Node with One Child")
    
    bst = VarBST()
    bst.set('b', 20.0)
    bst.set('a', 10.0)
    bst.set('c', 30.0)
    bst.set('d', 40.0)
    
    # 'c' memiliki satu anak kanan 'd'
    bst.delete('c')
    assert bst.get('c') is None
    assert bst.root.right.key == 'd'  # 'd' naik ke posisi 'c'
    
    print("✅ BST Delete - Node with One Child test passed!")


def test_bst_delete_two_children():
    """Menguji DELETE node dengan dua anak pada BST"""
    print("\n[TEST] BST Delete - Node with Two Children")
    
    bst = VarBST()
    bst.set('d', 40.0)
    bst.set('b', 20.0)
    bst.set('f', 60.0)
    bst.set('a', 10.0)
    bst.set('c', 30.0)
    bst.set('e', 50.0)
    bst.set('g', 70.0)
    
    # Hapus node 'd' (punya dua anak)
    bst.delete('d')
    assert bst.get('d') is None
    # Inorder successor 'e' (50) harus menggantikan 'd'
    assert bst.root.key == 'e'
    
    print("✅ BST Delete - Node with Two Children test passed!")


def test_bst_list_all():
    """Menguji operasi LIST (inorder traversal) pada BST"""
    print("\n[TEST] BST List All (Inorder Traversal)")
    
    bst = VarBST()
    
    # BST kosong
    assert bst.list_all() == []
    
    # Insert data tidak berurutan
    bst.set('d', 40.0)
    bst.set('b', 20.0)
    bst.set('f', 60.0)
    bst.set('a', 10.0)
    bst.set('c', 30.0)
    bst.set('e', 50.0)
    bst.set('g', 70.0)
    
    # List harus terurut berdasarkan key
    expected = [
        ('a', 10.0), ('b', 20.0), ('c', 30.0),
        ('d', 40.0), ('e', 50.0), ('f', 60.0), ('g', 70.0)
    ]
    
    result = bst.list_all()
    assert result == expected
    
    print("✅ BST List All test passed!")


if __name__ == "__main__":
    print("=" * 60)
    print("UNIT TEST: STRUKTUR DATA BST")
    print("=" * 60)
    test_bst_node()
    test_bst_set_insert()
    test_bst_set_update()
    test_bst_get()
    test_bst_delete_leaf()
    test_bst_delete_one_child()
    test_bst_delete_two_children()
    test_bst_list_all()
    print("\n" + "=" * 60)
    print("✅ SEMUA TEST BST BERHASIL!")
    print("=" * 60)
