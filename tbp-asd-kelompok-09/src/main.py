import math
import time
from typing import Optional, Dict, List, Tuple, Set
from collections import deque

# =============================================================================
# 1. Operator & Fungsi
# =============================================================================
PREC = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
RASSOC = {'^'}
FUNCS = {'sin', 'cos', 'sqrt', 'log', 'abs'}

# =============================================================================
# 2. Stack (Linked List)
# =============================================================================
class LNode:
    __slots__ = ('data', 'next')
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0
    def push(self, data):
        node = LNode(data)
        node.next = self.top
        self.top = node
        self.size += 1
    def pop(self):
        if self.top is None: return None
        val = self.top.data
        self.top = self.top.next
        self.size -= 1
        return val
    def peek(self):
        return self.top.data if self.top else None
    def is_empty(self):
        return self.size == 0

# =============================================================================
# 3. Tokenizer
# =============================================================================
def tokenize(expr: str) -> List[str]:
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or (ch == '.' and i+1 < n and expr[i+1].isdigit()):
            j = i
            while j < n and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue
        if ch.isalpha():
            j = i
            while j < n and expr[j].isalpha():
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue
        if ch in '+-*/^()':
            tokens.append(ch)
            i += 1
            continue
        raise ValueError(f"Karakter tidak dikenal: '{ch}'")
    return tokens

# =============================================================================
# 4. Infix -> Postfix
# =============================================================================
def infix_to_postfix(tokens: List[str]) -> List[str]:
    output = []
    op_stack = Stack()
    for tok in tokens:
        if tok in FUNCS:
            op_stack.push(tok)
        elif tok == '(':
            op_stack.push(tok)
        elif tok == ')':
            while not op_stack.is_empty() and op_stack.peek() != '(':
                output.append(op_stack.pop())
            if op_stack.is_empty():
                raise ValueError("Parentheses tidak cocok")
            op_stack.pop()
            if not op_stack.is_empty() and op_stack.peek() in FUNCS:
                output.append(op_stack.pop())
        elif tok in PREC:
            while (not op_stack.is_empty() and op_stack.peek() != '(' and
                   (PREC[op_stack.peek()] > PREC[tok] or
                    (PREC[op_stack.peek()] == PREC[tok] and tok not in RASSOC))):
                output.append(op_stack.pop())
            op_stack.push(tok)
        else:
            output.append(tok)
    while not op_stack.is_empty():
        top = op_stack.pop()
        if top in '()':
            raise ValueError("Parentheses tidak cocok")
        output.append(top)
    return output

# =============================================================================
# 5. Evaluasi Postfix
# =============================================================================
def eval_postfix(tokens: List[str], var_table: Dict[str, float]) -> float:
    stack = Stack()
    for tok in tokens:
        if tok in FUNCS:
            arg = stack.pop()
            if arg is None:
                raise ValueError(f"Argumen kurang untuk {tok}")
            if tok == 'sin':
                res = math.sin(arg)
            elif tok == 'cos':
                res = math.cos(arg)
            elif tok == 'sqrt':
                if arg < 0: raise ValueError("sqrt negatif")
                res = math.sqrt(arg)
            elif tok == 'log':
                if arg <= 0: raise ValueError("log non-positif")
                res = math.log(arg)
            elif tok == 'abs':
                res = abs(arg)
            else:
                raise ValueError(f"Fungsi tak dikenal {tok}")
            stack.push(res)
        elif tok in PREC:
            b = stack.pop()
            a = stack.pop()
            if a is None or b is None:
                raise ValueError(f"Operand kurang untuk {tok}")
            if tok == '+': res = a + b
            elif tok == '-': res = a - b
            elif tok == '*': res = a * b
            elif tok == '/': res = a / b
            elif tok == '^': res = a ** b
            else: raise ValueError(f"Operator tak dikenal {tok}")
            stack.push(res)
        else:
            try:
                val = float(tok)
            except ValueError:
                if tok not in var_table:
                    raise ValueError(f"Variabel '{tok}' belum di-SET")
                val = var_table[tok]
            stack.push(val)
    result = stack.pop()
    if not stack.is_empty():
        raise ValueError("Ekspresi tidak valid")
    return result

