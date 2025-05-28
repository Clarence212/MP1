yes = { #diz is the priority of each operators
    '||': 1, '&&': 2, '!': 3,
    '==': 4, '!=': 4, '<': 5, '>': 5, '<=': 5, '>=': 5,
    '+': 6, '-': 6,
    '*': 7, '/': 7, '%': 7,
    '^': 8
} 
def is_operator(token):
    return token in yes
def apply_operator(op, a, b=None):
    try:
        if op == '+': return a + b
        elif op == '-': return a - b
        elif op == '*': return a * b
        elif op == '/': return a // b if b != 0 else (_ for _ in ()).throw(ValueError("error: can't divide by 0")) 
        elif op == '%': return a % b
        elif op == '^': return a ** b
        elif op == '>': return int(a > b)
        elif op == '<': return int(a < b)
        elif op == '>=': return int(a >= b)
        elif op == '<=': return int(a <= b)
        elif op == '==': return int(a == b)
        elif op == '!=': return int(a != b)
        elif op == '&&': return int(a and b)
        elif op == '||': return int(a or b)
        elif op == '!': return int(not a)
    except Exception as e:
        raise ValueError(f"Invalid operation: {op} {a} {b}")
def tokenize(expr):
    tokens = []
    num = ""
    i = 0
    while i < len(expr):
        if expr[i].isdigit():
            num += expr[i]
        else:
            if num:
                tokens.append(num)
                num = ""
            if expr[i:i+2] in yes:
                tokens.append(expr[i:i+2])
                i += 1
            elif expr[i] in yes or expr[i] in '()':
                tokens.append(expr[i])
            elif not expr[i].isspace():
                raise ValueError(f"Invalid character: {expr[i]}")
        i += 1
    if num:
        tokens.append(num)
    return tokens

def infix_to_postfix(expr):
    output, stack = [], []
    tokens = tokenize(expr)
    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            found_paren = False
            while stack:
                top = stack.pop()
                if top == '(':
                    found_paren = True
                    break
                output.append(top)
            if not found_paren:
                raise ValueError("unclosedparentheses")
        elif is_operator(token):
            while (stack and stack[-1] != '(' and
                   yes[token] <= yes.get(stack[-1], 0)):
                output.append(stack.pop())
            stack.append(token)
    while stack:
        if stack[-1] in '()':
            raise ValueError("unclosed parentheses")
        output.append(stack.pop())
    return output
def evaluate_postfix(postfix):
    stack = []
    for token in postfix:
        if token.isdigit():
            stack.append(int(token))
        elif token == '!':
            if not stack:
                raise ValueError("missing operand for '!'")
            a = stack.pop()
            stack.append(apply_operator(token, a))
        else:
            if len(stack) < 2:
                raise ValueError(f"not enough operands for '{token}'")
            b = stack.pop()
            a = stack.pop()
            stack.append(apply_operator(token, a, b))
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    return stack[0]
