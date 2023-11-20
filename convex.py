import tkinter as tk
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from math import atan2

def ccw(p1, p2, p3):
    """ Check if three points make a counter-clockwise turn """
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

# Convex Hull Algorithms
def brute_force(points):
    def on_right(a, b, c):
        """ Return true if point c is on the right of line segment ab """
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) < 0

    hull = []
    for a in points:
        for b in points:
            if a == b:
                continue
            all_right = True
            for c in points:
                if c == a or c == b:
                    continue
                if not on_right(a, b, c):
                    all_right = False
                    break
            if all_right:
                hull.append(a)
                break

    # Order the hull points counterclockwise
    center = tuple(map(lambda x: sum(x) / len(hull), zip(*hull)))
    hull.sort(key=lambda p: atan2(p[1] - center[1], p[0] - center[0]))

    return hull

    # Extract unique points from the edges
    hull_points = list(set([point for edge in hull_edges for point in edge]))

    # Sort by angle from the first point to ensure proper ordering
    first_point = min(hull_points, key=lambda p: (p[1], p[0]))
    hull_points.sort(key=lambda p: (atan2(p[1] - first_point[1], p[0] - first_point[0]), -p[1], p[0]))

    return hull_points

def jarvis_march(points):
    def left_most_point(points):
        """ Find the leftmost point """
        return min(points, key=lambda p: p[0])

    def ccw(p1, p2, p3):
        """ Check if three points make a counter-clockwise turn """
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    def next_hull_point(points, current_point):
        """ Find the next point on the hull """
        next_point = points[0]
        for p in points:
            if p == current_point:
                continue
            if ccw(current_point, next_point, p) > 0 or (ccw(current_point, next_point, p) == 0 and 
                                                        ((p[0] - current_point[0])**2 + (p[1] - current_point[1])**2) > 
                                                        ((next_point[0] - current_point[0])**2 + (next_point[1] - current_point[1])**2)):
                next_point = p
        return next_point

    if len(points) < 3:
        # Convex hull is not defined for less than 3 points
        return points

    hull = []
    left_point = left_most_point(points)
    current_point = left_point

    while True:
        hull.append(current_point)
        next_point = next_hull_point(points, current_point)
        if next_point == left_point:
            # Wrapped around to the first point again
            break
        current_point = next_point

    return hull

def graham_scan(points):
    # Find the bottom-most point
    bottom_most = min(points, key=lambda p: (p[1], p[0]))
    
    # Sort points by polar angle relative to bottom_most point
    def polar_angle(p):
        return atan2(p[1] - bottom_most[1], p[0] - bottom_most[0])

    sorted_points = sorted(points, key=polar_angle)

    # Initialize the hull with the first three points
    hull = sorted_points[:3]

    for p in sorted_points[3:]:
        # While the angle formed by the last three points makes a non-left turn
        while len(hull) > 1 and ccw(hull[-2], hull[-1], p) <= 0:
            hull.pop()  # Remove the last point from the hull
        hull.append(p)  # Add the new point to the hull

    return hull

def quick_elimination(points):
    if len(points) < 4:
        return points

    # Find extreme points
    min_x = min(points, key=lambda p: p[0])
    max_x = max(points, key=lambda p: p[0])
    min_y = min(points, key=lambda p: p[1])
    max_y = max(points, key=lambda p: p[1])

    # Construct a coarse hull from the extreme points
    # Assuming no three of them are collinear
    coarse_hull = [min_x, min_y, max_x, max_y]

    # A function to check if a point is inside the coarse hull polygon
    def inside_coarse_hull(p):
        total = 0
        for i in range(len(coarse_hull)):
            j = (i + 1) % len(coarse_hull)
            if ccw(coarse_hull[i], coarse_hull[j], p) < 0:
                total += 1
        return total == len(coarse_hull)

    # Filter points that are not inside the coarse hull
    candidates = [p for p in points if not inside_coarse_hull(p)]

    # Use Jarvis March to find the convex hull from the remaining points
    return jarvis_march(candidates)


def chans_algorithm(points, m=None):
    def find_next_hull_point(sub_hulls, point_on_hull):
        """ Find the next point on the hull from sub hulls """
        next_point = None
        for hull in sub_hulls:
            for p in hull:
                if p == point_on_hull:
                    continue
                if next_point is None or ccw(point_on_hull, next_point, p) > 0:
                    next_point = p
        return next_point

    if m is None:
        m = len(points) // 2

    while m <= len(points):
        sub_hulls = []
        for i in range(0, len(points), m):
            sub_hull = graham_scan(points[i:i + m])
            if sub_hull:
                sub_hulls.append(sub_hull)

        point_on_hull = min(points, key=lambda p: p[0])
        hull = []

        for _ in range(m):
            hull.append(point_on_hull)
            next_point = find_next_hull_point(sub_hulls, point_on_hull)

            if next_point == hull[0]:
                return hull

            point_on_hull = next_point

        m *= 2

    return points

# Function to plot points and the convex hull
def plot_convex_hull(points, hull_points):
    # Unpack points for plotting
    x_coords, y_coords = zip(*points)
    
    # Create a figure and axis for the plot
    fig, ax = plt.subplots()
    
    # Plot the points
    ax.scatter(x_coords, y_coords, color='blue', label='Points')

    # Plot the convex hull
    hull_coords = hull_points + [hull_points[0]]  # Close the hull by adding the first point at the end
    hx, hy = zip(*hull_coords)
    ax.plot(hx, hy, color='red', label='Convex Hull')

    # Set plot properties
    ax.set_title("Convex Hull Visualization")
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")
    ax.legend()

    # Show the plot
    plt.show()

# Function to process points and selected algorithm
def process_points(points, algorithm):
    if algorithm.lower() == 'brute':
        hull_points = brute_force(points)
    elif algorithm.lower() == 'jarvis':
        hull_points = jarvis_march(points)
    elif algorithm.lower() == 'graham':
        hull_points = graham_scan(points)
    elif algorithm.lower() == 'quick':
        hull_points = quick_elimination(points)
    elif algorithm.lower() == 'chan':
        hull_points = chans_algorithm(points)
    else:
        raise ValueError("Invalid algorithm choice")

    return hull_points

# Function to handle random point generation
def generate_random_points():
    num_points = random.randint(15, 30)
    points = [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(num_points)]
    return points

# Function to get user input
def get_input(method):
    if method == "manual":
        point_string = simpledialog.askstring("Input", "Enter points (x1,y1 x2,y2 ...):")
        if point_string:  # Ensure that some input is given
            try:
                points = [tuple(map(float, p.split(','))) for p in point_string.split()]
            except ValueError:
                tk.messagebox.showerror("Input error", "Invalid format of points. Please enter points in x,y format.")
                return
        else:
            return
    elif method == "random":
        points = generate_random_points()

    algorithm = simpledialog.askstring("Input", "Choose algorithm: brute/jarvis/graham/quick/chan")
    if not algorithm or algorithm.lower() not in ['brute', 'jarvis', 'graham', 'quick', 'chan']:
        tk.messagebox.showerror("Input error", "Invalid algorithm choice.")
        return

    hull_points = process_points(points, algorithm)
    plot_convex_hull(points, hull_points)

# Create the main window
root = tk.Tk()
root.geometry("400x300")

# Add buttons for input methods
manual_button = tk.Button(root, text="Enter Points Manually", command=lambda: get_input("manual"))
manual_button.pack(pady=10)

random_button = tk.Button(root, text="Randomly Select Points", command=lambda: get_input("random"))
random_button.pack(pady=10)

root.mainloop()
