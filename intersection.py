import tkinter as tk
from tkinter import simpledialog
import matplotlib.pyplot as plt


def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0  # colinear
    return 1 if val > 0 else 2  # clock or counterclock wise

def on_segment(p, q, r):
    if min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1]):
        return True
    return False

# Function to check intersection
def cross_product_intersect(p1, q1, p2, q2):
    # Find orientations
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special Cases
    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True

    return False

# Vector Method for Intersection
def vector_intersect(p1, q1, p2, q2):
    A = [q1[0] - p1[0], q1[1] - p1[1]]
    B = [p2[0] - q2[0], p2[1] - q2[1]]
    C = [p2[0] - p1[0], p2[1] - p1[1]]

    alpha = (B[1] * C[0] - B[0] * C[1]) / (A[0] * B[1] - A[1] * B[0])
    beta  = (A[0] * C[1] - A[1] * C[0]) / (A[0] * B[1] - A[1] * B[0])

    if 0 <= alpha <= 1 and 0 <= beta <= 1:
        return True  # Intersection occurs
    return False  # No Intersection

# Simple Geometric Method as an alternative to Sweep Line
def simple_geometric_intersect(p1, q1, p2, q2):
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    return ccw(p1, p2, q2) != ccw(q1, p2, q2) and ccw(p1, q1, p2) != ccw(p1, q1, q2)

# Function to plot the line segments
def plot_segments(segment1, segment2, intersect):
    x_vals = [segment1[0][0], segment1[1][0], segment2[0][0], segment2[1][0]]
    y_vals = [segment1[0][1], segment1[1][1], segment2[0][1], segment2[1][1]]

    plt.plot([segment1[0][0], segment1[1][0]], [segment1[0][1], segment1[1][1]], 'ro-')
    plt.plot([segment2[0][0], segment2[1][0]], [segment2[0][1], segment2[1][1]], 'bo-')
    
    if intersect:
        plt.title("Line Segments Intersect")
    else:
        plt.title("Line Segments Do Not Intersect")

    plt.xlim(min(x_vals) - 1, max(x_vals) + 1)
    plt.ylim(min(y_vals) - 1, max(y_vals) + 1)
    plt.grid()
    plt.show()

# Function to get user input and process it
def get_input():
    segment1 = simpledialog.askstring("Input", "Enter Segment 1 (x1,y1,x2,y2):")
    segment2 = simpledialog.askstring("Input", "Enter Segment 2 (x1,y1,x2,y2):")

    segment1 = tuple(map(int, segment1.split(',')))
    segment2 = tuple(map(int, segment2.split(',')))
    
    segment1 = ((segment1[0], segment1[1]), (segment1[2], segment1[3]))
    segment2 = ((segment2[0], segment2[1]), (segment2[2], segment2[3]))

    method = simpledialog.askstring("Input", "Choose method: cross/vector/geometric")
    if method.lower() == 'cross':
        intersect = cross_product_intersect(*segment1, *segment2)
    elif method.lower() == 'vector':
        intersect = vector_intersect(*segment1, *segment2)
    elif method.lower() == 'geometric':
        intersect = simple_geometric_intersect(*segment1, *segment2)
    else:
        messagebox.showerror("Error", "Invalid method. Please enter 'cross', 'vector', or 'geometric'.")
        return

    plot_segments(segment1, segment2, intersect)

root = tk.Tk()
root.geometry("300x100")

button = tk.Button(root, text="Enter Line Segments", command=get_input)
button.pack(pady=20)

root.mainloop()