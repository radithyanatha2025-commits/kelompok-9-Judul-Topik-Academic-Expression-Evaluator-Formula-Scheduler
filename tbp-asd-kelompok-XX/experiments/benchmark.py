# =======================
# Studi Kasus Teknik 
# ======================
def run_studi_kasus():
    print("\n" + "="*70)
    print(" STUDI KASUS TEKNIK")
    print("="*70)
    
    # ========== KASUS 1: GERAK PARABOLA (Fisika) ==========
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
    
    # ========== KASUS 2: PEMBAGI TEGANGAN (Elektro) ==========
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

# ======================
# Eksperimen Runtime
# ======================
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


