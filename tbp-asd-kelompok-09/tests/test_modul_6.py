import sys
import os
import io
import math
from contextlib import redirect_stdout, redirect_stderr

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# =============================================================================
# IMPORT MODUL YANG DIUJI
# =============================================================================
from modules.modul_1 import infix_to_postfix, PREC, RASSOC, FUNCS
from modules.modul_2 import eval_postfix
from modules.modul_3 import VarBST
from modules.modul_4 import build_expr_tree, inorder_expr, preorder_expr, postorder_expr, eval_tree
from modules.modul_5 import FormulaDAG
from modules.tokenizer import tokenize


# =============================================================================
# FUNGSI BANTU UNTUK TEST
# =============================================================================
def capture_output(func, *args, **kwargs):
    """
    Menangkap output stdout dari suatu fungsi
    """
    f = io.StringIO()
    with redirect_stdout(f):
        result = func(*args, **kwargs)
    output = f.getvalue()
    return result, output


def simulate_cli_command(command, var_bst, dag):
    """
    Simulasi eksekusi satu perintah CLI
    Mengembalikan output string dan perubahan state
    """
    parts = command.strip().split(maxsplit=1)
    if not parts:
        return "", var_bst, dag
    
    cmd = parts[0].upper()
    output_lines = []
    
    try:
        if cmd == "SET":
            if len(parts) != 2:
                output_lines.append("Usage: SET var nilai")
            else:
                sub = parts[1].split()
                if len(sub) != 2:
                    output_lines.append("Usage: SET var nilai")
                else:
                    vname, vval = sub[0], sub[1]
                    if len(vname) != 1 or not vname.isalpha():
                        output_lines.append("Nama variabel harus satu huruf")
                    else:
                        try:
                            val = float(vval)
                            var_bst.set(vname, val)
                            output_lines.append(f"{vname} = {val}")
                        except ValueError:
                            output_lines.append("Nilai harus angka")
        
        elif cmd == "GET":
            if len(parts) != 2:
                output_lines.append("Usage: GET var")
            else:
                vname = parts[1].strip()
                if len(vname) != 1 or not vname.isalpha():
                    output_lines.append("Nama variabel harus satu huruf")
                else:
                    val = var_bst.get(vname)
                    if val is None:
                        output_lines.append(f"Variabel {vname} belum di-SET")
                    else:
                        output_lines.append(f"{vname} = {val}")
        
        elif cmd == "DELETE":
            if len(parts) != 2:
                output_lines.append("Usage: DELETE var")
            else:
                vname = parts[1].strip()
                if len(vname) != 1 or not vname.isalpha():
                    output_lines.append("Nama variabel harus satu huruf a-z")
                else:
                    var_bst.delete(vname)
                    output_lines.append(f"Variabel '{vname}' telah dihapus")
        
        elif cmd == "LIST":
            vars_list = var_bst.list_all()
            if not vars_list:
                output_lines.append("Tidak ada variabel.")
            else:
                for k, v in vars_list:
                    output_lines.append(f"{k} = {v}")
        
        elif cmd == "EVAL":
            if len(parts) != 2:
                output_lines.append("Usage: EVAL ekspresi")
            else:
                expr_str = parts[1]
                try:
                    toks = tokenize(expr_str)
                    post = infix_to_postfix(toks)
                    vardict = {k: v for k, v in var_bst.list_all()}
                    res = eval_postfix(post, vardict)
                    output_lines.append(f"Result = {res}")
                except Exception as e:
                    output_lines.append(f"Error: {e}")
        
        elif cmd == "TREE":
            if len(parts) != 2:
                output_lines.append("Usage: TREE ekspresi")
            else:
                expr_str = parts[1]
                try:
                    toks = tokenize(expr_str)
                    post = infix_to_postfix(toks)
                    tree = build_expr_tree(post)
                    output_lines.append(f"Inorder : {inorder_expr(tree)}")
                    output_lines.append(f"Preorder: {' '.join(preorder_expr(tree))}")
                    output_lines.append(f"Postorder: {' '.join(postorder_expr(tree))}")
                except Exception as e:
                    output_lines.append(f"Error: {e}")
        
        elif cmd == "DEFINE":
            if len(parts) != 2:
                output_lines.append("Usage: DEFINE name = expr")
            else:
                def_part = parts[1].strip()
                if '=' not in def_part:
                    output_lines.append("Harus ada '='")
                else:
                    name, expr = def_part.split('=', 1)
                    name = name.strip()
                    expr = expr.strip()
                    if not name or not expr:
                        output_lines.append("Format salah")
                    elif name in FUNCS:
                        output_lines.append("Nama tidak boleh sama dengan fungsi")
                    else:
                        try:
                            dag.define(name, expr)
                            output_lines.append(f"Formula {name} didefinisikan: {expr}")
                        except Exception as e:
                            output_lines.append(f"Error: {e}")
        
        elif cmd == "SHOW_FORMULAS":
            if not dag.formulas:
                output_lines.append("Tidak ada formula.")
            else:
                for name, expr in dag.formulas.items():
                    deps = []
                    for dep, targets in dag.graph.items():
                        if name in targets:
                            deps.append(dep)
                    output_lines.append(f"{name} = {expr}  (depend: {deps})")
        
        elif cmd == "EVAL_FORMULA":
            if len(parts) != 2:
                output_lines.append("Usage: EVAL_FORMULA nama")
            else:
                fname = parts[1].strip()
                if fname not in dag.formulas:
                    output_lines.append(f"Formula {fname} tidak ditemukan")
                else:
                    try:
                        vardict = {k: v for k, v in var_bst.list_all()}
                        res = dag.evaluate_one(fname, vardict)
                        output_lines.append(f"{fname} = {res}")
                    except Exception as e:
                        output_lines.append(f"Error: {e}")
        
        elif cmd == "HELP":
            output_lines.append("PERINTAH: SET, GET, DELETE, LIST, EVAL, TREE, DEFINE, SHOW_FORMULAS, EVAL_FORMULA, HELP, EXIT")
        
        elif cmd == "EXIT":
            output_lines.append("Goodbye!")
        
        else:
            output_lines.append(f"Perintah tidak dikenal: {cmd}. Ketik HELP.")
    
    except Exception as e:
        output_lines.append(f"Unexpected error: {e}")
    
    return "\n".join(output_lines), var_bst, dag


