import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.modul_1 import infix_to_postfix
from modules.tokenizer import tokenize


def test_modul_1_basic_operators():
    """Menguji konversi operator dasar"""
    print("\n[TEST MODUL 1] Basic Operators")
    
    test_cases = [
        ("a + b", ["a", "b", "+"]),
        ("a - b", ["a", "b", "-"]),
        ("a * b", ["a", "b", "*"]),
        ("a / b", ["a", "b", "/"]),
        ("a ^ b", ["a", "b", "^"]),
    ]
    
    for expr, expected in test_cases:
        tokens = tokenize(expr)
        result = infix_to_postfix(tokens)
        assert result == expected, f"Failed: {expr}"
        print(f"  ✅ {expr} → {' '.join(result)}")
    
    print("✅ Basic operators test passed!")


def test_modul_1_precedence():
    """Menguji aturan precedence operator"""
    print("\n[TEST MODUL 1] Precedence Rules")
    
    test_cases = [
        ("a + b * c", ["a", "b", "c", "*", "+"]),
        ("a * b + c", ["a", "b", "*", "c", "+"]),
        ("a ^ b ^ c", ["a", "b", "c", "^", "^"]),  # right-associative
        ("a + b - c", ["a", "b", "+", "c", "-"]),   # left-associative
        ("a * b / c", ["a", "b", "*", "c", "/"]),   # left-associative
    ]
    
    for expr, expected in test_cases:
        tokens = tokenize(expr)
        result = infix_to_postfix(tokens)
        assert result == expected, f"Failed: {expr}\nGot: {result}"
        print(f"  ✅ {expr} → {' '.join(result)}")
    
    print("✅ Precedence test passed!")


def test_modul_1_parentheses():
    """Menguji konversi dengan kurung"""
    print("\n[TEST MODUL 1] Parentheses")
    
    test_cases = [
        ("(a + b) * c", ["a", "b", "+", "c", "*"]),
        ("a * (b + c)", ["a", "b", "c", "+", "*"]),
        ("(a + b) * (c - d)", ["a", "b", "+", "c", "d", "-", "*"]),
        ("((a + b) * c) / d", ["a", "b", "+", "c", "*", "d", "/"]),
    ]
    
    for expr, expected in test_cases:
        tokens = tokenize(expr)
        result = infix_to_postfix(tokens)
        assert result == expected, f"Failed: {expr}"
        print(f"  ✅ {expr} → {' '.join(result)}")
    
    print("✅ Parentheses test passed!")


def test_modul_1_functions():
    """Menguji konversi dengan fungsi matematika"""
    print("\n[TEST MODUL 1] Functions")
    
    test_cases = [
        ("sin(a)", ["a", "sin"]),
        ("cos(a)", ["a", "cos"]),
        ("sqrt(a)", ["a", "sqrt"]),
        ("log(a)", ["a", "log"]),
        ("abs(a)", ["a", "abs"]),
        ("sin(a) + cos(b)", ["a", "sin", "b", "cos", "+"]),
        ("sqrt(a^2 + b^2)", ["a", "2", "^", "b", "2", "^", "+", "sqrt"]),
    ]
    
    for expr, expected in test_cases:
        tokens = tokenize(expr)
        result = infix_to_postfix(tokens)
        assert result == expected, f"Failed: {expr}\nGot: {result}"
        print(f"  ✅ {expr} → {' '.join(result)}")
    
    print("✅ Functions test passed!")


def test_modul_1_complex():
    """Menguji konversi ekspresi kompleks"""
    print("\n[TEST MODUL 1] Complex Expressions")
    
    test_cases = [
        ("a + b * c - d / e ^ f", 
         ["a", "b", "c", "*", "+", "d", "e", "f", "^", "/", "-"]),
        ("sin(a) * cos(b) + sqrt(c)", 
         ["a", "sin", "b", "cos", "*", "c", "sqrt", "+"]),
    ]
    
    for expr, expected in test_cases:
        tokens = tokenize(expr)
        result = infix_to_postfix(tokens)
        assert result == expected, f"Failed: {expr}"
        print(f"  ✅ {expr} → {' '.join(result)}")
    
    print("✅ Complex expressions test passed!")


if __name__ == "__main__":
    print("=" * 60)
    print("UNIT TEST: MODUL 1 (INFIX → POSTFIX)")
    print("=" * 60)
    test_modul_1_basic_operators()
    test_modul_1_precedence()
    test_modul_1_parentheses()
    test_modul_1_functions()
    test_modul_1_complex()
    print("\n" + "=" * 60)
    print("✅ SEMUA TEST MODUL 1 BERHASIL!")
    print("=" * 60)
