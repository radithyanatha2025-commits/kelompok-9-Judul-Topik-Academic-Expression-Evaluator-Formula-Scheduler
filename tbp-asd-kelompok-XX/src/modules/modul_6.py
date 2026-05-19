def tokenize(expr : str) -> list:
  """
  memecah string ekspresi menjadi list token.
  Mendukung angka, variabel (a-z), fungsi, operator, kurung.
  """
  tokens = []
  i = 0
  n = len(expr)
  while i < n:
    ch = expr[i]
    if ch.isspace():
        i += 1
        continue
    if ch.isdigit() or (ch == '.' and i+1 < n and expr[i+1].isdigit()):
        j = i
        while j < n and (expr[j].isdigit() or expr[j] == '.'):
            j += 1
        tokens.append(expr[i:j])
        i = j
        continue
    if ch.isalpha():
        j = i
        while j < n and expr[j].isalpha():
            j += 1
        tokens.append(expr[i:j])
        i = j
        continue
    if ch in '+-*/^()':
        tokens.append(ch)
        i += 1
        continue
    raise ValueError(f"Karakter tidak dikenal: '{ch}'")
return tokens