# =============================================================================
# UNIT TEST
# =============================================================================
def test_modul_6_help():
    """Menguji perintah HELP"""
    print("\n[TEST MODUL 6] HELP Command")
    
    var_bst = VarBST()
    dag = FormulaDAG()
    
    output, _, _ = simulate_cli_command("HELP", var_bst, dag)
    
    assert "PERINTAH:" in output
    assert "SET" in output
    assert "GET" in output
    assert "DELETE" in output
    assert "LIST" in output
    assert "EVAL" in output
    assert "TREE" in output
    assert "DEFINE" in output
    
    print("✅ HELP command test passed!")


def test_modul_6_set():
    """Menguji perintah SET"""
    print("\n[TEST MODUL 6] SET Command")
    
    var_bst = VarBST()
    dag = FormulaDAG()
    
    # SET variabel yang valid
    output, var_bst, _ = simulate_cli_command("SET a 10", var_bst, dag)
    assert "a = 10.0" in output
    assert var_bst.get('a') == 10.0
    
    # SET variabel dengan nama tidak valid (multi huruf)
    output, var_bst, _ = simulate_cli_command("SET ab 10", var_bst, dag)
    assert "Nama variabel harus satu huruf" in output
    
    # SET dengan nilai bukan angka
    output, var_bst, _ = simulate_cli_command("SET a abc", var_bst, dag)
    assert "Nilai harus angka" in output
    
    # SET format salah
    output, var_bst, _ = simulate_cli_command("SET a", var_bst, dag)
    assert "Usage: SET var nilai" in output
    
    print("✅ SET command test passed!")


def test_modul_6_get():
    """Menguji perintah GET"""
    print("\n[TEST MODUL 6] GET Command")
    
    var_bst = VarBST()
    dag = FormulaDAG()
    
    # GET variabel yang belum di-SET
    output, _, _ = simulate_cli_command("GET x", var_bst, dag)
    assert "Variabel x belum di-SET" in output
    
    # SET lalu GET
    var_bst.set('x', 25.0)
    output, _, _ = simulate_cli_command("GET x", var_bst, dag)
    assert "x = 25.0" in output
    
    # GET dengan nama tidak valid
    output, _, _ = simulate_cli_command("GET ab", var_bst, dag)
    assert "Nama variabel harus satu huruf" in output
    
    print("✅ GET command test passed!")


