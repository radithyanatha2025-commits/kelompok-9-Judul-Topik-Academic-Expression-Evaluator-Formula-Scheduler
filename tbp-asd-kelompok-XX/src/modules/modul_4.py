class ExprNode:
    def __init__(self, val: str):
        self.val = val
        self.left: Optional['ExprNode'] = None
        self.right: Optional['ExprNode'] = None
 
 
def build_expr_tree(postfix: List[str]) -> Optional[ExprNode]:
    """
    Bangun binary expression tree dari token postfix.
    Node internal = operator/fungsi, node daun = operand/variabel.
    Big-O: O(n) — setiap token diproses tepat sekali.
 
    Algoritma:
    - Angka/variabel → buat node daun, push ke stack
    - Operator biner → pop right & left, buat node dengan 2 anak
    - Fungsi unary   → pop satu anak (right)
    """
    stack = Stack()
 
    for tok in postfix:
        node = ExprNode(tok)
 
        if tok in PREC:
            # Operator biner: pop right dulu, lalu left
            if stack.size() < 2:
                raise ValueError(f'Operator {tok!r} tidak cukup operand untuk tree')
            node.right = stack.pop()
            node.left = stack.pop()
 
        elif tok in FUNCS:
            # Fungsi unary: pop satu anak
            if stack.is_empty():
                raise ValueError(f'Fungsi {tok!r} tidak punya operand untuk tree')
            node.right = stack.pop()
            # node.left = None (tidak ada operand kiri)
 
        # Untuk angka dan variabel, node sudah dibuat tanpa anak
        stack.push(node)
 
    if stack.is_empty():
        return None
    return stack.pop()
 
 
def inorder_expr(root: Optional[ExprNode]) -> str:
    """
    Inorder traversal: menghasilkan ekspresi infix dengan kurung.
    Big-O: O(n) — mengunjungi setiap node tepat sekali.
    Pattern: (left OP right) untuk operator, FUNC(right) untuk fungsi.
    """
    if root is None:
        return ''
 
    # Node daun (operand/variabel)
    if root.left is None and root.right is None:
        return root.val
 
    # Node fungsi unary
    if root.val in FUNCS:
        return f'{root.val}({inorder_expr(root.right)})'
 
    # Node operator biner: tambah kurung untuk kejelasan
    left_str = inorder_expr(root.left)
    right_str = inorder_expr(root.right)
    return f'({left_str} {root.val} {right_str})'
 
 
def preorder_expr(root: Optional[ExprNode]) -> List[str]:
    """
    Preorder traversal: Root → Left → Right (prefix notation).
    Big-O: O(n).
    """
    if root is None:
        return []
    result = [root.val]
    result.extend(preorder_expr(root.left))
    result.extend(preorder_expr(root.right))
    return result
 
 
def postorder_expr(root: Optional[ExprNode]) -> List[str]:
    """
    Postorder traversal: Left → Right → Root (postfix notation).
    Big-O: O(n).
    """
    if root is None:
        return []
    result = []
    result.extend(postorder_expr(root.left))
    result.extend(postorder_expr(root.right))
    result.append(root.val)
    return result
 
 
def eval_tree(root: Optional[ExprNode], var_table: VarBST) -> float:
    """
    Evaluasi rekursif expression tree.
    Big-O: O(n) — mengunjungi setiap node tepat sekali.
 
    Algoritma rekursif:
    - Node daun angka  → konversi ke float
    - Node daun var    → lookup dari BST
    - Node fungsi      → eval anak kanan, terapkan fungsi
    - Node operator    → eval kedua anak, terapkan operator
    """
    if root is None:
        raise ValueError('Tree kosong')
 
    # Angka literal
    if root.val.replace('.', '', 1).lstrip('-').isdigit():
        return float(root.val)
 
    # Variabel
    if root.left is None and root.right is None and root.val not in FUNCS:
        val = var_table.get(root.val)
        if val is None:
            raise ValueError(f"Variabel '{root.val}' belum di-SET")
        return val
 
    # Fungsi unary
    if root.val in FUNCS:
        operand = eval_tree(root.right, var_table)
        try:
            return FUNCS[root.val](operand)
        except Exception as e:
            raise ValueError(f'Error {root.val}({operand}): {e}')
 
    # Operator biner
    if root.val in PREC:
        a = eval_tree(root.left, var_table)
        b = eval_tree(root.right, var_table)
        if root.val == '+': return a + b
        if root.val == '-': return a - b
        if root.val == '*': return a * b
        if root.val == '/':
            if b == 0:
                raise ValueError('Pembagian dengan nol')
            return a / b
        if root.val == '^': return a ** b
 
    raise ValueError(f'Token tidak dikenal di tree: {root.val!r}')
 
 
def print_tree(root: Optional[ExprNode], prefix: str = '', is_left: bool = True) -> str:
    """Cetak tree secara visual. Big-O: O(n)."""
    if root is None:
        return ''
    lines = []
    connector = '├── ' if is_left else '└── '
    lines.append(prefix + connector + root.val)
    child_prefix = prefix + ('│   ' if is_left else '    ')
    if root.left or root.right:
        if root.left:
            lines.append(print_tree(root.left, child_prefix, True))
        if root.right:
            lines.append(print_tree(root.right, child_prefix, False))
    return '\n'.join(lines)
 
