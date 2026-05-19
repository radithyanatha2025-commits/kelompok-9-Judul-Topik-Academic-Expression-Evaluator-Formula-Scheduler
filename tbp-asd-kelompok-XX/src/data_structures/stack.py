class LNode:
    """Node untuk Linked List"""
    __slots__ = ('data', 'next')
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    """Stack berbasis Linked List"""
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, data) -> None:
        """Push data ke stack - O(1)"""
        node = LNode(data)
        node.next = self.top
        self.top = node
        self.size += 1

    def pop(self):
        """Pop data dari stack - O(1)"""
        if self.top is None:
            return None
        val = self.top.data
        self.top = self.top.next
        self.size -= 1
        return val

    def peek(self):
        """Lihat data teratas tanpa menghapus - O(1)"""
        return self.top.data if self.top else None

    def is_empty(self) -> bool:
        """Cek apakah stack kosong - O(1)"""
        return self.size == 0
