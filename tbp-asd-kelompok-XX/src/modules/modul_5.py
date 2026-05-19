class FormulaDAG:
    """
    DAG untuk menyimpan formula dan dependensinya.
    Node = nama formula, Edge (A→B) = formula A bergantung pada hasil formula B.
    Big-O: O(V+E) untuk topological sort
    """
    def __init__(self):
        self.adj: Dict[str, List[str]] = {}          # adjacency list
        self.formulas: Dict[str, str] = {}           # nama -> ekspresi
        self.trees: Dict[str, ExprNode] = {}         # nama -> expression tree

    def _extract_dependencies(self, expr: str) -> Set[str]:
        """Ekstrak nama variabel/formula dari ekspresi (tanpa fungsi bawaan)"""
        tokens = tokenize(expr)
        deps = set()
        for tok in tokens:
            if tok.isalpha() and tok not in FUNCS:
                deps.add(tok)
        return deps

    def define(self, name: str, expr: str) -> None:
        """DEFINE <nama_formula> = <ekspresi> - Definisikan formula dengan dependensi"""
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        tree = build_expr_tree(postfix)
        deps = self._extract_dependencies(expr)
        deps.discard(name)  # self-loop tidak diizinkan
        
        self.adj[name] = list(deps)
        self.formulas[name] = expr
        self.trees[name] = tree
        
        # Validasi tidak ada siklus
        try:
            self.topological_sort()
        except ValueError as e:
            del self.adj[name]
            del self.formulas[name]
            del self.trees[name]
            raise ValueError(f"Siklus terdeteksi pada '{name}': {e}")

    def topological_sort(self) -> List[str]:
        """
        Kahn's algorithm untuk topological sort.
        Menentukan urutan evaluasi formula.
        Big-O: O(V+E)
        """
        in_degree = {u: 0 for u in self.adj}
        for u in self.adj:
            for v in self.adj[u]:
                if v not in in_degree:
                    in_degree[v] = 0
        for u in self.adj:
            for v in self.adj[u]:
                if v in in_degree:
                    in_degree[v] += 1
        
        q = deque([u for u, d in in_degree.items() if d == 0])
        order = []
        
        while q:
            u = q.popleft()
            order.append(u)
            for v in self.adj.get(u, []):
                if v in in_degree:
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        q.append(v)
        
        if len(order) != len(in_degree):
            raise ValueError("Siklus dependensi terdeteksi")
        return order

    def get_schedule(self) -> List[str]:
        """SCHEDULE - Mengembalikan urutan evaluasi formula (topological sort)"""
        return self.topological_sort()

    def evaluate_one(self, name: str, var_table: Dict[str, float]) -> float:
        """Evaluasi formula berdasarkan nama, dengan memoization"""
        memo = {}
        
        def eval_rec(n: str) -> float:
            if n in memo:
                return memo[n]
            if n not in self.trees:
                raise ValueError(f"Formula '{n}' tidak terdefinisi")
            local = {**var_table, **memo}
            res = eval_tree(self.trees[n], local)
            memo[n] = res
            return res
        
        return eval_rec(name)

    def get_all_formulas(self) -> Dict[str, str]:
        """Mengembalikan semua formula yang terdefinisi"""
        return self.formulas.copy()

    def get_dependencies(self, name: str) -> List[str]:
        """Mengembalikan dependensi suatu formula"""
        return self.adj.get(name, []).copy()
