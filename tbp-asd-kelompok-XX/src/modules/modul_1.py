def infix_to_postfix(tokens: List[str]) -> List[str]:
    """
    Konversi token infix ke postfix menggunakan Stack Linked List.
    Algoritma: Shunting-Yard (Dijkstra).
    Big-O: O(n) waktu, O(n) ruang — setiap token diproses tepat sekali.
 
    Aturan precedence: ^ > * / > + -
    ^ adalah right-associative, sisanya left-associative.
    Fungsi (sin, cos, dll.) diperlakukan sebagai operator unary.
    """
    output: List[str] = []
    op_stack = Stack()
 
    for tok in tokens:
        if tok.replace('.', '', 1).lstrip('-').isdigit():
            # Token adalah angka → langsung ke output
            output.append(tok)
 
        elif tok in FUNCS:
            # Token adalah fungsi → push ke op_stack
            op_stack.push(tok)
 
        elif tok in PREC:
            # Token adalah operator
            # Pop operator dari stack jika:
            # - top bukan kurung kiri, DAN
            # - (top adalah fungsi ATAU precedence top > tok ATAU
            #    (precedence sama DAN tok left-associative))
            while (not op_stack.is_empty() and
                   op_stack.peek() != '(' and
                   (op_stack.peek() in FUNCS or
                    (op_stack.peek() in PREC and
                     (PREC[op_stack.peek()] > PREC[tok] or
                      (PREC[op_stack.peek()] == PREC[tok] and tok not in RASSOC))))):
                output.append(op_stack.pop())
            op_stack.push(tok)
 
        elif tok == '(':
            # Kurung buka → push ke stack
            op_stack.push(tok)
 
        elif tok == ')':
            # Kurung tutup → pop sampai ketemu kurung buka
            while not op_stack.is_empty() and op_stack.peek() != '(':
                output.append(op_stack.pop())
            if op_stack.is_empty():
                raise ValueError('Kurung tidak seimbang: kurung tutup berlebih')
            op_stack.pop()  # buang '('
            # Jika ada fungsi di atas stack, pop ke output
            if not op_stack.is_empty() and op_stack.peek() in FUNCS:
                output.append(op_stack.pop())
 
        else:
            # Token adalah variabel
            output.append(tok)
 
    # Pop semua sisa operator dari stack
    while not op_stack.is_empty():
        top = op_stack.pop()
        if top == '(':
            raise ValueError('Kurung tidak seimbang: kurung buka berlebih')
        output.append(top)
 
    return output
