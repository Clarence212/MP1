import tkinter as tk
from tkinter import font
yes = { #diz is the priority of each operators
    '||': 1, '&&': 2, '!': 3,
    '==': 4, '!=': 4, '<': 5, '>': 5, '<=': 5, '>=': 5,
    '+': 6, '-': 6,
    '*': 7, '/': 7, '%': 7,
    '^': 8
} 
def is_operator(token): #so basically chinecheck nya lang if yung operator is nasa dictionary which is yung "yes" dict
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
def handle_implicit_multiplication(expression_str):
    processed_expression = ""
    i = 0
    while i < len(expression_str):
        current_char = expression_str[i]
        processed_expression += current_char
        if i + 1 < len(expression_str):
            next_char = expression_str[i+1]
            if current_char.isdigit() and next_char == '(':
                processed_expression += '*'            
            elif current_char == ')' and next_char.isdigit():
                processed_expression += '*'
            elif current_char == ')' and next_char == '(':
                processed_expression += '*'            
        i += 1
    return processed_expression

def infix_to_postfix(original_expression):
    # Step 1: Handle implicit multiplication first
    explicit_expression = handle_implicit_multiplication(original_expression)
    print(f"Original: {original_expression} -> Explicit: {explicit_expression}")

    try:
        eval_result = eval(explicit_expression) 
        return f"Converted to postfix (mock): {explicit_expression.replace('*', ' * ').replace('+', ' + ')} (evaluates to {eval_result})"
    except Exception as e:
        return f"Error during mock conversion: {e}"
print(infix_to_postfix("1(2*2)"))
print(infix_to_postfix("(2+3)(4-1)"))
print(infix_to_postfix("5(A+B)")) 
print(infix_to_postfix("1+2*3")) 


def tokenize(expr): #eto naman ginagawa nyang token yung each character in an expression
    tokens = []     #for example, 2+(2*2), magiging ['2','+','(','2','+','2',')'] sya, tas ma iistore sya dun sa tokens = []
    num = ""       #yung num naman na ito is para sa multi digit dumbers so if 123 magiging "123" not '1','2','3' 
    i = 0 #yung index when nag iiscan sya thru the token like tinitingnan nya kung anong current character ung iniiscan
    while i < len(expr): #tas eto naman yung loop na nag ruruun from left to right char by char
        if expr[i].isdigit(): #base don sa scanner pag na scan nya yung character as digit ilalagay nya sa loob ng "" ex. num = "123"
            num += expr[i]
        else:           # so eto naman is pag hindi na digit yung nababasa nya meaning tapos na yung current number at mag aappend na to sa  tokens = [] at mag rereset na ulet for the next one
            if num:
                tokens.append(num)
                num = ""
            if expr[i:i+2] in yes: #dito naman ay chinecheck kung may two character operator ba na tinype na intended like ==,<=, for example '&&' mag iiskip yan para hindi maging ['&','&']
                tokens.append(expr[i:i+2])
                i += 1
            elif expr[i] in yes or expr[i] in '()': #so if hindi naman double character operator, like * or parenthesis lang sya check mo parin and append mo din sa tokens
                tokens.append(expr[i])
            elif not expr[i].isspace():         #so pag hindi digit or hindi operator or space, mag eerror yann
                raise ValueError(f"Invalid character: {expr[i]}")
        i += 1    #pang moveforward lang ng loop hahaha
    if num: #pagnatapos na yung loop baka may laman pa yung num, add na kaagad yan sa tokens
        tokens.append(num)
    return tokens #return na yung whole token list ready na for the next step>>

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



###gui
root = tk.Tk()
root.title("MP1 - INFIX TO POSTFIX CALCULATOR")
root.geometry("700x400")
root.configure(bg="#f0f4f8")
title_font = font.Font(family="Helvetica", size=18, weight="bold")
label_font = font.Font(family="Helvetica", size=12)
entry_font = font.Font(family="Courier", size=14)
title_label = tk.Label(root, text="Infix to Postfix Stack Calculator - MP1 ", font=title_font, bg="#f0f4f8", fg="#333")
title_label.pack(pady=20)
entry = tk.Entry(root, font=entry_font, width=50, justify="center", bd=3, relief="groove")
entry.pack(pady=10)
calc_button = tk.Button(root, text="Evaluate Expression", font=label_font, bg="#0066ff", fg="white", padx=15, pady=5, command=lambda: calculate())
calc_button.pack(pady=10)
postfix_label = tk.Label(root, text="Postfix:", font=label_font, bg="#f0f4f8", fg="#555")
postfix_label.pack(pady=5)
result_label = tk.Label(root, text="Result:", font=label_font, bg="#43d14f", fg="#000", relief="groove", padx=10, pady=5, width=60, anchor="center")
result_label.pack(pady=10)
def calculate():
    expr = entry.get().strip()
    if not expr:
        postfix_label.config(text="Postfix: ")
        result_label.config(text="Nothing entered")
        return
    try:
        if len(expr) > 256:
            raise ValueError("Expression exceeds 256 characters, plz reduce expression")
        postfix = infix_to_postfix(expr)
        postfix_label.config(text="Postfix: " + ' '.join(postfix))
        result = evaluate_postfix(postfix)
        result_label.config(text="Result: " + str(result))
    except Exception as e:
        postfix_label.config(text="Postfix: Error")
        result_label.config(text=f"Error: {e}")

root.mainloop()
