"""
UNIT TEST: MODUL 3 - BST TABEL VARIABEL
Menguji implementasi BST untuk menyimpan variabel
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.modul_3 import VarBST


def test_modul_3_set_get():
    """Menguji SET dan GET variabel"""
    print("\n[TEST MODUL 3] SET and GET")
    
    bst = VarBST()
    
    # SET variabel
    bst.set('a', 10.0)
    bst.set('b', 20.0)
    bst.set('c', 30.0)
    
    # GET variabel
    assert bst.get('a') == 10.0
    assert bst.get('b') == 20.0
    assert bst.get('c') == 30.0
    assert bst.get('z') is None
    
    # UPDATE variabel
    bst.set('b', 25.0)
    assert bst.get('b') == 25.0
    
    print("✅ SET and GET test passed!")


def test_modul_3_delete():
    """Menguji DELETE variabel"""
    print("\n[TEST MODUL 3] DELETE")
    
    bst = VarBST()
    bst.set('a', 10.0)
    bst.set('b', 20.0)
    bst.set('c', 30.0)
    
    # DELETE variabel
    bst.delete('b')
    assert bst.get('b') is None
    assert bst.get('a') == 10.0
    assert bst.get('c') == 30.0
    
    # DELETE variabel yang tidak ada
    bst.delete('z')  # Seharusnya tidak error
    
    print("✅ DELETE test passed!")


def test_modul_3_list():
    """Menguji LIST (inorder traversal)"""
    print("\n[TEST MODUL 3] LIST")
    
    bst = VarBST()
    
    # LIST kosong
    assert bst.list_all() == []
    
    # Insert tidak berurutan
    bst.set('d', 40.0)
    bst.set('b', 20.0)
    bst.set('f', 60.0)
    bst.set('a', 10.0)
    bst.set('c', 30.0)
    bst.set('e', 50.0)
    bst.set('g', 70.0)
    
    # LIST harus terurut
    expected = [
        ('a', 10.0), ('b', 20.0), ('c', 30.0),
        ('d', 40.0), ('e', 50.0), ('f', 60.0), ('g', 70.0)
    ]
    
    assert bst.list_all() == expected
    
    print("✅ LIST test passed!")


def test_modul_3_validation():
    """Menguji validasi nama variabel"""
    print("\n[TEST MODUL 3] Validation")
    
    bst = VarBST()
    
    # Nama variabel harus satu huruf
    try:
        bst.set('ab', 10.0)
        assert False, "Should reject multi-letter variable"
    except ValueError as e:
        assert "satu huruf" in str(e)
        print(f"  ✅ Multi-letter rejected: {e}")
    
    # Nama variabel harus huruf
    try:
        bst.set('1', 10.0)
        assert False, "Should reject numeric variable"
    except ValueError as e:
        assert "satu huruf" in str(e)
        print(f"  ✅ Numeric variable rejected: {e}")
    
    print("✅ Validation test passed!")


if __name__ == "__main__":
    print("=" * 60)
    print("UNIT TEST: MODUL 3 (BST TABEL VARIABEL)")
    print("=" * 60)
    test_modul_3_set_get()
    test_modul_3_delete()
    test_modul_3_list()
    test_modul_3_validation()
    print("\n" + "=" * 60)
    print("✅ SEMUA TEST MODUL 3 BERHASIL!")
    print("=" * 60)
