import math
import re
from typing import Optional, Dict, List, Tuple, Set
from collections import deque

# ----------------------------------------------------------------------
# Operator & function definitions
# ----------------------------------------------------------------------
PREC = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
RASSOC = {'^'}
FUNCS = {'sin', 'cos', 'sqrt', 'log', 'abs'}

# ----------------------------------------------------------------------
# Linked List Node & Stack
# ----------------------------------------------------------------------
class LNode:
    __slots__ = ('data', 'next')
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, data) -> None:
        node = LNode(data)
        node.next = self.top
        self.top = node
        self.size += 1

    def pop(self):
        if self.top is None:
            return None
        val = self.top.data
        self.top = self.top.next
        self.size -= 1
        return val

    def peek(self):
        return self.top.data if self.top else None

    def is_empty(self) -> bool:
        return self.size == 0

# ----------------------------------------------------------------------
# Tokenizer
# ----------------------------------------------------------------------
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
        raise ValueError(f"Unknown character: '{ch}'")
    return tokens

# ----------------------------------------------------------------------
# Module 1: Infix to Postfix (Shunting-Yard)
# ----------------------------------------------------------------------
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
                raise ValueError("Mismatched parentheses")
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
            raise ValueError("Mismatched parentheses")
        output.append(top)
    return output

# ----------------------------------------------------------------------
# Module 2: Evaluate Postfix
# ----------------------------------------------------------------------
def eval_postfix(tokens: List[str], var_table: Dict[str, float]) -> float:
    stack = Stack()
    for tok in tokens:
        if tok in FUNCS:
            arg = stack.pop()
            if arg is None:
                raise ValueError(f"Not enough arguments for {tok}")
            if tok == 'sin':
                res = math.sin(arg)
            elif tok == 'cos':
                res = math.cos(arg)
            elif tok == 'sqrt':
                if arg < 0:
                    raise ValueError("sqrt of negative number")
                res = math.sqrt(arg)
            elif tok == 'log':
                if arg <= 0:
                    raise ValueError("log of non-positive number")
                res = math.log(arg)
            elif tok == 'abs':
                res = abs(arg)
            else:
                raise ValueError(f"Unknown function {tok}")
            stack.push(res)
        elif tok in PREC:
            b = stack.pop()
            a = stack.pop()
            if a is None or b is None:
                raise ValueError(f"Not enough operands for {tok}")
            if tok == '+':
                res = a + b
            elif tok == '-':
                res = a - b
            elif tok == '*':
                res = a * b
            elif tok == '/':
                if b == 0:
                    raise ZeroDivisionError("division by zero")
                res = a / b
            elif tok == '^':
                res = a ** b
            else:
                raise ValueError(f"Unknown operator {tok}")
            stack.push(res)
        else:
            try:
                val = float(tok)
            except ValueError:
                if tok not in var_table:
                    raise ValueError(f"Variable '{tok}' not set")
                val = var_table[tok]
            stack.push(val)
    result = stack.pop()
    if not stack.is_empty():
        raise ValueError("Invalid expression: leftover stack entries")
    return result

# ----------------------------------------------------------------------
# Module 4: Expression Tree
# ----------------------------------------------------------------------
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
            if left is None or right is None:
                raise ValueError("Invalid postfix expression for tree")
            node.left = left
            node.right = right
        elif tok in FUNCS:
            child = stack.pop()
            if child is None:
                raise ValueError("Not enough arguments for function")
            node.left = child
        stack.push(node)
    root = stack.pop()
    if not stack.is_empty():
        raise ValueError("Invalid postfix expression for tree")
    return root

def inorder_expr(root: Optional[ExprNode]) -> str:
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
    if root is None:
        return []
    result = [root.val]
    if root.left:
        result.extend(preorder_expr(root.left))
    if root.right:
        result.extend(preorder_expr(root.right))
    return result

def postorder_expr(root: Optional[ExprNode]) -> List[str]:
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
    if root is None:
        raise ValueError("Empty tree")
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
                raise ZeroDivisionError("division by zero")
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
                raise ValueError("sqrt of negative number")
            return math.sqrt(arg)
        elif root.val == 'log':
            if arg <= 0:
                raise ValueError("log of non-positive number")
            return math.log(arg)
        elif root.val == 'abs':
            return abs(arg)
    else:
        try:
            return float(root.val)
        except ValueError:
            if root.val not in var_table:
                raise ValueError(f"Variable '{root.val}' not set")
            return var_table[root.val]
    raise ValueError(f"Unknown node value: {root.val}")

# ----------------------------------------------------------------------
# Module 3: BST Variable Table
# ----------------------------------------------------------------------
class VarBSTNode:
    __slots__ = ('key', 'val', 'left', 'right')
    def __init__(self, key: str, val: float):
        self.key = key
        self.val = val
        self.left = None
        self.right = None

class VarBST:
    def __init__(self):
        self.root = None

    def set(self, key: str, val: float) -> None:
        if not isinstance(key, str) or len(key) != 1 or not key.isalpha():
            raise ValueError("Variable name must be a single letter a-z")
        self.root = self._set(self.root, key, val)

    def _set(self, node: Optional[VarBSTNode], key: str, val: float) -> VarBSTNode:
        if node is None:
            return VarBSTNode(key, val)
        if key < node.key:
            node.left = self._set(node.left, key, val)
        elif key > node.key:
            node.right = self._set(node.right, key, val)
        else:
            node.val = val
        return node

    def get(self, key: str) -> Optional[float]:
        node = self._get(self.root, key)
        return node.val if node else None

    def _get(self, node: Optional[VarBSTNode], key: str) -> Optional[VarBSTNode]:
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._get(node.left, key)
        else:
            return self._get(node.right, key)

    def delete(self, key: str) -> None:
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[VarBSTNode], key: str) -> Optional[VarBSTNode]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            succ = self._min(node.right)
            node.key = succ.key
            node.val = succ.val
            node.right = self._delete(node.right, succ.key)
        return node

    def _min(self, node: VarBSTNode) -> VarBSTNode:
        while node.left:
            node = node.left
        return node

    def list_all(self) -> List[Tuple[str, float]]:
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[VarBSTNode], out: List[Tuple[str, float]]) -> None:
        if node:
            self._inorder(node.left, out)
            out.append((node.key, node.val))
            self._inorder(node.right, out)