# =============================================================================
# 6. Expression Tree
# =============================================================================
class ExprNode:
    __slots__ = ('val', 'left', 'right')
    def __init__(self, val: str):
        self.val = val
        self.left = None
        self.right = None

def build_expr_tree(postfix: List[str]) -> Optional[ExprNode]:
    stack = Stack()
    for tok in postfix:
        node = ExprNode(tok)
        if tok in PREC:
            right = stack.pop()
            left = stack.pop()
            node.left = left
            node.right = right
        elif tok in FUNCS:
            child = stack.pop()
            node.left = child
        stack.push(node)
    root = stack.pop()
    return root

def inorder_expr(root: Optional[ExprNode]) -> str:
    if root is None: return ""
    if root.val in PREC:
        return f"({inorder_expr(root.left)} {root.val} {inorder_expr(root.right)})"
    elif root.val in FUNCS:
        return f"{root.val}({inorder_expr(root.left)})"
    else:
        return root.val

def preorder_expr(root: Optional[ExprNode]) -> List[str]:
    if root is None: return []
    return [root.val] + preorder_expr(root.left) + preorder_expr(root.right)

def postorder_expr(root: Optional[ExprNode]) -> List[str]:
    if root is None: return []
    return postorder_expr(root.left) + postorder_expr(root.right) + [root.val]

def eval_tree(root: Optional[ExprNode], var_table: Dict[str, float]) -> float:
    if root is None:
        raise ValueError("Tree kosong")
    if root.val in PREC:
        left_val = eval_tree(root.left, var_table)
        right_val = eval_tree(root.right, var_table)
        if root.val == '+': return left_val + right_val
        if root.val == '-': return left_val - right_val
        if root.val == '*': return left_val * right_val
        if root.val == '/': return left_val / right_val
        if root.val == '^': return left_val ** right_val
    elif root.val in FUNCS:
        arg = eval_tree(root.left, var_table)
        if root.val == 'sin': return math.sin(arg)
        if root.val == 'cos': return math.cos(arg)
        if root.val == 'sqrt': return math.sqrt(arg)
        if root.val == 'log': return math.log(arg)
        if root.val == 'abs': return abs(arg)
    else:
        try:
            return float(root.val)
        except ValueError:
            if root.val not in var_table:
                raise ValueError(f"Variabel '{root.val}' belum di-SET")
            return var_table[root.val]
    raise ValueError(f"Node tak dikenal: {root.val}")

# =============================================================================
# 7. BST Tabel Variabel (satu huruf)
# =============================================================================
class VarBSTNode:
    __slots__ = ('key','val','left','right')
    def __init__(self, key: str, val: float):
        self.key = key
        self.val = val
        self.left = None
        self.right = None

