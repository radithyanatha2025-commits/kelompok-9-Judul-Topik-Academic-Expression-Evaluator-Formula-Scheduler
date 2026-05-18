def infix_to_postfix(tokens: List[str]) -> List[str]:
    output = []
    op_stack = Stack()
    for tok in tokens:
        if tok in FUNCS:          # fungsi unary
            op_stack.push(tok)
        elif tok == '(':
            op_stack.push(tok)
        elif tok == ')':
            while op_stack.peek() != '(':
                output.append(op_stack.pop())
            op_stack.pop()        # buang '('
            if op_stack.peek() in FUNCS:
                output.append(op_stack.pop())
        elif tok in PREC:         # operator
            while (not op_stack.is_empty() and 
                   prioritas(puncak) >= prioritas(tok)):
                output.append(op_stack.pop())
            op_stack.push(tok)
        else:                     # operand
            output.append(tok)
    # sisa operator
    while not op_stack.is_empty():
        output.append(op_stack.pop())
    return output