# ----------------------------------------------------------------------
# Module 5: Formula DAG
# ----------------------------------------------------------------------
class FormulaDAG:
    def __init__(self):
        self.adj: Dict[str, List[str]] = {}
        self.formulas: Dict[str, str] = {}
        self.trees: Dict[str, ExprNode] = {}

    def _extract_dependencies(self, expr: str) -> Set[str]:
        tokens = tokenize(expr)
        deps = set()
        for tok in tokens:
            if tok.isalpha() and tok not in FUNCS:
                deps.add(tok)
        return deps

    def define(self, name: str, expr: str) -> None:
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        tree = build_expr_tree(postfix)
        deps = self._extract_dependencies(expr)
        deps.discard(name)
        self.adj[name] = list(deps)
        self.formulas[name] = expr
        self.trees[name] = tree
        try:
            self.topological_sort()
        except ValueError as e:
            del self.adj[name]
            del self.formulas[name]
            del self.trees[name]
            raise ValueError(f"Cycle detected when defining '{name}': {e}")

    def topological_sort(self) -> List[str]:
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
            raise ValueError("Cycle detected in formula dependencies")
        return order

    def evaluate_one(self, name: str, var_table: Dict[str, float]) -> float:
        memo = {}
        def eval_rec(n: str) -> float:
            if n in memo:
                return memo[n]
            if n not in self.trees:
                raise ValueError(f"Formula '{n}' not defined")
            local = {**var_table, **memo}
            try:
                res = eval_tree(self.trees[n], local)
                memo[n] = res
                return res
            except Exception as e:
                raise ValueError(f"Error evaluating '{n}': {e}")
        return eval_rec(name)

# ----------------------------------------------------------------------
# Main & CLI
# ----------------------------------------------------------------------
def print_help():
    print("""
Available commands:
  SET <var> <value>          - assign a value to variable (a-z)
  GET <var>                  - show current value of variable
  DELETE <var>               - remove variable from symbol table
  LIST                       - show all variables with values (sorted)
  EVAL <expression>          - evaluate infix expression using current variables
  TREE <expression>          - show inorder, preorder, postorder traversal
  DEFINE <name> = <expr>     - define a formula (can depend on other formulas)
  SHOW_FORMULAS              - list defined formulas
  EVAL_FORMULA <name>        - evaluate a defined formula using current variables
  HELP                       - show this help
  EXIT                       - quit the program
""")

def main():
    var_bst = VarBST()
    formula_dag = FormulaDAG()
    history = []

    # Test expressions with explicit variable values
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

    print("Academic Expression Evaluator & Formula Scheduler")
    print("Type HELP for available commands.\n")
    print("--- Running predefined test expressions ---")
    for expr, var_vals in test_exprs:
        for var, val in var_vals.items():
            var_bst.set(var, val)
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        result = eval_postfix(postfix, var_vals)
        tree = build_expr_tree(postfix)
        tree_result = eval_tree(tree, var_vals)
        # Format output to show variable values
        var_str = ", ".join(f"{k}={v}" for k, v in var_vals.items())
        print(f"EVAL {expr}  [dengan {var_str}] = {result} (tree: {tree_result})")
    print("--- End of tests ---\n")

    # CLI loop
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
                    print("Value must be a number")
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
                    print(f"Variable '{var_name}' not set")
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
                    print("No variables set.")
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
                    # Get current variables from BST
                    var_dict = {k: v for k, v in var_bst.list_all()}
                    result = eval_postfix(postfix, var_dict)
                    print(f"Result: {result}")
                    tree = build_expr_tree(postfix)
                    history.append((expr_str, result))
                    if len(history) > 10:
                        history.pop(0)
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
                    print("Invalid definition")
                    continue
                if not name.isalpha():
                    print("Formula name must contain only letters")
                    continue
                if name in FUNCS:
                    print("Formula name cannot be a built-in function name")
                    continue
                try:
                    formula_dag.define(name, expr)
                    print(f"Formula '{name}' defined: {expr}")
                except Exception as e:
                    print(f"Definition failed: {e}")
            elif cmd == "SHOW_FORMULAS":
                if not formula_dag.formulas:
                    print("No formulas defined.")
                else:
                    print("Defined formulas:")
                    for name, expr in formula_dag.formulas.items():
                        deps = formula_dag.adj.get(name, [])
                        deps_str = ", ".join(deps) if deps else "none"
                        print(f"  {name} = {expr}  (depends on: {deps_str})")
            elif cmd == "EVAL_FORMULA":
                if len(parts) != 2:
                    print("Usage: EVAL_FORMULA <formula_name>")
                    continue
                fname = parts[1].strip()
                if fname not in formula_dag.formulas:
                    print(f"Formula '{fname}' not defined")
                    continue
                try:
                    var_dict = {k: v for k, v in var_bst.list_all()}
                    result = formula_dag.evaluate_one(fname, var_dict)
                    print(f"{fname} = {result}")
                except Exception as e:
                    print(f"Evaluation error: {e}")
            else:
                print(f"Unknown command: {cmd}. Type HELP.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except EOFError:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
