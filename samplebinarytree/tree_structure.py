from tkinter import Canvas

# Gamit 'to para i-drawing ang buong binary tree sa canvas ng Tkinter
def display_tree_structure(canvas: Canvas, root_node):
    if not root_node:
        return  # Wala namang tree? Edi wag na. Alis na agad.

    node_radius = 20          # Gaano kalaki ang bilog ng bawat node
    vertical_gap = 70         # Gaano kalayo ang bawat level ng tree (para hindi dikit-dikit parang sardinas)

    positions = {}   # Dito natin i-store ang (x, y) na posisyon ng bawat node — parang address 

     # === Step 1: Kuha muna tayo ng coordinates ng bawat node (recursive)
    def calculate_positions(node, depth=0, x=canvas.winfo_width() // 2, offset=200):
        if node is None:
            return # Walang node dito? Wag na mag-calculate, sayang oras

        # I-assign ang posisyon ng current node base sa lalim at horizontal offset
        positions[node] = (x, depth * vertical_gap + 40) # 40 para di dikit sa taas

        # Kung may left child, calculate natin position niya (pakaliwa)
        if node.left:
            calculate_positions(node.left, depth + 1, x - offset, offset // 2)

        # Kung may right child, calculate natin position niya (pakanan)
        if node.right:
            calculate_positions(node.right, depth + 1, x + offset, offset // 2)

    # === Step 2: Drawing time
    def draw_nodes(node):
        if node is None:
            return  # Wala namang node, edi walang drawing

        x, y = positions[node]   # Kunin natin coordinates ng node na 'to or yung current position

        # Draw line to left child, then draw the left subtree
        if node.left:
            lx, ly = positions[node.left]
            canvas.create_line(x, y, lx, ly)  # draw ng linya from parent to left child
            draw_nodes(node.left) # Drawing ng buong kaliwang subtree

        # Kung may anak sa kanan, same drill
        if node.right:
            rx, ry = positions[node.right]
            canvas.create_line(x, y, rx, ry)
            draw_nodes(node.right)

        # Drawing ng node mismo — bilog, para legit mukhang node
        canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="#e9c347")
        # Text sa loob ng bilog — ito 'yung value ng node
        canvas.create_text(x, y, text=str(node.data), font=("Arial", 12, "bold"))

    canvas.update()    # I-update muna ang canvas dimensions para sure ang layout 
    calculate_positions(root_node)  # Step 1: Calculate all node positions
    draw_nodes(root_node)           # Step 2: Draw all nodes and lines
