def infix_to_postfix(tokens: List[str]) -> List[str]:
    output = []
    op_stack = Stack()
    for tok in tokens:
        if tok in FUNCS:
            op_stack.push(tok)
        elif tok == '(':
            op_stack.push(tok)
        elif tok == ')':
            while not op_stack.is_empty() and op_stack.peek() != '(':
                output.append(op_stack.pop())
            if op_stack.is_empty():
                raise ValueError("Parentheses tidak cocok")
            op_stack.pop()
            if not op_stack.is_empty() and op_stack.peek() in FUNCS:
                output.append(op_stack.pop())
        elif tok in PREC:
            while (not op_stack.is_empty() and op_stack.peek() != '(' and
                   (PREC[op_stack.peek()] > PREC[tok] or
                    (PREC[op_stack.peek()] == PREC[tok] and tok not in RASSOC))):
                output.append(op_stack.pop())
            op_stack.push(tok)
        else:
            output.append(tok)
    while not op_stack.is_empty():
        top = op_stack.pop()
        if top in '()':
            raise ValueError("Parentheses tidak cocok")
        output.append(top)
    return output
