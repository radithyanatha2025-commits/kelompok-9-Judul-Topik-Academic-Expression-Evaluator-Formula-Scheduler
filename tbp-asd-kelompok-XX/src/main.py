import math, time
from typing import Optional, Dict, List, Tuple

# ── Precedence & associativity ─────────────────────────────────
PREC = {'+': 2, '-': 2, '*': 3, '/': 3, '^': 4}
RASSOC = {'^'} # right-associative operators
FUNCS = {'sin': math.sin, 'cos': math.cos, 'sqrt': math.sqrt,
'log': math.log, 'abs': abs}
# ── Node Linked List ──────────────────────────────────────────────
class LLNode:
    def __init__(self, data=None):
        self.data = data
        self.next: Optional['LLNode'] = None

# ── Stack berbasis Linked List ────────────────────────────────────
class Stack:
    def __init__(self):
        self.top: Optional['LLNode'] = None
        self._size = int             = 0

def push(self, data) -> None:
    """Big-O: O(1)."""
    node = LLNode(data)
    node.next = self.top
    self.top = node
    self._size += 1
    
def pop(self):
    """Big-O: O(1)."""
    if not self.top: 
        return None
    val      = self.top.data
    self.top = self.top.next
    self._size -= 1
    return val

def peek(self):
    return self.top.data if self.top else None

def is_empty(self) -> bool:
    return self._size == 0

# ── Tokenizer (diberikan, jangng diubah) ───────────────────────────────────────────────
def tokenize(expr: str) -> List[str]:
    """
    Memecah string ekspresi menjadi list token.
    Mendukung: angka (int/float), variabel (a-z),
    operator (+,-,*,/,^), kurung, nama fungsi.
    Contoh: '(a+b)*sin(c)' -> ['(','a','+','b',')','*','sin','(','c',')']
    Big-O: O(n) di mana n = panjang string.
    """
class Queue :
    """Queue (FIFO) berbasis Linked List. Dipakai pada Kahn's algoritma."""
    
def __init__(self):
        self._head: optional[LLNode] = None 
        self._tail: Optional[LLNode] = None
        self._size: int  
def enqueque(self, data) -> None:
    """Big-O: O(1)."""
    node = LLnode(data)
    if self._tail:
        self._tail.next = node
    self._tail = node
    if self._head is None:
        self._head = node
    self._size += 1

def dequeque(self):
    """Big-O: O(1)."""
    if not self._head:
         return None 
    Val         = self._head.data
    self._head  = self._head.next
    if self.head is None:
        self._tail = None 
    slef._size -= 1
    return val

def is_empty(self) -> bool:
