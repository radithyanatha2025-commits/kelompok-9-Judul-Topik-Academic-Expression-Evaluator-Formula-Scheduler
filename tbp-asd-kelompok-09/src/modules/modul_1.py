def infix_to_postfix(tokens: List[str]) -> List[str]:
    output = []           # Hasil akhir (postfix)
    op_stack = Stack()    # Stack untuk operator
    
    for tok in tokens:
        # KASUS 1: Fungsi unary (sin, cos, dll)
        if tok in FUNCS:
            op_stack.push(tok)   

        # KASUS 2: Kurung buka   
        elif tok == '(':
            op_stack.push(tok)
        
        # KASUS 3: Kurung tutup
        elif tok == ')':
            # Pop semua operator sampai ketemu '('
            while not op_stack.is_empty() and op_stack.peek() != '(':
                output.append(op_stack.pop())
            # Buang '(' dari stack
            op_stack.pop() 
            # Jika ada fungsi di stack, pindahkan ke output
            if not op_stack.is_empty() and op_stack.peek() in FUNCS:
                output.append(op_stack.pop())
        
        # KASUS 4: Operator biner (+, -, *, /, ^)
        elif tok in PREC:
            # Pop operator dengan prioritas lebih tinggi atau sama
            while (not op_stack.is_empty() and 
                   op_stack.peek() != '(' and
                   (PREC[op_stack.peek()] > PREC[tok] or
                    (PREC[op_stack.peek()] == PREC[tok] and tok not in RASSOC))):
                output.append(op_stack.pop())
            op_stack.push(tok)
        
        # KASUS 5: Operand (angka/variabel)
        else:
            output.append(tok)
    
    # Sisa operator di stack, pindahkan semua ke output
    while not op_stack.is_empty():
        top = op_stack.pop()
        if top in '()':
            raise ValueError("Parentheses tidak cocok")
        output.append(top)
    
    return output
