import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.modul_1 import infix_to_postfix
from modules.modul_2 import eval_postfix
from modules.tokenizer import tokenize


def test_modul_2_basic_arithmetic():
    """Menguji evaluasi aritmetika dasar"""
    print("\n[TEST MODUL 2] Basic Arithmetic")
    
    test_cases = [
        ("2 + 3", 5.0),
        ("2 + 3 * 4", 14.0),
        ("(2 + 3) * 4", 20.0),
        ("10 - 3", 7.0),
        ("10 / 2", 5.0),
        ("2 ^ 3", 8.0),
        ("2 ^ 3 ^ 2", 512.0),  # right-associative: 2^(3^2)=2^9=512
    ]
    
    for expr, expected in test_cases:
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        result = eval_postfix(postfix, {})
        assert abs(result - expected) < 0.0001, f"{expr}: expected {expected}, got {result}"
        print(f"  ✅ {expr} = {result}")
    
    print("✅ Basic arithmetic test passed!")


def test_modul_2_with_variables():
    """Menguji evaluasi dengan variabel"""
    print("\n[TEST MODUL 2] Variables")
    
    var_table = {'a': 2.0, 'b': 3.0, 'c': 5.0, 'x': 10.0, 'y': 4.0}
    
    test_cases = [
        ("a + b", 5.0),
        ("a * b + c", 11.0),
        ("(a + b) * c", 25.0),
        ("x / y", 2.5),
        ("x ^ 2", 100.0),
        ("x - y * 2", 2.0),
    ]
    
    for expr, expected in test_cases:
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        result = eval_postfix(postfix, var_table)
        assert abs(result - expected) < 0.0001, f"{expr}: expected {expected}, got {result}"
        print(f"  ✅ {expr} = {result}")
    
    print("✅ Variables test passed!")


def test_modul_2_functions():
    """Menguji evaluasi dengan fungsi matematika"""
    print("\n[TEST MODUL 2] Mathematical Functions")
    
    test_cases = [
        ("sin(0)", 0.0),
        ("cos(0)", 1.0),
        ("sqrt(16)", 4.0),
        ("log(2.718281828459045)", 1.0),
        ("abs(-5)", 5.0),
        ("sin(3.14159/2)", 1.0),  # sin(90°)
    ]
    
    for expr, expected in test_cases:
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        result = eval_postfix(postfix, {})
        assert abs(result - expected) < 0.0001, f"{expr}: expected {expected}, got {result}"
        print(f"  ✅ {expr} = {result}")
    
    print("✅ Functions test passed!")


def test_modul_2_complex():
    """Menguji evaluasi ekspresi kompleks"""
    print("\n[TEST MODUL 2] Complex Expressions")
    
    var_table = {'a': 3.0, 'b': 4.0, 'c': 5.0}
    
    test_cases = [
        ("sqrt(a^2 + b^2)", 5.0),    # Pythagoras: 3-4-5 triangle
        ("a * b + b * c + c * a", 47.0),  # 12 + 20 + 15 = 47
        ("(a + b) * (a - b)", -7.0),      # 7 * (-1) = -7
        ("abs(a - b) * c", 5.0),          # | -1 | * 5 = 5
        ("a / (b + c)", 0.33333),         # 3 / 9 = 0.333...
    ]
    
    for expr, expected in test_cases:
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        result = eval_postfix(postfix, var_table)
        assert abs(result - expected) < 0.0001, f"{expr}: expected {expected}, got {result}"
        print(f"  ✅ {expr} = {result}")
    
    print("✅ Complex expressions test passed!")


def test_modul_2_error_handling():
    """Menguji penanganan error"""
    print("\n[TEST MODUL 2] Error Handling")
    
    # Variabel belum di-SET
    try:
        tokens = tokenize("x + y")
        postfix = infix_to_postfix(tokens)
        eval_postfix(postfix, {})
        assert False, "Should raise error for undefined variable"
    except ValueError as e:
        assert "belum di-SET" in str(e)
        print(f"  ✅ Undefined variable error caught: {e}")
    
    # Pembagian dengan nol
    try:
        tokens = tokenize("10 / 0")
        postfix = infix_to_postfix(tokens)
        eval_postfix(postfix, {})
        assert False, "Should raise division by zero error"
    except ZeroDivisionError as e:
        print(f"  ✅ Division by zero error caught: {e}")
    
    print("✅ Error handling test passed!")


if __name__ == "__main__":
    print("=" * 60)
    print("UNIT TEST: MODUL 2 (EVALUASI POSTFIX)")
    print("=" * 60)
    test_modul_2_basic_arithmetic()
    test_modul_2_with_variables()
    test_modul_2_functions()
    test_modul_2_complex()
    test_modul_2_error_handling()
    print("\n" + "=" * 60)
    print("✅ SEMUA TEST MODUL 2 BERHASIL!")
    print("=" * 60)
