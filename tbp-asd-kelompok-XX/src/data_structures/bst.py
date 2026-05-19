MODUL 3: BST Tabel Variabel (SATU-SATUNYA BST DALAM PROGRAM)
Binary Search Tree untuk menyimpan variabel dengan kunci (a-z)
"""

from typing import Optional, List, Tuple


class VarBSTNode:
    """NODE UNTUK BST"""
    __slots__ = ('key', 'val', 'left', 'right')
    def __init__(self, key: str, val: float):
        self.key = key      # Kunci: huruf a-z (unique)
        self.val = val      # Nilai: float
        self.left = None    # Anak kiri (key lebih kecil)
        self.right = None   # Anak kanan (key lebih besar)


class VarBST:
    """
    BINARY SEARCH TREE (BST) untuk menyimpan variabel
    Property BST: left.key < node.key < right.key
    """
    def __init__(self):
        self.root = None    # Akar pohon

    # ========== INSERT / UPDATE ==========
    def set(self, key: str, val: float) -> None:
        """SET <var> <nilai> - O(log n)"""
        if not isinstance(key, str) or len(key) != 1 or not key.isalpha():
            raise ValueError("Nama variabel harus satu huruf a-z")
        self.root = self._set(self.root, key, val)

    def _set(self, node: Optional[VarBSTNode], key: str, val: float) -> VarBSTNode:
        if node is None:
            return VarBSTNode(key, val)     # Leaf baru
        
        if key < node.key:
            node.left = self._set(node.left, key, val)   # Ke kiri
        elif key > node.key:
            node.right = self._set(node.right, key, val) # Ke kanan
        else:
            node.val = val   # Update nilai jika key sudah ada
        
        return node

    # ========== SEARCH ==========
    def get(self, key: str) -> Optional[float]:
        """GET <var> - O(log n)"""
        node = self._get(self.root, key)
        return node.val if node else None

    def _get(self, node: Optional[VarBSTNode], key: str) -> Optional[VarBSTNode]:
        if node is None or node.key == key:
            return node
        
        if key < node.key:
            return self._get(node.left, key)    # Cari di kiri
        else:
            return self._get(node.right, key)   # Cari di kanan

    # ========== DELETE ==========
    def delete(self, key: str) -> None:
        """DELETE <var> - O(log n)"""
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[VarBSTNode], key: str) -> Optional[VarBSTNode]:
        if node is None:
            return None
        
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Ketemu node yang akan dihapus!
            
            # Case 1: Tidak punya anak
            if node.left is None and node.right is None:
                return None
            
            # Case 2: Punya 1 anak
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            
            # Case 3: Punya 2 anak
            # Cari successor (node paling kiri dari subtree kanan)
            succ = self._min(node.right)
            node.key = succ.key
            node.val = succ.val
            node.right = self._delete(node.right, succ.key)
        
        return node

    def _min(self, node: VarBSTNode) -> VarBSTNode:
        """Cari node dengan key terkecil"""
        while node.left:
            node = node.left
        return node

    # ========== TRAVERSAL ==========
    def list_all(self) -> List[Tuple[str, float]]:
        """LIST - Inorder traversal = hasil TERURUT O(n)"""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[VarBSTNode], out: List[Tuple[str, float]]) -> None:
        """Inorder: kiri → node → kanan (menghasilkan urutan ascending)"""
        if node:
            self._inorder(node.left, out)
            out.append((node.key, node.val))
            self._inorder(node.right, out)

MODUL 6: CLI - Menggunakan berbagai struktur data
"""
def tokenize(expr : str) -> list:
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
    
def print_help():
    print("""
================================================================================
PERINTAH YANG TERSEDIA (CLI Kalkulator Teknik)
================================================================================
  SET <var> <nilai>          - Simpan nilai ke variabel (huruf a-z)
  GET <var>                  - Tampilkan nilai variabel
  DELETE <var>               - Hapus variabel
  LIST                       - Tampilkan semua variabel (terurut BST)
  EVAL <ekspresi>            - Evaluasi ekspresi infix (+, -, *, /, ^, sin, cos, dll)
  TREE <ekspresi>            - Tampilkan pohon ekspresi (inorder, preorder, postorder)
  DEFINE <nama> = <ekspresi> - Definisikan formula (dengan dependensi)
  SHOW_FORMULAS              - Lihat semua formula dan dependensinya
  EVAL_FORMULA <nama>        - Evaluasi formula yang sudah didefinisikan
  HELP                       - Tampilkan bantuan ini
  EXIT                       - Keluar program
================================================================================
""")