def test_modul_6_delete():
    """Menguji perintah DELETE"""
    print("\n[TEST MODUL 6] DELETE Command")
    
    var_bst = VarBST()
    dag = FormulaDAG()
    
    # SET lalu DELETE
    var_bst.set('a', 10.0)
    var_bst.set('b', 20.0)
    
    output, var_bst, _ = simulate_cli_command("DELETE a", var_bst, dag)
    assert "Variabel 'a' telah dihapus" in output
    assert var_bst.get('a') is None
    assert var_bst.get('b') == 20.0
    
    # DELETE dengan nama tidak valid
    output, _, _ = simulate_cli_command("DELETE ab", var_bst, dag)
    assert "Nama variabel harus satu huruf a-z" in output
    
    print("✅ DELETE command test passed!")


def test_modul_6_list():
    """Menguji perintah LIST"""
    print("\n[TEST MODUL 6] LIST Command")
    
    var_bst = VarBST()
    dag = FormulaDAG()
    
    # LIST saat kosong
    output, _, _ = simulate_cli_command("LIST", var_bst, dag)
    assert "Tidak ada variabel" in output
    
    # SET beberapa variabel
    var_bst.set('c', 30.0)
    var_bst.set('a', 10.0)
    var_bst.set('b', 20.0)
    
    output, _, _ = simulate_cli_command("LIST", var_bst, dag)
    # Harus terurut: a, b, c
    lines = output.strip().split('\n')
    assert "a = 10.0" in lines[0]
    assert "b = 20.0" in lines[1]
    assert "c = 30.0" in lines[2]
    
    print("✅ LIST command test passed!")


def test_modul_6_eval():
    """Menguji perintah EVAL"""
    print("\n[TEST MODUL 6] EVAL Command")
    
    var_bst = VarBST()
    dag = FormulaDAG()
    
    # Eval ekspresi tanpa variabel
    output, _, _ = simulate_cli_command("EVAL 2 + 3", var_bst, dag)
    assert "Result = 5.0" in output
    
    # Eval dengan variabel
    var_bst.set('a', 10.0)
    var_bst.set('b', 20.0)
    output, _, _ = simulate_cli_command("EVAL a + b", var_bst, dag)
    assert "Result = 30.0" in output
    
    # Eval dengan fungsi
    output, _, _ = simulate_cli_command("EVAL sin(0)", var_bst, dag)
    assert "Result = 0.0" in output
    
    # Eval ekspresi kompleks
    output, _, _ = simulate_cli_command("EVAL (2 + 3) * 4", var_bst, dag)
    assert "Result = 20.0" in output
    
    # Eval dengan variabel belum di-SET
    output, _, _ = simulate_cli_command("EVAL x + y", var_bst, dag)
    assert "Error:" in output
    
    print("✅ EVAL command test passed!")


def test_modul_6_tree():
    """Menguji perintah TREE"""
    print("\n[TEST MODUL 6] TREE Command")
    
    var_bst = VarBST()
    dag = FormulaDAG()
    
    # TREE ekspresi sederhana
    output, _, _ = simulate_cli_command("TREE a + b", var_bst, dag)
    assert "Inorder : (a + b)" in output
    assert "Preorder: + a b" in output
    assert "Postorder: a b +" in output
    
    # TREE ekspresi dengan precedence
    output, _, _ = simulate_cli_command("TREE a + b * c", var_bst, dag)
    assert "Inorder : (a + (b * c))" in output
    
    # TREE ekspresi dengan kurung
    output, _, _ = simulate_cli_command("TREE (a + b) * c", var_bst, dag)
    assert "Inorder : ((a + b) * c)" in output
    
    # TREE dengan fungsi
    output, _, _ = simulate_cli_command("TREE sin(a)", var_bst, dag)
    assert "Inorder : sin(a)" in output
    
    print("✅ TREE command test passed!")


def test_modul_6_define():
    """Menguji perintah DEFINE"""
    print("\n[TEST MODUL 6] DEFINE Command")
    
    var_bst = VarBST()
    dag = FormulaDAG()
    
    # DEFINE formula valid
    output, _, dag = simulate_cli_command("DEFINE pythag = sqrt(a^2 + b^2)", var_bst, dag)
    assert "Formula pythag didefinisikan" in output
    assert "pythag" in dag.formulas
    
    # DEFINE dengan nama sudah ada fungsi
    output, _, _ = simulate_cli_command("DEFINE sin = a + b", var_bst, dag)
    assert "Nama tidak boleh sama dengan fungsi" in output
    
    # DEFINE format salah
    output, _, _ = simulate_cli_command("DEFINE pythag", var_bst, dag)
    assert "Harus ada '='" in output
    
    # DEFINE dengan nama kosong
    output, _, _ = simulate_cli_command("DEFINE = a + b", var_bst, dag)
    assert "Format salah" in output
    
    print("✅ DEFINE command test passed!")


