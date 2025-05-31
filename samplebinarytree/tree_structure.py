from tkinter import Canvas

# Function to visually display a binary tree structure on a Tkinter Canvas
def display_tree_structure(canvas: Canvas, root_node):
    if not root_node:
        return  # Exit early if there's no tree to display

    node_radius = 20          # Radius of each tree node (circle)
    vertical_gap = 70         # Vertical space between levels of the tree

    positions = {}  # Dictionary to store the (x, y) position of each node

    # Recursive function to calculate screen positions of each node
    def calculate_positions(node, depth=0, x=canvas.winfo_width() // 2, offset=200):
        if node is None:
            return

        # Assign the current node's position
        positions[node] = (x, depth * vertical_gap + 40)

        # Calculate position for left child, shifting left
        if node.left:
            calculate_positions(node.left, depth + 1, x - offset, offset // 2)

        # Calculate position for right child, shifting right
        if node.right:
            calculate_positions(node.right, depth + 1, x + offset, offset // 2)

    # Recursive function to draw nodes and their connecting lines
    def draw_nodes(node):
        if node is None:
            return

        x, y = positions[node]  # Current node's position

        # Draw line to left child, then draw the left subtree
        if node.left:
            lx, ly = positions[node.left]
            canvas.create_line(x, y, lx, ly)
            draw_nodes(node.left)

        # Draw line to right child, then draw the right subtree
        if node.right:
            rx, ry = positions[node.right]
            canvas.create_line(x, y, rx, ry)
            draw_nodes(node.right)

        # Draw the circle for the node
        canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill="#e9c347")
        # Draw the node's data (text) inside the circle
        canvas.create_text(x, y, text=str(node.data), font=("Arial", 12, "bold"))

    canvas.update()  # Update the canvas size before calculating positions
    calculate_positions(root_node)  # Step 1: Calculate all node positions
    draw_nodes(root_node)           # Step 2: Draw all nodes and lines