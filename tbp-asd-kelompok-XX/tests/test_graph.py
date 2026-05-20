"""
UNIT TEST: GRAPH DAG (DIRECTED ACYCLIC GRAPH)
Menguji implementasi Graph untuk Formula DAG
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.modul_5 import FormulaDAG
from modules.modul_1 import PREC, RASSOC, FUNCS
from modules.tokenizer import tokenize


def test_graph_define_no_deps():
    """Menguji definisi formula tanpa dependensi"""
    print("\n[TEST] Graph DAG - Define Formula No Dependencies")
    
    dag = FormulaDAG()
    dag.define('a', '10')
    dag.define('b', '20')
    dag.define('c', '30')
    
    assert len(dag.formulas) == 3
    assert 'a' in dag.formulas
    assert 'b' in dag.formulas
    assert 'c' in dag.formulas
    
    print("✅ Define formula without dependencies test passed!")


def test_graph_define_with_deps():
    """Menguji definisi formula dengan dependensi"""
    print("\n[TEST] Graph DAG - Define Formula with Dependencies")
    
    dag = FormulaDAG()
    dag.define('x', '10')
    dag.define('y', '20')
    dag.define('z', 'x + y')
    
    # Cek dependensi: z bergantung pada x dan y
    # x dan y tidak bergantung pada siapa pun
    assert 'x' in dag.graph
    assert 'y' in dag.graph
    assert 'z' in dag.graph
    
    print("✅ Define formula with dependencies test passed!")


def test_graph_topological_sort():
    """Menguji topological sort pada DAG"""
    print("\n[TEST] Graph DAG - Topological Sort")
    
    dag = FormulaDAG()
    dag.define('a', '10')
    dag.define('b', '20')
    dag.define('c', 'a + b')
    dag.define('d', 'c * 2')
    
    order = dag.topological_sort()
    
    # Urutan harus memenuhi: a dan b sebelum c, c sebelum d
    assert order.index('c') > order.index('a')
    assert order.index('c') > order.index('b')
    assert order.index('d') > order.index('c')
    
    print(f"✅ Topological sort test passed! Order: {order}")


def test_graph_cycle_detection():
    """Menguji deteksi siklus pada graph"""
    print("\n[TEST] Graph DAG - Cycle Detection")
    
    dag = FormulaDAG()
    dag.define('a', 'b + 1')
    dag.define('b', 'c + 1')
    
    # Mendeteksi siklus saat menambah 'c' yang bergantung pada 'a'
    try:
        dag.define('c', 'a + 1')
        assert False, "Should have detected cycle!"
    except ValueError as e:
        assert "Siklus" in str(e) or "cycle" in str(e).lower()
        print(f"✅ Cycle detected correctly: {e}")


def test_graph_self_dependency():
    """Menguji deteksi self-dependency (formula bergantung pada dirinya sendiri)"""
    print("\n[TEST] Graph DAG - Self Dependency Detection")
    
    dag = FormulaDAG()
    
    try:
        dag.define('x', 'x + 1')
        assert False, "Should reject self-dependency!"
    except ValueError:
        print("✅ Self-dependency detected correctly!")


def test_graph_evaluate_one():
    """Menguji evaluasi satu formula dengan dependensinya"""
    print("\n[TEST] Graph DAG - Evaluate One Formula")
    
    dag = FormulaDAG()
    dag.define('a', '10')
    dag.define('b', '20')
    dag.define('c', 'a + b')
    dag.define('d', 'c * 2')
    
    var_table = {}
    result = dag.evaluate_one('d', var_table)
    
    # a=10, b=20 → c=30 → d=60
    assert result == 60.0
    
    print("✅ Evaluate one formula test passed!")


if __name__ == "__main__":
    print("=" * 60)
    print("UNIT TEST: STRUKTUR DATA GRAPH DAG")
    print("=" * 60)
    test_graph_define_no_deps()
    test_graph_define_with_deps()
    test_graph_topological_sort()
    test_graph_cycle_detection()
    test_graph_self_dependency()
    test_graph_evaluate_one()
    print("\n" + "=" * 60)
    print("✅ SEMUA TEST GRAPH DAG BERHASIL!")
    print("=" * 60)
