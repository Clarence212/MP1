# Import necessary modules from tkinter, filedialog,messagebox, os, other file
from tkinter import *
from tkinter import filedialog, messagebox
import os
from tree_structure import display_tree_structure  # Import function to display tree graphically

# Define class for Node ng Binary Tree
class Node:
    def __init__(self, value):
        self.left = None       # Left child
        self.right = None      # Right child
        self.data = value      # Value of the node
        self.parent = None     # Parent node reference

# Define class for the Binary Tree
class Tree:
    def createnode(self, data):
        return Node(data)  # Gumagawa ng bagong Node object

    def insert(self, node, data, parent=None):
        # Recursive insertion ng node sa tamang position
        if node is None:
            new_node = self.createnode(data)
            new_node.parent = parent  # I-set ang parent ng bagong node
            return new_node
        if data < node.data:
            node.left = self.insert(node.left, data, node)
        else:
            node.right = self.insert(node.right, data, node)
        return node

    # Inorder Traversal (LDR)
    def traverse_inorder(self, root, result):
        if root:
            self.traverse_inorder(root.left, result)
            result.append(str(root.data))
            self.traverse_inorder(root.right, result)

    # Preorder Traversal (DLR)
    def traverse_preorder(self, root, result):
        if root:
            result.append(str(root.data))
            self.traverse_preorder(root.left, result)
            self.traverse_preorder(root.right, result)

    # Postorder Traversal (LRD)
    def traverse_postorder(self, root, result):
        if root:
            self.traverse_postorder(root.left, result)
            self.traverse_postorder(root.right, result)
            result.append(str(root.data))

    # Kinokolekta lahat ng node info: parent, sibling, left, right, degree, depth
    def collect_nodes_info(self, node, depth=0, nodes_info=None):
        if nodes_info is None:
            nodes_info = []

        if node is None:
            return nodes_info

        # Hanapin parent value
        parent_val = node.parent.data if node.parent else "NULL"
        
        # Hanapin sibling
        sibling = "NULL"
        if node.parent:
            if node.parent.left == node and node.parent.right is not None:
                sibling = str(node.parent.right.data)
            elif node.parent.right == node and node.parent.left is not None:
                sibling = str(node.parent.left.data)

        # I-get values ng left at right child
        left_val = str(node.left.data) if node.left else "NULL"
        right_val = str(node.right.data) if node.right else "NULL"
        degree = int(bool(node.left)) + int(bool(node.right))  # Bilang ng anak (degree)

        # I-add sa info list
        nodes_info.append([
            str(node.data), parent_val, sibling, left_val, right_val, str(degree), str(depth)
        ])

        # Recursive call para sa left at right subtrees
        self.collect_nodes_info(node.left, depth + 1, nodes_info)
        self.collect_nodes_info(node.right, depth + 1, nodes_info)

        return nodes_info

# Global variables
tree = Tree()           # Instance ng Tree class
root_node = None        # Root ng binary tree
number_list = []        # List of numbers from file


# Function to browse and select file
def browse_file():
    path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if path:
        file_entry.delete(0, END)        # Clear current text sa entry
        file_entry.insert(0, path)       # I-set ang selected file path

