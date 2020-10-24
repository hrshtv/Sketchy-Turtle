import cv2
import aced
import argparse
import numpy as np
from turtle import Turtle, Screen
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = [10, 10] # Bigger plots

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-in", type=str, required=True)
parser.add_argument("--output", "-o", type=str, required=True)
parser.add_argument("--width", "-wt", type=int, required=True)
parser.add_argument("--height", "-ht", type=int, required=True)
args = parser.parse_args()

INPUT_PATH = args.input
OUTPUT_PATH = args.output
W = args.width
H = args.height

# CONSTANTS: You may need to tune some of this wrt to the image used
THRESHOLD_VAL = 50 # Cutoff value for binary thresholding
SHAPE = (W, H) # Shape of the image (Width, Height), as well as the screen size
CUTOFF_LEN = ((W+H)/2)/50 # Constant that ensures only continuous lines are drawn

"""FUNCTIONS:"""

def preprocess(src, cutoff, shape=(240, 240)):
    """Pre-processes the image"""
    # Resizing the image, for computational reasons, else the algorithm will take too much time
    dst = cv2.resize(src, shape)
    # (automated) Canny Edge Detection
    dst = aced.detect(dst)
    # Binary or Adaptive thresholding
    dst = aced.thresh(dst, cutoff, method='bin')
    return dst

def init_screen(W, H):
    """Initializes the screen"""
    screen = Screen()
    screen.bgcolor('black')
    screen.setup(W + 10, H + 10) # Padding for the sidebars and title bars
    return screen

def init_turtle():
    """Initializes the turtle"""
    t = Turtle(shape='turtle')
    t.resizemode('user')
    t.turtlesize(0.6, 0.6, 0)
    t.color('red')
    t.pencolor('white')
    t.speed('fastest')
    return t

def find_closest(p):
    """Returns the nearest neighbour of a point"""
    if len(positions) > 0: # 'positions' is a global variable
        nodes = np.array(positions)
        distances = np.sum((nodes - p)**2, axis=1) 
        i_min = np.argmin(distances)
        return positions[i_min] # The positons of the closest neighbour
    else:
        # We have traveresed over all the 'white' pixels in the image, positions[] is empty
        return None
    
"""MAIN"""

# Image input and pre-processing
src = cv2.imread(INPUT_PATH, 0) # Read as grayscale image
dst = preprocess(src, cutoff=THRESHOLD_VAL, shape=SHAPE)
aced.dispim(dst) # Displays the detected image which will be drawn

# Initializing the screen and the turtle
screen = init_screen(W, H)
t = init_turtle()

# Extract the binary edge-matrix's indices
iH, iW = np.where(dst == 1) # Edges will have the value as 1, as a result of binary thresholding
# Shift of origin, and y-axis flip, for conversion into turtle coordinates
iW = iW - W/2
iH = -1*(iH - H/2)
# Positions of edge pixels:
positions = [list(iwh) for iwh in zip(iW, iH)] # Another way will be : list(zip(iW, iH))

# Take the turtle to the initial position
t.penup()
t.goto(positions[0])
t.pendown()

"""Iterative approach, more robust, and doesn't crash, unlike the recursive approach"""
p = positions[0]
while (p):
    p = find_closest(p)
    if p:    
        current_pos = np.asarray(t.pos())
        new_pos = np.asarray(p)
        length = np.linalg.norm(new_pos - current_pos)
        if length < CUTOFF_LEN:
            t.goto(p)  # Go to the closest neighbour, keeping the pen down
        else:
            t.penup()
            t.goto(p)  # Go to the closest neighbour, keeping the pen up
            t.pendown()         
        positions.remove(p) # To ensure that we don't go back to the point     
    else:     
        p = None

# Saving the file as an .eps file, convert it to png using any online tool/cmd line tool
screen.getcanvas().postscript(file = OUTPUT_PATH + ".eps")
screen.exitonclick()