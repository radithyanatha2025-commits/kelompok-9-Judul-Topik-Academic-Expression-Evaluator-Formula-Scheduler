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

# Modul 1: Konversi Infix ke Postfix (Shunting-Yard)
def infix_to_postfix(tokens: list) -> list:
    output = []
    op_stack = Stack()  # <-- PENGGUNAAN STACK
    
    for tok in tokens:
        if tok in FUNCS:
            op_stack.push(tok)      # push fungsi
        elif tok == '(':
            op_stack.push(tok)      # push kurung buka
        elif tok == ')':
            while not op_stack.is_empty() and op_stack.peek() != '(':
                output.append(op_stack.pop())  # pop hingga '('
            op_stack.pop()  # buang '('
        elif tok in PREC:
            while (not op_stack.is_empty() and op_stack.peek() != '(' and
                   (PREC[op_stack.peek()] > PREC[tok] or
                    (PREC[op_stack.peek()] == PREC[tok] and tok not in RASSOC))):
                output.append(op_stack.pop())  # pop operator
            op_stack.push(tok)      # push operator baru
        else:
            output.append(tok)
    
    while not op_stack.is_empty():
        output.append(op_stack.pop())  # pop sisa operator
    
    return output

# Modul 2: Evaluasi Postfix
def eval_postfix(tokens: list, var_table: dict) -> float:
    stack = Stack()  # <-- PENGGUNAAN STACK
    
    for tok in tokens:
        if tok in FUNCS:
            arg = stack.pop()      # pop operand
            res = math.sin(arg)    # hitung fungsi
            stack.push(res)        # push hasil
        elif tok in PREC:
            b = stack.pop()        # pop operand kanan
            a = stack.pop()        # pop operand kiri
            res = a + b            # hitung operator
            stack.push(res)        # push hasil
        else:
            stack.push(float(tok)) # push angka/variabel
    
    return stack.pop()  # hasil akhir

# Modul 4: Build Expression Tree
def build_expr_tree(postfix: list):
    stack = Stack()  # <-- PENGGUNAAN STACK
    
    for tok in postfix:
        node = ExprNode(tok)
        if tok in PREC:                     # operator binary
            right = stack.pop()             # pop right child
            left = stack.pop()              # pop left child
            node.left = left
            node.right = right
        elif tok in FUNCS:                  # fungsi unary
            child = stack.pop()             # pop child
            node.left = child
        stack.push(node)                    # push node ke stack
    
    return stack.pop()  # root tree