def test_modul_6_show_formulas():
    """Menguji perintah SHOW_FORMULAS"""
    print("\n[TEST MODUL 6] SHOW_FORMULAS Command")
    
    var_bst = VarBST()
    dag = FormulaDAG()
    
    # SHOW_FORMULAS saat kosong
    output, _, _ = simulate_cli_command("SHOW_FORMULAS", var_bst, dag)
    assert "Tidak ada formula" in output
    
    # DEFINE beberapa formula
    dag.define('a', '10')
    dag.define('b', '20')
    dag.define('c', 'a + b')
    
    output, _, _ = simulate_cli_command("SHOW_FORMULAS", var_bst, dag)
    assert "a = 10" in output
    assert "b = 20" in output
    assert "c = a + b" in output
    
    print("✅ SHOW_FORMULAS command test passed!")


def test_modul_6_eval_formula():
    """Menguji perintah EVAL_FORMULA"""
    print("\n[TEST MODUL 6] EVAL_FORMULA Command")
    
    var_bst = VarBST()
    dag = FormulaDAG()
    
    # EVAL_FORMULA formula tidak ada
    output, _, _ = simulate_cli_command("EVAL_FORMULA unknown", var_bst, dag)
    assert "tidak ditemukan" in output
    
    # DEFINE formula
    dag.define('a', '10')
    dag.define('b', '20')
    dag.define('c', 'a + b')
    dag.define('d', 'c * 2')
    
    # EVAL_FORMULA
    output, _, _ = simulate_cli_command("EVAL_FORMULA d", var_bst, dag)
    assert "d = 60.0" in output
    
    print("✅ EVAL_FORMULA command test passed!")


def test_modul_6_unknown_command():
    """Menguji perintah yang tidak dikenal"""
    print("\n[TEST MODUL 6] Unknown Command")
    
    var_bst = VarBST()
    dag = FormulaDAG()
    
    output, _, _ = simulate_cli_command("UNKNOWN abc", var_bst, dag)
    assert "Perintah tidak dikenal" in output
    
    print("✅ Unknown command test passed!")


def test_modul_6_integration():
    """Menguji integrasi beberapa perintah berurutan"""
    print("\n[TEST MODUL 6] Integration Test")
    
    var_bst = VarBST()
    dag = FormulaDAG()
    
    # Simulasi sesi CLI
    commands = [
        "SET a 3",
        "SET b 4",
        "DEFINE pythag = sqrt(a^2 + b^2)",
        "EVAL_FORMULA pythag",
        "LIST",
        "TREE (a + b) * 2",
    ]
    
    outputs = []
    for cmd in commands:
        output, var_bst, dag = simulate_cli_command(cmd, var_bst, dag)
        outputs.append(output)
        print(f"  {cmd} → {output[:50]}...")
    
    # Verifikasi hasil integrasi
    # SET a 3
    assert var_bst.get('a') == 3.0
    # SET b 4
    assert var_bst.get('b') == 4.0
    # DEFINE pythag
    assert "pythag" in dag.formulas
    # EVAL_FORMULA pythag = 5
    assert any("5.0" in out for out in outputs)
    # LIST harus ada a=3, b=4
    list_output = outputs[4]
    assert "a = 3.0" in list_output
    assert "b = 4.0" in list_output
    
    print("✅ Integration test passed!")


if __name__ == "__main__":
    print("=" * 60)
    print("UNIT TEST: MODUL 6 (CLI KALKULATOR)")
    print("=" * 60)
    
    test_modul_6_help()
    test_modul_6_set()
    test_modul_6_get()
    test_modul_6_delete()
    test_modul_6_list()
    test_modul_6_eval()
    test_modul_6_tree()
    test_modul_6_define()
    test_modul_6_show_formulas()
    test_modul_6_eval_formula()
    test_modul_6_unknown_command()
    test_modul_6_integration()
    
    print("\n" + "=" * 60)
    print("✅ SEMUA TEST MODUL 6 BERHASIL!")
    print("=" * 60)
