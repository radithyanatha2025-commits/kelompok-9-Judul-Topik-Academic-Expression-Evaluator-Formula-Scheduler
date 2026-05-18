def eval_postfix(tokens: List[str], var_table: 'VarBST') -> float:
    """
    Evaluasi ekspresi postfix menggunakan Stack Linked List.
    Lookup variabel dari var_table (BST).
    Mendukung fungsi unary: sin, cos, sqrt, log, abs.
    Big-O: O(n) — setiap token diproses tepat sekali.
 
    Algoritma:
    - Angka/variabel → push ke stack
    - Fungsi unary  → pop 1 operand, terapkan, push hasil
    - Operator biner → pop 2 operand (b dulu, lalu a), hitung a OP b, push
    """
    stack = Stack()
 
    for tok in tokens:
        if tok in FUNCS:
            # Fungsi unary: pop satu operand
            if stack.is_empty():
                raise ValueError(f'Fungsi {tok!r} tidak punya operand')
            operand = stack.pop()
            try:
                result = FUNCS[tok](operand)
            except Exception as e:
                raise ValueError(f'Error saat menghitung {tok}({operand}): {e}')
            stack.push(result)
 
        elif tok in PREC:
            # Operator biner: pop dua operand
            if stack.size() < 2:
                raise ValueError(f'Operator {tok!r} tidak cukup operand')
            b = stack.pop()  # operand kanan
            a = stack.pop()  # operand kiri
            if tok == '+':
                stack.push(a + b)
            elif tok == '-':
                stack.push(a - b)
            elif tok == '*':
                stack.push(a * b)
            elif tok == '/':
                if b == 0:
                    raise ValueError('Pembagian dengan nol')
                stack.push(a / b)
            elif tok == '^':
                stack.push(a ** b)
 
        elif tok.replace('.', '', 1).lstrip('-').isdigit():
            # Angka literal
            stack.push(float(tok))
 
        else:
            # Variabel: lookup dari BST
            val = var_table.get(tok)
            if val is None:
                raise ValueError(f"Variabel '{tok}' belum di-SET")
            stack.push(val)
 
    if stack.is_empty():
        raise ValueError('Ekspresi kosong')
    result = stack.pop()
    if not stack.is_empty():
        raise ValueError('Ekspresi tidak valid: terlalu banyak operand')
    return result
 
