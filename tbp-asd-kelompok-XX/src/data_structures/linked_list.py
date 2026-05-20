# =============================================================================
# LINKED LIST NODE
# =============================================================================
class LNode:
    __slots__ = ('data', 'next')

    def __init__(self, data):
        self.data = data
        self.next = None


# =============================================================================
# STACK MENGGUNAKAN LINKED LIST
# =============================================================================
class Stack:
    def __init__(self):
        self.top = None
        self.size = 0

    # Push data ke stack
    def push(self, data):
        node = LNode(data)
        node.next = self.top
        self.top = node
        self.size += 1

    # Pop data dari stack
    def pop(self):
        if self.top is None:
            return None

        val = self.top.data
        self.top = self.top.next
        self.size -= 1
        return val

    # Melihat elemen paling atas
    def peek(self):
        if self.top:
            return self.top.data
        return None

    # Mengecek apakah stack kosong
    def is_empty(self):
        return self.size == 0

    # Menampilkan isi stack
    def display(self):
        cur = self.top
        print("TOP -> ", end="")
        while cur:
            print(cur.data, end=" -> ")
            cur = cur.next
        print("None")
