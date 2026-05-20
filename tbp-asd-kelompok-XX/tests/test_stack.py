"""
UNIT TEST: STACK (LINKED LIST)
Menguji implementasi Stack berbasis Linked List
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_structures.stack import Stack, LNode


def test_linked_list_node():
    """Menguji pembuatan node Linked List"""
    print("\n[TEST] Linked List Node")
    
    node = LNode(10)
    assert node.data == 10
    assert node.next is None
    
    node2 = LNode(20)
    node.next = node2
    assert node.next.data == 20
    
    print("✅ Linked List Node test passed!")


def test_stack_push():
    """Menguji operasi push pada Stack"""
    print("\n[TEST] Stack Push")
    
    stack = Stack()
    
    # Push pertama
    stack.push(10)
    assert stack.size == 1
    assert stack.peek() == 10
    assert stack.top.data == 10
    
    # Push kedua
    stack.push(20)
    assert stack.size == 2
    assert stack.peek() == 20
    assert stack.top.data == 20
    assert stack.top.next.data == 10
    
    # Push ketiga
    stack.push(30)
    assert stack.size == 3
    assert stack.peek() == 30
    
    print("✅ Stack Push test passed!")


def test_stack_pop():
    """Menguji operasi pop pada Stack (LIFO)"""
    print("\n[TEST] Stack Pop")
    
    stack = Stack()
    
    # Pop dari stack kosong
    assert stack.pop() is None
    
    # Push beberapa data
    stack.push(10)
    stack.push(20)
    stack.push(30)
    
    # Pop harus mengembalikan 30 (LIFO)
    popped = stack.pop()
    assert popped == 30
    assert stack.size == 2
    assert stack.peek() == 20
    
    popped = stack.pop()
    assert popped == 20
    assert stack.size == 1
    assert stack.peek() == 10
    
    popped = stack.pop()
    assert popped == 10
    assert stack.size == 0
    assert stack.is_empty() == True
    
    # Pop dari stack kosong lagi
    assert stack.pop() is None
    
    print("✅ Stack Pop test passed!")


def test_stack_peek():
    """Menguji operasi peek pada Stack (melihat tanpa menghapus)"""
    print("\n[TEST] Stack Peek")
    
    stack = Stack()
    
    # Peek stack kosong
    assert stack.peek() is None
    
    stack.push(100)
    assert stack.peek() == 100
    assert stack.size == 1  # Size tidak berubah
    
    stack.push(200)
    assert stack.peek() == 200
    assert stack.size == 2  # Size tidak berubah
    
    print("✅ Stack Peek test passed!")


def test_stack_is_empty():
    """Menguji operasi is_empty pada Stack"""
    print("\n[TEST] Stack Is Empty")
    
    stack = Stack()
    assert stack.is_empty() == True
    
    stack.push(10)
    assert stack.is_empty() == False
    
    stack.pop()
    assert stack.is_empty() == True
    
    print("✅ Stack Is Empty test passed!")


if __name__ == "__main__":
    print("=" * 60)
    print("UNIT TEST: STRUKTUR DATA STACK")
    print("=" * 60)
    test_linked_list_node()
    test_stack_push()
    test_stack_pop()
    test_stack_peek()
    test_stack_is_empty()
    print("\n" + "=" * 60)
    print("✅ SEMUA TEST STACK BERHASIL!")
    print("=" * 60)
