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
        self._size = 0

def push(self, data) -> None:
    """Big-O: O(1)."""
    node = LLNode(data)
    node.next = self.top
    self.top = node
    self._size += 1

def pop(self):
    """Big-O: O(1)."""
    if not self.top: return None
    val = self.top.data
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
tokens = []
i = 0
while i < len(expr):
    ch = expr[i]
    if ch.isspace(): i += 1; continue
    if ch.isdigit() or (ch == '.' and i+1 < len(expr) and expr[i+1].isdigit()):
        j = i
        while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
            j += 1
        tokens.append(expr[i:j])
        i = j
    elif ch.isalpha():
        j = i
        while j < len(expr) and expr[j].isalpha():
            j += 1
        tokens.append(expr[i:j])
        i = j
    elif ch in '+-*/^()':
        tokens.append(ch)
        i += 1
    else:
        raise ValueError(f'Token tidak dikenal: {ch!r}')
return tokens

# ── Shunting-Yard: infix → postfix (implementasikan) ─────────────
def infix_to_postfix(tokens: List[str]) -> List[str]:
    """
    Konversi token infix ke postfix menggunakan Stack Linked List.
    Big-O: O(n) waktu, O(n) ruang.
    Catatan: unary minus belum didukung dalam starter ini.
    """
    output: List[str] = []
    op_stack = Stack()
    # TODO: implementasikan Shunting-Yard Algorithm
    # Gunakan PREC, RASSOC, FUNCS untuk panduan
    return output

# ── Evaluasi postfix (implementasikan) ───────────────────────────
def eval_postfix(tokens: List[str], var_table: Dict[str, float]) -> float:
    """
    Evaluasi token postfix menggunakan Stack Linked List.
    Lookup variabel dari var_table (BST dalam implementasi penuh).
    Big-O: O(n).
    """
stack = Stack()
for tok in tokens:
    if tok in FUNCS:
    # TODO: pop satu operand, terapkan fungsi, push hasil
    pass
elif tok in PREC: # operator binary
    # TODO: pop dua operand, hitung, push hasil
    # Perhatian: urutan pop! b = pop(), a = pop() → a OP b
    pass
elif tok.replace('.','',1).lstrip('-').isdigit():
    stack.push(float(tok))
else: # variabel
    val = var_table.get(tok)
    if val is None: raise ValueError(f'Variabel {tok!r} belum di-SET')
    stack.push(val)
result = stack.pop()
if not stack.is_empty(): raise ValueError('Ekspresi tidak valid')
return result

# ── Expression Tree Node ─────────────────────────────────────────
class ExprNode:
    def __init__(self, val: str):
    self.val = val
    self.left: Optional['ExprNode'] = None
    self.right: Optional['ExprNode'] = None

# ── Bangun Expression Tree dari postfix (implementasikan) ─────────
def build_expr_tree(postfix: List[str]) -> Optional[ExprNode]:
    """Big-O: O(n)."""
    stack = Stack()
    for tok in postfix:
        node = ExprNode(tok)
        if tok in PREC:
# TODO: pop right lalu left, set sebagai anak node
    pass
elif tok in FUNCS:
    # TODO: pop satu anak (right)
    pass
    stack.push(node)
return stack.pop()

# ── Traversal Expression Tree (implementasikan) ───────────────────
def inorder_expr(root: Optional[ExprNode]) -> str:
    """Kembalikan ekspresi infix (dengan kurung untuk kejelasan)."""
    # TODO: implementasikan rekursif
pass
def preorder_expr(root: Optional[ExprNode]) -> List[str]:
    # TODO: implementasikan
pass
    def postorder_expr(root: Optional[ExprNode]) -> List[str]:
    # TODO: implementasikan
    pass

# ── BST Tabel Variabel (implementasikan) ─────────────────────────
class VarBSTNode:
    def __init__(self, key: str, val: float):
        self.key = key; self.val = val
        self.left = self.right = None
class VarBST:
    def __init__(self): self.root = None
    def set(self, key: str, val: float): pass # TODO
    def get(self, key: str) -> Optional[float]: pass # TODO
    def delete(self, key: str): pass # TODO
    def list_all(self) -> List[Tuple[str,float]]: pass # TODO inorder

    # ── Graph DAG Dependensi Formula (implementasikan) ────────────────
class FormulaDAG:
    def __init__(self):
        self.adj: Dict[str, List[str]] = {} # formula -> [depends_on]
        self.formulas: Dict[str, str] = {} # nama -> ekspresi

    def define(self, nama: str, ekspresi: str, deps: List[str]) -> None:
    """Tambahkan formula dan dependensinya."""
    # TODO: deteksi siklus, tambahkan ke adj dan formulas
    pass
def topological_sort(self) -> List[str]:
    """
    Urutan evaluasi valid (DFS-based).
    Big-O: O(V+E).
    Raise ValueError jika ada siklus.
    """
# TODO: implementasikan Kahn's algorithm atau DFS topo sort
pass

# ── Contoh ekspresi uji ───────────────────────────────────────────
TEST_EXPRS = [
    ('(a + b) * c', {'a': 2.0, 'b': 3.0, 'c': 4.0}), # hasil: 20.0
    ('a ^ 2 + b ^ 2', {'a': 3.0, 'b': 4.0}), # hasil: 25.0
    ('sin(a) + cos(b)', {'a': 0.0, 'b': 0.0}), # hasil: 1.0
    ('sqrt(a * a + b * b)', {'a': 3.0, 'b': 4.0}), # hasil: 5.0
    ('(a + b) * (a - b)', {'a': 5.0, 'b': 3.0}), # hasil: 16.0
    ('log(a) + sqrt(b)', {'a': math.e, 'b': 16.0}), # hasil: 5.0
    ('a * b + b * c + c * a', {'a': 1.0,'b': 2.0,'c': 3.0}), # hasil: 11.0
    ('(a + b) ^ 2', {'a': 2.0, 'b': 3.0}), # hasil: 25.0
    ('abs(a - b) * c', {'a': 1.0, 'b': 4.0, 'c': 2.0}), # hasil: 6.0
    ('a / (b + c)', {'a': 10.0, 'b': 2.0, 'c': 3.0}), # hasil: 2.0
]
# ── Main CLI (implementasikan) ────────────────────────────────────
def main():
    var_bst = VarBST()
    formula_dag = FormulaDAG()
    history_stack = Stack() # menyimpan 10 ekspresi terakhir
    print('Academic Expression Evaluator Ketik BANTUAN untuk daftar perintah')
print(f'Menjalankan {len(TEST_EXPRS)} ekspresi uji...')
for expr, vals in TEST_EXPRS:
    # Set variabel ke BST
    for k, v in vals.items(): var_bst.set(k, v)
    # TODO: tokenize → infix_to_postfix → build_expr_tree → eval_tree
    pass
# TODO: implementasikan loop CLI
if __name__ == '__main__':
    main()

