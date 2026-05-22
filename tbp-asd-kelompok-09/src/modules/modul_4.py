class ExprNode:
    """Node untuk Expression Tree"""
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val: str):
        self.val = val
        self.left = None
        self.right = None


def build_expr_tree(postfix: List[str]) -> Optional[ExprNode]:
    """
    Membangun expression tree dari token postfix.
    Node internal = operator/fungsi, node daun = operand/variabel.
    Big-O: O(n)
    """
    stack = Stack()
    
    for tok in postfix:
        node = ExprNode(tok)
        if tok in PREC:
            right = stack.pop()
            left = stack.pop()
            if left is None or right is None:
                raise ValueError("Postfix tidak valid untuk tree")
            node.left = left
            node.right = right
        elif tok in FUNCS:
            child = stack.pop()
            if child is None:
                raise ValueError("Argumen fungsi kurang")
            node.left = child
        stack.push(node)
    
    root = stack.pop()
    if not stack.is_empty():
        raise ValueError("Postfix tidak valid")
    return root


def inorder_expr(root: Optional[ExprNode]) -> str:
    """Traversal inorder - menghasilkan ekspresi infix dengan kurung"""
    if root is None:
        return ""
    if root.val in PREC:
        left = inorder_expr(root.left)
        right = inorder_expr(root.right)
        return f"({left} {root.val} {right})"
    elif root.val in FUNCS:
        child = inorder_expr(root.left)
        return f"{root.val}({child})"
    else:
        return root.val


def preorder_expr(root: Optional[ExprNode]) -> List[str]:
    """Traversal preorder - prefix notation"""
    if root is None:
        return []
    result = [root.val]
    if root.left:
        result.extend(preorder_expr(root.left))
    if root.right:
        result.extend(preorder_expr(root.right))
    return result


def postorder_expr(root: Optional[ExprNode]) -> List[str]:
    """Traversal postorder - postfix notation"""
    if root is None:
        return []
    result = []
    if root.left:
        result.extend(postorder_expr(root.left))
    if root.right:
        result.extend(postorder_expr(root.right))
    result.append(root.val)
    return result


def eval_tree(root: Optional[ExprNode], var_table: Dict[str, float]) -> float:
    """Evaluasi rekursif dari expression tree"""
    if root is None:
        raise ValueError("Tree kosong")
    
    if root.val in PREC:
        left_val = eval_tree(root.left, var_table)
        right_val = eval_tree(root.right, var_table)
        op = root.val
        if op == '+':
            return left_val + right_val
        elif op == '-':
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            if right_val == 0:
                raise ZeroDivisionError("Pembagian nol")
            return left_val / right_val
        elif op == '^':
            return left_val ** right_val
    
    elif root.val in FUNCS:
        arg = eval_tree(root.left, var_table)
        if root.val == 'sin':
            return math.sin(arg)
        elif root.val == 'cos':
            return math.cos(arg)
        elif root.val == 'sqrt':
            if arg < 0:
                raise ValueError("sqrt negatif")
            return math.sqrt(arg)
        elif root.val == 'log':
            if arg <= 0:
                raise ValueError("log non-positif")
            return math.log(arg)
        elif root.val == 'abs':
            return abs(arg)
    
    else:
        try:
            return float(root.val)
        except ValueError:
            if root.val not in var_table:
                raise ValueError(f"Variabel '{root.val}' belum di-SET")
            return var_table[root.val]
    
    raise ValueError(f"Node tak dikenal: {root.val}")
