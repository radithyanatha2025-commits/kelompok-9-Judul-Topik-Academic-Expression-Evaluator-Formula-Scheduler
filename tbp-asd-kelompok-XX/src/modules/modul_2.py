def eval_postfix(tokens, var_table):
    stack = Stack()
    for tok in tokens:
        if tok in FUNCS:
            arg = stack.pop()
            stack.push(hitung_fungsi(tok, arg))
        elif tok in PREC:
            b = stack.pop()
            a = stack.pop()
            stack.push(hitung_operator(tok, a, b))
        else:
            # angka atau variabel
            stack.push(float(tok) if tok not in var_table 
                       else var_table[tok])
    return stack.pop()
                                                                                                                    
