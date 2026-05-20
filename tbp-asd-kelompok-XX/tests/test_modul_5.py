import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.modul_5 import FormulaDAG


def test_modul_5_define():
    """Menguji definisi formula"""
    print("\n[TEST MODUL 5] Define Formula")
    
    dag = FormulaDAG()
    dag.define('a', '10')
    dag.define('b', '20')
    dag.define('c', 'a + b')
    
    assert 'a' in dag.formulas
    assert 'b' in dag.formulas
    assert 'c' in dag.formulas
    assert dag.formulas['c'] == 'a + b'
    
    print("✅ Define formula test passed!")


def test_modul_5_topological_order():
    """Menguji urutan topological sort"""
    print("\n[TEST MODUL 5] Topological Order")
    
    dag = FormulaDAG()
    dag.define('a', '10')
    dag.define('b', '20')
    dag.define('c', 'a + b')
    dag.define('d', 'c * 2')
    
    order = dag.topological_sort()
    
    # Urutan harus memenuhi dependensi
    for i, f in enumerate(order):
        if f == 'c':
            assert order.index('a') < i
            assert order.index('b') < i
        if f == 'd':
            assert order.index('c') < i
    
    print(f"✅ Topological order test passed! Order: {order}")


def test_modul_5_evaluate():
    """Menguji evaluasi formula dengan dependensi"""
    print("\n[TEST MODUL 5] Evaluate Formula")
    
    dag = FormulaDAG()
    dag.define('a', '10')
    dag.define('b', '20')
    dag.define('c', 'a + b')
    dag.define('d', 'c * 2')
    dag.define('e', 'd - 5')
    
    var_table = {}
    
    assert dag.evaluate_one('a', var_table) == 10.0
    assert dag.evaluate_one('b', var_table) == 20.0
    assert dag.evaluate_one('c', var_table) == 30.0
    assert dag.evaluate_one('d', var_table) == 60.0
    assert dag.evaluate_one('e', var_table) == 55.0
    
    print("✅ Evaluate formula test passed!")


def test_modul_5_cycle_detection():
    """Menguji deteksi siklus dependensi"""
    print("\n[TEST MODUL 5] Cycle Detection")
    
    dag = FormulaDAG()
    dag.define('a', 'b + 1')
    dag.define('b', 'c + 1')
    
    try:
        dag.define('c', 'a + 1')  # Membentuk siklus: a→b→c→a
        assert False, "Should detect cycle!"
    except ValueError as e:
        assert "Siklus" in str(e)
        print(f"✅ Cycle detection test passed: {e}")


def test_modul_5_formula_with_functions():
    """Menguji formula yang mengandung fungsi matematika"""
    print("\n[TEST MODUL 5] Formula with Functions")
    
    dag = FormulaDAG()
    dag.define('rad', 'theta * 3.141592653589793 / 180')
    dag.define('jarak', 'v^2 * sin(2 * rad) / g')
    
    var_table = {'v': 25.0, 'theta': 45.0, 'g': 9.81}
    
    # Evaluasi pada sudut 45 derajat
    jarak = dag.evaluate_one('jarak', var_table)
    expected = (25.0**2 * math.sin(2 * math.radians(45))) / 9.81
    assert abs(jarak - expected) < 0.01
    
    print(f"✅ Formula with functions test passed! Jarak = {jarak:.2f} m")


if __name__ == "__main__":
    print("=" * 60)
    print("UNIT TEST: MODUL 5 (FORMULA DAG)")
    print("=" * 60)
    test_modul_5_define()
    test_modul_5_topological_order()
    test_modul_5_evaluate()
    test_modul_5_cycle_detection()
    test_modul_5_formula_with_functions()
    print("\n" + "=" * 60)
    print("✅ SEMUA TEST MODUL 5 BERHASIL!")
    print("=" * 60)