# Function to load file and build binary tree
def load_file():
    global number_list, tree, root_node
    filepath = file_entry.get().strip()

    # I-check kung valid ang file extension
    if not filepath.endswith(".txt"):
        messagebox.showerror("Invalid File", "Please select a valid .txt file.")
        return

    # I-check kung existing ang file
    if not os.path.exists(filepath):
        messagebox.showerror("File Not Found", "The file does not exist.")
        return

    try:
        with open(filepath, "r") as file:
            lines = file.readlines()

        # Clean lines: remove empty at spaces
        lines = [line.strip() for line in lines if line.strip()]

        # I-check kung walang laman
        if not lines:
            messagebox.showwarning("Empty File", "The file is empty.")
            return

        # I-validate kung lahat ng line ay integers lang
        def validline(line):
            return line.isdigit() or (line.startswith('-') and line[1:].isdigit())

        if all(validline(line) for line in lines):
            number_list = list(map(int, lines))  # Convert to list of ints

            # Check for duplicates
            if len(number_list) != len(set(number_list)):
                messagebox.showerror("Duplicate Entry", "The file contains duplicate numbers. Please remove them.")
                return

            root_node = None  # Reset tree
            for num in number_list:
                root_node = tree.insert(root_node, num)
            messagebox.showinfo("Success", f"Loaded: {', '.join(map(str, number_list))}")
        else:
            messagebox.showerror("Invalid Format", "Each number must be on a separate line. No commas or spaces.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to display traversals on canvas
def traverse_display():
    canvas.delete("all")  # Clear canvas
    if not number_list:
        messagebox.showerror("No Data", "Please load a file with valid numbers first.")
        return

    pre, ino, post = [], [], []
    tree.traverse_preorder(root_node, pre)
    tree.traverse_inorder(root_node, ino)
    tree.traverse_postorder(root_node, post)

    # Display results ng traversals with ube cheese colors
    canvas.create_text(20, 40, anchor="w", text="Preorder:  " + ' '.join(pre),
                       font=("Segoe UI", 14, "bold"), fill="#5b2c6f")  # dark purple text
    canvas.create_text(20, 80, anchor="w", text="Inorder:   " + ' '.join(ino),
                       font=("Segoe UI", 14, "bold"), fill="#5b2c6f")
    canvas.create_text(20, 120, anchor="w", text="Postorder: " + ' '.join(post),
                       font=("Segoe UI", 14, "bold"), fill="#5b2c6f")


def display_node_table():
    canvas.delete("all")  # Clear canvas
    if not root_node:
        messagebox.showerror("No Data", "Please load a file with valid numbers first.")
        return

    headers = ['Node', 'Parent', 'Sibling', 'Left', 'Right', 'Degree', 'Depth']
    table = tree.collect_nodes_info(root_node)

    col_width = canvas.winfo_width() // len(headers)
    row_height = 30
    start_y = 40

    # Header row 
    canvas.create_rectangle(0, start_y-30, canvas.winfo_width(), start_y, fill="#8e44ad")
    for i, header in enumerate(headers):
        x = i * col_width
        canvas.create_text(x + col_width//2, start_y - 15, text=header,
                           font=("Segoe UI", 14, "bold"), fill="#f9e79f")  # creamy yellow text

    # Line below header - ube purple
    canvas.create_line(0, start_y, canvas.winfo_width(), start_y, fill="#8e44ad", width=2)

    # Data rows 
    for r, row in enumerate(table):
        bg_color = "#fcf3cf" if r % 2 == 0 else "#f9e79f"  # light and darker creamy yellow
        canvas.create_rectangle(0, start_y + r*row_height, canvas.winfo_width(),
                                start_y + (r+1)*row_height, fill=bg_color, outline="")
        for c, val in enumerate(row):
            x = c * col_width
            y = start_y + (r + 0.5) * row_height
            canvas.create_text(x + col_width//2, y, text=val,
                               font=("Segoe UI", 12), fill="#5b2c6f")  # dark purple text

    # Draw vertical grid lines
    for i in range(len(headers)+1):
        x = i * col_width
        canvas.create_line(x, start_y-30, x, start_y + row_height * len(table),
                           fill="#8e44ad", width=1)
# Function to show graphical tree structure
def display_tree():
    canvas.delete("all")
    if not root_node:
        messagebox.showerror("No Data", "Please load a file with valid numbers first.")
        return
    display_tree_structure(canvas, root_node)  # External function to draw tree

# Mouse hover effects para sa buttons
def on_enter_btn(e):
    e.widget['background'] = '#f7b733'   # Cheese accent yellow on hover
    e.widget['foreground'] = '#6a4c93'   # Ube purple text on hover

def on_leave_btn(e):
    e.widget['background'] = '#9f7aea'   # Lighter Ube purple normal bg
    e.widget['foreground'] = 'white'     # White text normally


# GUI

window = Tk()
window.title("Puno ni sir Javier")
window.geometry("950x950")      # Set window size
window.configure(bg="#f3e9f9")  # background
window.resizable(False, False)

# Title Frame
title_frame = Frame(window, bg="#6a4c93", pady=15)  # Dark ube purple
title_frame.pack(fill=X)

title_label = Label(title_frame, text="Binary Tree ", font=("Segoe UI", 24, "bold"), bg="#6a4c93", fg="#f6d365")  # Cheese yellow text
title_label.pack()

# File Selection Frame
file_frame = Frame(window, bg="#f3e9f9", pady=15)
file_frame.pack(fill=X, padx=20)

file_label = Label(file_frame, text="Select a .txt file:", font=("Segoe UI", 14), bg="#f3e9f9", fg="#6a4c93")
file_label.pack(side=LEFT, padx=(0, 10))

file_entry = Entry(file_frame, font=("Segoe UI", 14), width=45)
file_entry.pack(side=LEFT, padx=10)

browse_button = Button(file_frame, text="Browse", font=("Segoe UI", 12, "bold"), bg="#9f7aea", fg="white", relief=FLAT, padx=15, pady=7, cursor="hand2", command=browse_file)
browse_button.pack(side=LEFT, padx=10)
browse_button.bind("<Enter>", on_enter_btn) # Hover in
browse_button.bind("<Leave>", on_leave_btn) # Hover out

# Control Buttons Frame
buttons_frame = Frame(window, bg="#f3e9f9", pady=10)
buttons_frame.pack(fill=X, padx=20)

# Load File button 
load_button = Button(buttons_frame, text="Load File", font=("Segoe UI", 14, "bold"), bg="#9f7aea", fg="white", relief=FLAT, padx=20, pady=10, cursor="hand2", command=load_file)
load_button.pack(side=LEFT, padx=10)
load_button.bind("<Enter>", on_enter_btn)
load_button.bind("<Leave>", on_leave_btn)


# Button to show Pre, In, Post traversals
draw_button = Button(buttons_frame, text="Display Traversals", font=("Segoe UI", 14, "bold"), bg="#9f7aea", fg="white", relief=FLAT, padx=20, pady=10, cursor="hand2", command=traverse_display)
draw_button.pack(side=LEFT, padx=10)
draw_button.bind("<Enter>", on_enter_btn)
draw_button.bind("<Leave>", on_leave_btn)

# Button to show Node Table (Node, Parent, etc.)
table_button = Button(buttons_frame, text="Display Node Table", font=("Segoe UI", 14, "bold"), bg="#9f7aea", fg="white", relief=FLAT, padx=20, pady=10, cursor="hand2", command=display_node_table)
table_button.pack(side=LEFT, padx=10)
table_button.bind("<Enter>", on_enter_btn)
table_button.bind("<Leave>", on_leave_btn)

# Button to show tree structure graphically
tree_button = Button(buttons_frame, text="Display Tree Structure", font=("Segoe UI", 14, "bold"), bg="#9f7aea", fg="white", relief=FLAT, padx=20, pady=10, cursor="hand2", command=display_tree)
tree_button.pack(side=LEFT, padx=10)
tree_button.bind("<Enter>", on_enter_btn)
tree_button.bind("<Leave>", on_leave_btn)

# Canvas frame for outputs
canvas_frame = Frame(window, bg="#d6cdea", padx=5, pady=5)  # Soft light purple bg for canvas frame
canvas_frame.pack(padx=20, pady=20, fill=BOTH, expand=True)


# Canvas itself (drawing area)
canvas = Canvas(canvas_frame, width=900, height=720, bg="white", highlightthickness=0)
canvas.pack()

window.mainloop()
