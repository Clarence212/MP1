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

def infix_to_postfix(expr): #eto naman yung function na mag coconvert from infix to postfix
    output, stack = [], [] #dito ihohold yung postfix result / Stack is para sa operators
    tokens = tokenize(expr) #eto na yung tokens na nabreakdown into manageable pieces
    for token in tokens: #mag loloop ito sa each tokens sa infix expression
        if token.isdigit():
            output.append(token) #if yung na loop nya na token is digit, is idadagdag nya yan sa output list. Mauuna muna yung numbers b4 yung operators
        elif token == '(': #pag left parenthesis mag pupush yan sa stack, lahat ng operators after nito ma eevaluate seperately before the closing parenthesis
            stack.append(token)
        elif token == ')': #pag right parenthesis naman po ipopop nya na yung operators from the stack tas i aadd na yun sa output hanggang mahanap yung closing
            found_paren = False
            while stack:
                top = stack.pop()
                if top == '(':
                    found_paren = True
                    break
                output.append(top)
            if not found_paren:
                raise ValueError("unclosedparentheses") #if hindi na close yung parenthesis mag raraise yan ng error
        elif is_operator(token):   #so eto naman uhh mag rurunn sya if yung current token is an operator, also naka depende kung anong priority(precedence) nung operator
            while (stack and stack[-1] != '(' and 
                   yes[token] <= yes.get(stack[-1], 0)):
                output.append(stack.pop()) #pinopop nya from stack to output
            stack.append(token)
    while stack: #final cleanupp nagchecheck lang if may laman pa yung stack pag parenthesis yung natira mag raraise yan ng error pag hindi naman parenthesis pop lang papuntang output :)
        if stack[-1] in '()':
            raise ValueError("unclosed parentheses")
        output.append(stack.pop())
    return output #all donee irereturn na yung fully converted na infix to postfix expression

def evaluate_postfix(postfix):  #so dito mag dedefine tayo ng function na nageevalutate ng postfix expression
    stack = [] #empty stack ulet for for storing sa items while nag eevaluate
    for token in postfix: #mag loloop sya
        if token.isdigit(): #if yung nadaanan nya na character is digit mag pupush yan sa stack ready na ma evaluate until may operator na madaanan yung loop
            stack.append(int(token)) #convert to int tapos mag push sya sa stack
        elif token == '!': #so eto naman para to sa logical operator na !, isang operand lang kasi need neto atleast 1, otherwise error sya
            if not stack:
                raise ValueError("missing operand for !")
            a = stack.pop()
            stack.append(apply_operator(token, a))
        else:  #eto naman chinecheck nya if sapat na yung operand para sa current operator like +,+,/, kasi ito need atleast 2 operands unlike ! na isa lang sapat na
            if len(stack) < 2:
                raise ValueError(f"not enough operands for '{token}'") #error if kulang yung operand
            b = stack.pop() #una i push si b sa top
            a = stack.pop()# then si a second top
            stack.append(apply_operator(token, a, b)) #push pabalik sa stack
    if len(stack) != 1: #after nung loop dapat isa lang matitira sa stack which is yung final answer pag wala or sobra mag eeror sha
        raise ValueError("Invalid expression") #error handler nya
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