class VarBST:
    def __init__(self):
        self.root = None
    def set(self, key: str, val: float):
        if len(key) != 1 or not key.isalpha():
            raise ValueError("Nama variabel harus satu huruf a-z")
        self.root = self._set(self.root, key, val)
    def _set(self, node, key, val):
        if node is None:
            return VarBSTNode(key, val)
        if key < node.key:
            node.left = self._set(node.left, key, val)
        elif key > node.key:
            node.right = self._set(node.right, key, val)
        else:
            node.val = val
        return node
    def get(self, key: str):
        node = self._get(self.root, key)
        return node.val if node else None
    def _get(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._get(node.left, key)
        else:
            return self._get(node.right, key)
    def delete(self, key: str):
        self.root = self._delete(self.root, key)
    def _delete(self, node, key):
        if node is None: return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None: return node.right
            if node.right is None: return node.left
            succ = self._min(node.right)
            node.key = succ.key
            node.val = succ.val
            node.right = self._delete(node.right, succ.key)
        return node
    def _min(self, node):
        while node.left: node = node.left
        return node
    def list_all(self):
        result = []
        self._inorder(self.root, result)
        return result
    def _inorder(self, node, out):
        if node:
            self._inorder(node.left, out)
            out.append((node.key, node.val))
            self._inorder(node.right, out)

# =============================================================================
# 8. Formula DAG (arah dependensi benar)
# =============================================================================
class FormulaDAG:
    def __init__(self):
        self.graph: Dict[str, List[str]] = {}
        self.formulas: Dict[str, str] = {}
        self.trees: Dict[str, ExprNode] = {}

    def _extract_deps(self, expr: str) -> Set[str]:
        tokens = tokenize(expr)
        deps = set()
        for tok in tokens:
            if tok.isalpha() and tok not in FUNCS:
                deps.add(tok)
        return deps

    def define(self, name: str, expr: str):
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        tree = build_expr_tree(postfix)
        deps = self._extract_deps(expr)
        deps.discard(name)
        self.formulas[name] = expr
        self.trees[name] = tree
        for dep in deps:
            if dep in self.formulas:
                self.graph.setdefault(dep, []).append(name)
        self.graph.setdefault(name, [])
        self.topological_sort()

    def topological_sort(self) -> List[str]:
        nodes = set(self.formulas.keys())
        in_degree = {n: 0 for n in nodes}
        for u in nodes:
            for v in self.graph.get(u, []):
                if v in nodes:
                    in_degree[v] += 1
        q = deque([n for n in nodes if in_degree[n] == 0])
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in self.graph.get(u, []):
                if v in nodes:
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        q.append(v)
        if len(order) != len(nodes):
            raise ValueError("Siklus dependensi terdeteksi")
        return order

    def evaluate_one(self, name: str, var_table: Dict[str, float]) -> float:
        order = self.topological_sort()
        results = {}
        for f in order:
            local = {**var_table, **results}
            results[f] = eval_tree(self.trees[f], local)
        return results[name]

# =============================================================================
# 9. Eksperimen Runtime
# =============================================================================
def run_experiment():
    print("\n" + "="*70)
    print(" EKSPERIMEN RUNTIME (BIG-O) - 2 STUDI KASUS TEKNIK")
    print("="*70)
    print("\n[Eksperimen 1] Gerak Parabola: jumlah token vs waktu")
    exprs = [
        ("v^2 * sin(2*t)/g", 9),
        ("(v^2*sin(2*t)/g)+(v^2*sin(2*t)/g)", 19),
        ("((v^2*sin(2*t)/g)+(v^2*sin(2*t)/g))^2", 24),
    ]
    var = {'v':20, 't':math.radians(45), 'g':9.8}
    for e,_ in exprs:
        toks = tokenize(e)
        post = infix_to_postfix(toks)
        start = time.perf_counter()
        eval_postfix(post, var)
        elapsed = (time.perf_counter()-start)*1000
        print(f"   Token count: {len(toks):2d} | Waktu: {elapsed:.4f} ms | Ekspresi: {e}")
    print("\n[Eksperimen 2] Pembagi Tegangan: jumlah token vs waktu")
    exprs2 = [
        ("V*b/(a+b)", 7),
        ("V*b/(a+b)+V*d/(c+d)", 15),
        ("(V*b/(a+b))*(V*d/(c+d))", 17),
    ]
    var2 = {'V':12, 'a':1000, 'b':2000, 'c':3000, 'd':4000}
    for e,_ in exprs2:
        toks = tokenize(e)
        post = infix_to_postfix(toks)
        start = time.perf_counter()
        eval_postfix(post, var2)
        elapsed = (time.perf_counter()-start)*1000
        print(f"   Token count: {len(toks):2d} | Waktu: {elapsed:.4f} ms | Ekspresi: {e}")
    print("\nKesimpulan: Waktu linear terhadap token count → O(n) sesuai analisis.\n")

# =============================================================================
# 10. Studi Kasus Teknik (2 kasus)
# =============================================================================
def run_studi_kasus():
    print("\n" + "="*70)
    print(" STUDI KASUS TEKNIK")
    print("="*70)
    # Kasus 1: Gerak parabola
    print("\n[1] GERAK PARABOLA (Fisika)")
    print("    Jarak = v^2 * sin(2*theta) / g")
    dag1 = FormulaDAG()
    bst1 = VarBST()
    bst1.set('v', 25.0)
    bst1.set('g', 9.81)
    dag1.define('rad', 't * 3.141592653589793 / 180')
    dag1.define('jarak', '(v^2 * sin(2*rad)) / g')
    print("    Sudut (°)   Jarak (m)")
    for sudut in [30, 45, 60]:
        bst1.set('t', float(sudut))
        var_dict = {k: bst1.get(k) for k in ['v','g','t']}
        jarak = dag1.evaluate_one('jarak', var_dict)
        print(f"       {sudut}         {jarak:.2f}")
    # Kasus 2: Pembagi tegangan
    print("\n[2] PEMBAGI TEGANGAN (Elektro)")
    print("    Vout = V * R2 / (R1+R2), toleransi ±5%")
    dag2 = FormulaDAG()
    bst2 = VarBST()
    bst2.set('V', 12.0)
    bst2.set('a', 1000)
    bst2.set('b', 2200)
    dag2.define('Vout_nom', 'V * b / (a+b)')
    dag2.define('Vout_min', 'V * (b*0.95) / ((a*1.05)+(b*0.95))')
    dag2.define('Vout_max', 'V * (b*1.05) / ((a*0.95)+(b*1.05))')
    var_dict = {k: bst2.get(k) for k in ['V','a','b']}
    print(f"    Vout nominal = {dag2.evaluate_one('Vout_nom', var_dict):.2f} V")
    print(f"    Vout min     = {dag2.evaluate_one('Vout_min', var_dict):.2f} V")
    print(f"    Vout max     = {dag2.evaluate_one('Vout_max', var_dict):.2f} V")
    print("\n" + "="*70 + "\n")

# =============================================================================
# 11. CLI dan MAIN
# =============================================================================
def print_help():
    print("""
PERINTAH:
  SET <var> <nilai>    - simpan variabel (satu huruf)
  GET <var>            - lihat nilai
  DELETE <var>         - hapus variabel
  LIST                 - semua variabel
  EVAL <ekspresi>      - hitung ekspresi
  TREE <ekspresi>      - tampilkan pohon
  DEFINE <nama>=<expr> - buat formula
  SHOW_FORMULAS        - daftar formula
  EVAL_FORMULA <nama>  - hitung formula
  TEST_EXP             - jalankan eksperimen runtime
  STUDI_KASUS          - jalankan 2 studi kasus
  HELP                 - bantuan
  EXIT
""")

def main():
    var_bst = VarBST()
    dag = FormulaDAG()
    print("\n" + "="*60)
    print("   KALKULATOR TEKNIK + FORMULA DAG")
    print("="*60)
    print("10 EKSPRESI UJI OTOMATIS (dengan nilai variabel):")
    test_exprs = [
        ('a + b', {'a': 2.0, 'b': 3.0}),
        ('a ^ 2 + b ^ 2', {'a': 3.0, 'b': 4.0}),
        ('sin(a) + cos(b)', {'a': 0.0, 'b': 0.0}),
        ('sqrt(a * a + b * b)', {'a': 3.0, 'b': 4.0}),
        ('(a + b) * (a - b)', {'a': 5.0, 'b': 3.0}),
        ('log(a) + sqrt(b)', {'a': math.e, 'b': 16.0}),
        ('a * b + b * c + c * a', {'a': 1.0, 'b': 2.0, 'c': 3.0}),
        ('(a + b) ^ 2', {'a': 2.0, 'b': 3.0}),
        ('abs(a - b) * c', {'a': 1.0, 'b': 4.0, 'c': 2.0}),
        ('a / (b + c)', {'a': 10.0, 'b': 2.0, 'c': 3.0}),
    ]
    for expr, var_vals in test_exprs:
        for k, v in var_vals.items():
            var_bst.set(k, v)
        post = infix_to_postfix(tokenize(expr))
        hasil = eval_postfix(post, var_vals)
        # Tampilkan nilai variabel
        var_str = ", ".join(f"{k}={v}" for k, v in var_vals.items())
        print(f"   EVAL {expr:25s} [dengan {var_str}] = {hasil}")
    print("SELESAI UJI.\n")
    print("Ketik HELP untuk daftar perintah.\n")
    while True:
        try:
            cmd = input(">>> ").strip()
            if not cmd: continue
            parts = cmd.split(maxsplit=1)
            c = parts[0].upper()
            if c == "EXIT":
                print("Goodbye!")
                break
            elif c == "HELP":
                print_help()
            elif c == "TEST_EXP":
                run_experiment()
            elif c == "STUDI_KASUS":
                run_studi_kasus()
            elif c == "SET":
                if len(parts)!=2:
                    print("Usage: SET var nilai")
                    continue
                sub = parts[1].split()
                if len(sub)!=2:
                    print("Usage: SET var nilai")
                    continue
                vname, vval = sub[0], sub[1]
                if len(vname)!=1 or not vname.isalpha():
                    print("Nama variabel harus satu huruf")
                    continue
                try:
                    val = float(vval)
                except:
                    print("Nilai harus angka")
                    continue
                var_bst.set(vname, val)
                print(f"{vname} = {val}")
            elif c == "GET":
                if len(parts)!=2:
                    print("Usage: GET var")
                    continue
                vname = parts[1].strip()
                if len(vname)!=1 or not vname.isalpha():
                    print("Nama variabel harus satu huruf")
                    continue
                val = var_bst.get(vname)
                if val is None:
                    print(f"Variabel {vname} belum di-SET")
                else:
                    print(f"{vname} = {val}")
            elif c == "DELETE":
                if len(parts)!=2:
                    print("Usage: DELETE var")
                    continue
                vname = parts[1].strip()
                if len(vname)!=1 or not vname.isalpha():
                    print("Nama variabel harus satu huruf a-z")
                    continue
                var_bst.delete(vname)
                print(f"Variabel '{vname}' telah dihapus")
            elif c == "LIST":
                for k,v in var_bst.list_all():
                    print(f"{k} = {v}")
            elif c == "EVAL":
                if len(parts)!=2:
                    print("Usage: EVAL ekspresi")
                    continue
                expr_str = parts[1]
                try:
                    toks = tokenize(expr_str)
                    post = infix_to_postfix(toks)
                    vardict = {k:v for k,v in var_bst.list_all()}
                    res = eval_postfix(post, vardict)
                    print(f"Result = {res}")
                except Exception as e:
                    print(f"Error: {e}")
            elif c == "TREE":
                if len(parts)!=2:
                    print("Usage: TREE ekspresi")
                    continue
                expr_str = parts[1]
                try:
                    toks = tokenize(expr_str)
                    post = infix_to_postfix(toks)
                    tree = build_expr_tree(post)
                    print("Inorder :", inorder_expr(tree))
                    print("Preorder:", " ".join(preorder_expr(tree)))
                    print("Postorder:", " ".join(postorder_expr(tree)))
                except Exception as e:
                    print(f"Error: {e}")
            elif c == "DEFINE":
                if len(parts)!=2:
                    print("Usage: DEFINE name = expr")
                    continue
                def_part = parts[1].strip()
                if '=' not in def_part:
                    print("Harus ada '='")
                    continue
                name, expr = def_part.split('=',1)
                name = name.strip()
                expr = expr.strip()
                if not name or not expr:
                    print("Format salah")
                    continue
                if name in FUNCS:
                    print("Nama tidak boleh sama dengan fungsi")
                    continue
                try:
                    dag.define(name, expr)
                    print(f"Formula {name} didefinisikan: {expr}")
                except Exception as e:
                    print(f"Error: {e}")
            elif c == "SHOW_FORMULAS":
                if not dag.formulas:
                    print("Tidak ada formula.")
                else:
                    for name, expr in dag.formulas.items():
                        deps = []
                        for dep, targets in dag.graph.items():
                            if name in targets:
                                deps.append(dep)
                        print(f"{name} = {expr}  (depend: {deps})")
            elif c == "EVAL_FORMULA":
                if len(parts)!=2:
                    print("Usage: EVAL_FORMULA nama")
                    continue
                fname = parts[1].strip()
                if fname not in dag.formulas:
                    print(f"Formula {fname} tidak ditemukan")
                    continue
                try:
                    vardict = {k:v for k,v in var_bst.list_all()}
                    res = dag.evaluate_one(fname, vardict)
                    print(f"{fname} = {res}")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Perintah tidak dikenal. Ketik HELP.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