def main():
    var_bst = VarBST()
    formula_dag = FormulaDAG()

    print("\n" + "="*70)
    print("   AKADEMIK EXPRESSION EVALUATOR & FORMULA SCHEDULER")
    print("="*70)


    print("\n--- MENJALANKAN 10 EKSPRESI UJI (OTOMATIS) ---")
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
        for var, val in var_vals.items():
            var_bst.set(var, val)

        tokens = tokenize(expr)
        postfix = infix_to_postfix(token)
        result = eval_postfix(postfix, var_vals)
        tree = build_expr_tree(postfix)
        tree_res = eval_tree(tree, var_vals)

        var_str = ", ".join(f"{k}={v}" for k, v in var_vals.items())
        print(f"   EVAL {expr:25s} [dengan {var_str}] = {result} (tree: {tree_res})")
    print("--- SELESAI UJI OTOMATIS ---\n")

    print("Ketik HELP untuk daftar perintah.\n")

     while True:
        try:
            cmd_line = input(">>> ").strip()
            if not cmd_line:
                continue
            
            parts = cmd_line.split(maxsplit=1)
            cmd = parts[0].upper()
            
            if cmd == "EXIT":
                print("Goodbye!")
                break
            elif cmd == "HELP":
                print_help()
            elif cmd == "SET":
                if len(parts) != 2:
                    print("Usage: SET <var> <value>")
                    continue
                sub = parts[1].split()
                if len(sub) != 2:
                    print("Usage: SET <var> <value>")
                    continue
                var_name = sub[0]
                try:
                    value = float(sub[1])
                except ValueError:
                    print("Nilai harus angka")
                    continue
                 try:
                    var_bst.set(var_name, value)
                    print(f"{var_name} = {value}")
                except ValueError as e:
                    print(e)
                    
            elif cmd == "GET":
                if len(parts) != 2:
                    print("Usage: GET <var>")
                    continue
                var_name = parts[1].strip()
                val = var_bst.get(var_name)
                if val is None:
                    print(f"Variabel '{var_name}' belum di-SET")
                else:
                    print(f"{var_name} = {val}")
                    
            elif cmd == "DELETE":
                if len(parts) != 2:
                    print("Usage: DELETE <var>")
                    continue
                var_name = parts[1].strip()
                var_bst.delete(var_name)
                print(f"Deleted {var_name}")
                
            elif cmd == "LIST":
                vars_list = var_bst.list_all()
                if not vars_list:
                    print("Tidak ada variabel.")
                else:
                    for k, v in vars_list:
                        print(f"{k} = {v}")
                        
            elif cmd == "EVAL":
                if len(parts) != 2:
                    print("Usage: EVAL <expression>")
                    continue
                expr_str = parts[1]
                try:
                    tokens = tokenize(expr_str)
                    postfix = infix_to_postfix(tokens)
                    var_dict = {k: v for k, v in var_bst.list_all()}
                    result = eval_postfix(postfix, var_dict)
                    print(f"Result: {result}")
                except Exception as e:
                    print(f"Error: {e}")
                    
            elif cmd == "TREE":
                if len(parts) != 2:
                    print("Usage: TREE <expression>")
                    continue
                expr_str = parts[1]
                try:
                    tokens = tokenize(expr_str)
                    postfix = infix_to_postfix(tokens)
                    tree = build_expr_tree(postfix)
                    print("Inorder (infix):   ", inorder_expr(tree))
                    print("Preorder (prefix): ", " ".join(preorder_expr(tree)))
                    print("Postorder (postfix):", " ".join(postorder_expr(tree)))
                except Exception as e:
                    print(f"Error: {e}")
                    
            elif cmd == "DEFINE":
                if len(parts) != 2:
                    print("Usage: DEFINE <name> = <expression>")
                    continue
                def_part = parts[1].strip()
                if '=' not in def_part:
                    print("Missing '='. Usage: DEFINE name = expr")
                    continue
                name_part, expr_part = def_part.split('=', 1)
                name = name_part.strip()
                expr = expr_part.strip()
                if not name or not expr:
                    print("Definisi tidak valid")
                    continue
                if name in FUNCS:
                    print("Nama tidak boleh sama dengan fungsi bawaan")
                    continue
                try:
                    formula_dag.define(name, expr)
                    print(f"Formula '{name}' didefinisikan: {expr}")
                except Exception as e:
                    print(f"Definisi gagal: {e}")
                    
            elif cmd == "SHOW_FORMULAS":
                if not formula_dag.formulas:
                    print("Belum ada formula didefinisikan.")
                else:
                    print("Daftar formula:")
                    for name, expr in formula_dag.formulas.items():
                      
                        deps = []
                        for dep, targets in formula_dag.graph.items():
                            if name in targets:
                                deps.append(dep)
                        deps_str = ", ".join(deps) if deps else "tidak ada"
                        print(f"  {name} = {expr}  (bergantung pada: {deps_str})")
                        
            elif cmd == "EVAL_FORMULA":
                if len(parts) != 2:
                    print("Usage: EVAL_FORMULA <formula_name>")
                    continue
                fname = parts[1].strip()
                if fname not in formula_dag.formulas:
                    print(f"Formula '{fname}' tidak ditemukan")
                    continue
                try:
                    var_dict = {k: v for k, v in var_bst.list_all()}
                    result = formula_dag.evaluate_one(fname, var_dict)
                    print(f"{fname} = {result}")
                except Exception as e:
                    print(f"Evaluasi error: {e}")
                    
            else:
                print(f"Perintah tidak dikenal: {cmd}. Ketik HELP.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except EOFError:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()

