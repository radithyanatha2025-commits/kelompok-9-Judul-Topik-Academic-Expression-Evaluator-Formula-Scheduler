def eval_postfix(tokens: List[str], var_table: Dict[str, float]) -> float:
    stack = Stack()  # Stack untuk operand
    
    for tok in tokens:
        # KASUS 1: Fungsi unary
        if tok in FUNCS:
            arg = stack.pop()
            if tok == 'sin':   res = math.sin(arg)
            elif tok == 'cos': res = math.cos(arg)
            elif tok == 'sqrt': res = math.sqrt(arg)
            elif tok == 'log':  res = math.log(arg)
            elif tok == 'abs':  res = abs(arg)
            stack.push(res)
        
        # KASUS 2: Operator biner
        elif tok in PREC:
            b = stack.pop()  # operand kanan
            a = stack.pop()  # operand kiri
            if tok == '+': res = a + b
            elif tok == '-': res = a - b
            elif tok == '*': res = a * b
            elif tok == '/': res = a / b
            elif tok == '^': res = a ** b
            stack.push(res)
        
        # KASUS 3: Operand (angka atau variabel)
        else:
            try:
                val = float(tok)  # angka
            except ValueError:
                val = var_table[tok]  # variabel (cari di BST)
            stack.push(val)
    
    result = stack.pop()
    
    # Cek apakah stack kosong (tidak boleh ada sisa)
    if not stack.is_empty():
        raise ValueError("Ekspresi tidak valid")
    
    return result
