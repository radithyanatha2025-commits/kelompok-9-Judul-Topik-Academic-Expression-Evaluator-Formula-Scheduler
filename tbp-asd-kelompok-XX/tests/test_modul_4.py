"""
UNIT TEST: MODUL 4 - EXPRESSION TREE
Menguji pembangunan tree dan traversal
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.modul_1 import infix_to_postfix
from modules.modul_4 import build_expr_tree, inorder_expr, preorder_expr, postorder_expr, eval_tree
from modules.tokenizer import tokenize


def test_modul_4_build_tree():
    """Menguji pembangunan expression tree"""
    print("\n[TEST MODUL 4] Build Expression Tree")
    
    expr = "a + b * c"
    tokens = tokenize(expr)
    postfix = infix_to_postfix(tokens)
    tree = build_expr_tree(postfix)
    
    assert tree is not None
    assert tree.val == '+'
    assert tree.left.val == 'a'
    assert tree.right.val == '*'
    assert tree.right.left.val == 'b'
    assert tree.right.right.val == 'c'
    
    print("✅ Build tree test passed!")


def test_modul_4_inorder():
    """Menguji inorder traversal (infix dengan kurung)"""
    print("\n[TEST MODUL 4] Inorder Traversal")
    
    test_cases = [
        ("a + b", "(a + b)"),
        ("a + b * c", "(a + (b * c))"),
        ("(a + b) * c", "((a + b) * c)"),
        ("a ^ b ^ c", "(a ^ (b ^ c))"),  # right-associative
    ]
    
    for expr, expected in test_cases:
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        tree = build_expr_tree(postfix)
        result = inorder_expr(tree)
        assert result == expected, f"{expr}: expected {expected}, got {result}"
        print(f"  ✅ {expr} → inorder: {result}")
    
    print("✅ Inorder traversal test passed!")


def test_modul_4_preorder():
    """Menguji preorder traversal (prefix notation)"""
    print("\n[TEST MODUL 4] Preorder Traversal")
    
    test_cases = [
        ("a + b", "+ a b"),
        ("a + b * c", "+ a * b c"),
        ("(a + b) * c", "* + a b c"),
    ]
    
    for expr, expected in test_cases:
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        tree = build_expr_tree(postfix)
        result = " ".join(preorder_expr(tree))
        assert result == expected, f"{expr}: expected {expected}, got {result}"
        print(f"  ✅ {expr} → preorder: {result}")
    
    print("✅ Preorder traversal test passed!")


def test_modul_4_postorder():
    """Menguji postorder traversal (postfix notation)"""
    print("\n[TEST MODUL 4] Postorder Traversal")
    
    test_cases = [
        ("a + b", "a b +"),
        ("a + b * c", "a b c * +"),
        ("(a + b) * c", "a b + c *"),
    ]
    
    for expr, expected in test_cases:
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        tree = build_expr_tree(postfix)
        result = " ".join(postorder_expr(tree))
        assert result == expected, f"{expr}: expected {expected}, got {result}"
        print(f"  ✅ {expr} → postorder: {result}")
    
    print("✅ Postorder traversal test passed!")


def test_modul_4_eval_tree():
    """Menguji evaluasi expression tree"""
    print("\n[TEST MODUL 4] Evaluate Expression Tree")
    
    var_table = {'a': 2.0, 'b': 3.0, 'c': 4.0}
    
    test_cases = [
        ("a + b", 5.0),
        ("a * b + c", 10.0),
        ("(a + b) * c", 20.0),
        ("a ^ b", 8.0),
    ]
    
    for expr, expected in test_cases:
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        tree = build_expr_tree(postfix)
        result = eval_tree(tree, var_table)
        assert abs(result - expected) < 0.0001, f"{expr}: expected {expected}, got {result}"
        print(f"  ✅ {expr} = {result}")
    
    print("✅ Evaluate tree test passed!")


if __name__ == "__main__":
    print("=" * 60)
    print("UNIT TEST: MODUL 4 (EXPRESSION TREE)")
    print("=" * 60)
    test_modul_4_build_tree()
    test_modul_4_inorder()
    test_modul_4_preorder()
    test_modul_4_postorder()
    test_modul_4_eval_tree()
    print("\n" + "=" * 60)
    print("✅ SEMUA TEST MODUL 4 BERHASIL!")
    print("=" * 60)
