import sys
from tkinter import *
import time
from Point import Point
# Matthew Pisano
# 6/6/2020
# Simple pathfinding program

# basis grid of gui and keeping track of already checked squares
grid = [[0]*50 for _ in range(50)]
# sets upper left corner to 1 (start of path) and bottom right to 2 (end of path)
grid[0][0] = 1
grid[len(grid)-1][len(grid[0])-1] = 2

# store the start and end positions [x, y]
start = [0, 0]
end = [0, 0]
print("grid dims, Y:", len(grid), "X:", len(grid[0]))
# searches grid for start (1) and end(2) signals and assigns their positions to lists
for y in range(len(grid[0])):
    print("Next")
    for x in range(len(grid)):
        print(x, y, grid[x][y])
        if grid[x][y] == 1:
            start = [x, y]
        if grid[x][y] == 2:
            end = [x, y]

print("Start", start, "End", end)


# returns the distance between given points
def distance(x1, y1, x2, y2):
    return (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** (1 / 2)


# using recursion, the shortest path from the current point to the end square is calculated and drawn on screen
def pather(x: int, y: int):
    # stores minimum distance from the closest tested point to the end
    min = 9001
    # the current x coordinate of the closest tested point to the end
    nextX = 0
    # the current x coordinate of the closest tested point to the end
    nextY = 0
    # Tests each possible direction, and stores the direction with the shortest distance to the end
    # Test cardinal directions
    # Top
    if y > 0:
        top = distance(x, y - 1, end[1], end[0])
        print("Top from ", x, y, " to ", x, y - 1, " dist: ", top)
        if top < min and grid[y-1][x] != 1:
            min = top
            nextX = x
            nextY = y - 1
    # Left
    if x > 0:
        left = distance(x - 1, y, end[1], end[0])
        print("Left from ", x, y, " to ", x - 1, y, " dist: ", left)
        if left < min and grid[y][x-1] != 1:
            min = left
            nextX = x - 1
            nextY = y
    # Right
    if x < len(grid[0]) - 1:
        right = distance(x + 1, y, end[1], end[0])
        print("Right from ", x, y, " to ", x + 1, y, " dist: ", right)
        if right < min and grid[y][x+1] != 1:
            min = right
            nextX = x + 1
            nextY = y
    # Bottom
    if y < len(grid) - 1:
        bottom = distance(x, y + 1, end[1], end[0])
        print("Bottom from ", x, y, " to ", x, y + 1, " dist: ", bottom)
        if bottom < min and grid[y+1][x] != 1:
            min = bottom
            nextX = x
            nextY = y + 1
    # Test diagonal directions
    # Top Left
    if y > 0 and x > 0:
        topL = distance(x-1, y - 1, end[1], end[0])
        print("TopLeft from ", x, y, " to ", x-1, y - 1, " dist: ", topL)
        if topL < min and grid[y-1][x-1] != 1:
            min = topL
            nextX = x-1
            nextY = y - 1
    # Top Right
    if y > 0 and x < len(grid[0]) - 1:
        topR = distance(x + 1, y-1, end[1], end[0])
        print("TopRight from ", x, y, " to ", x + 1, y-1, " dist: ", topR)
        if topR < min and grid[y-1][x+1] != 1:
            min = topR
            nextX = x + 1
            nextY = y-1
    # Bottom Right
    if y < len(grid) - 1 and x < len(grid[0]) - 1:
        bottomR = distance(x + 1, y+1, end[1], end[0])
        print("BottomRight from ", x, y, " to ", x + 1, y+1, " dist: ", bottomR)
        if bottomR < min and grid[y+1][x+1] != 1:
            min = bottomR
            nextX = x + 1
            nextY = y+1
    # Bottom Left
    if y < len(grid) - 1 and x > 0:
        bottomL = distance(x-1, y + 1, end[1], end[0])
        print("BottomLeft from ", x, y, " to ", x-1, y + 1, " dist: ", bottomL)
        if bottomL < min and grid[y+1][x-1] != 1:
            min = bottomL
            nextX = x-1
            nextY = y + 1

    # Prints coordinates of next step
    print("Next coords", nextX, nextY)

    # Draws rectangle and calls recursively if not at the end (2)
    if grid[nextY][nextX] != 2:
        app.mkRect(nextX, nextY, "#"+str(app.plsCurrentColor()))
        pather(nextX, nextY)


# Class for GUI Window
class Window(Frame):
    # Stores the canvas
    canvas: Canvas = None
    # Width of canvas
    canvas_width = 600
    # Height of cancas
    canvas_height = 600
    # Color of current square
    currentColor = 476042
    # Weather currentColor is incrementing of decrementing
    upColor = True
    # Coordinates in pixels of last click on canvas
    x0, y0 = 0, 0

    # initializes window and calls make_widgets
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        Window.make_widgets(self, master)

    # Returns currentColor
    def getCurrentColor(self):
        return self.currentColor

    # Increments and returns currentColor (in a loop so it does not over or under flow)
    # Results in squares gradually changing colors
    def plsCurrentColor(self):
        colorChange = 5
        if self.currentColor+colorChange < 900000 and self.upColor:
            self.currentColor = self.currentColor+colorChange
        if self.currentColor - colorChange > 100000 and not self.upColor:
            self.currentColor = self.currentColor - colorChange
        else:
            self.upColor = not self.upColor
        return self.currentColor

    # Calls the pather method starting at the starting point on the grid
    def startPath(self):
        pather(start[0], start[1])

    # Clears drawing and paths from canvas, reset to startup
    def resetCanvas(self):
        self.currentColor = 476042
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                grid[i][j] = 0
        grid[start[0]][start[1]] = 1
        grid[end[0]][end[1]] = 2
        self.canvas.delete("all")
        self.repaintCanvas()

    # Fills in a given grid square with a given color and marks that square as checked in grid
    def mkRect(self, indexX: int, indexY: int, color: str):
        print("rectMake")
        self.canvas.create_rectangle(indexX * self.canvas_width / len(grid[0]),
                                     indexY * self.canvas_height / len(grid),
                                     (indexX + 1) * self.canvas_width / len(grid[0]),
                                     (indexY + 1) * self.canvas_height / len(grid),
                                     fill=color)
        grid[indexY][indexX] = 1
        for i in range(len(grid)):
            print()
            for j in range(len(grid[0])):
                sys.stdout.write(str(grid[i][j]) + " ")

    # Stores the coordinates of the click
    def click(self, event):
        print("click")
        self.x0 = event.x
        self.y0 = event.y

    # Draws a grey barrier from the precious click to the current location of the mouse
    # The path must go around these barriers
    def unClick(self, event):
        print("unclicik")
        m: float = 0
        linePoints = []
        # if possible, calculate the slope of the line connecting the previous click to the current mouse
        if abs(event.x-self.x0) > 5:
            self.canvas.create_line(self.x0, self.y0, event.x, event.y, fill="red", width=int(4))
            m = (event.y - self.y0) / (event.x - self.x0)
        # if possible, add the points on the line to the linePoints list
        if event.x+5 < self.x0:
            for xc in range(event.x, self.x0, 2):
                yc = m * (xc - event.x) + event.y
                linePoints.insert(len(linePoints) - 1, Point(xc, yc))
        elif event.x > self.x0+5:
            for xc in range(self.x0, event.x, 2):
                yc = m * (xc - self.x0) + self.y0
                linePoints.insert(len(linePoints) - 1, Point(xc, yc))
        # allows for a single square to be drawn at a single click
        else:
            linePoints.insert(len(linePoints) - 1, Point(event.x, event.y))

        # For each point in linePoints, find the corresponding grid square and fill it in grey
        for coord in range(len(linePoints)):
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    xDiff = Point(j * self.canvas_width / len(grid[0]), (j + 1) * self.canvas_width / len(grid[0]))
                    yDiff = Point(i * self.canvas_height / len(grid), (i + 1) * self.canvas_height / len(grid))
                    if xDiff.y >= linePoints[coord].x >= xDiff.x:
                        if yDiff.y >= linePoints[coord].y >= yDiff.x:
                            self.mkRect(j, i, "grey")

    # Draws grid lines and start and end squares
    def repaintCanvas(self):
        # Draws Vertical lines
        for i in range(len(grid[0])):
            x = int(self.canvas_width * i / len(grid[0]))
            self.canvas.create_line(x, 0, x, self.canvas_height, fill="#476042")
        # Draws Horizontal lines
        for i in range(len(grid)):
            y = int(self.canvas_height * i / len(grid))
            self.canvas.create_line(0, y, self.canvas_width, y, fill="#476042")
        # Start and end squares
        self.canvas.create_rectangle(start[1] * self.canvas_width / len(grid),
                                     start[0] * self.canvas_height / len(grid[0]),
                                     (start[1] + 1) * self.canvas_width / len(grid),
                                     (start[0] + 1) * self.canvas_height / len(grid[0]),
                                     fill="#476042")
        self.canvas.create_rectangle(end[1] * self.canvas_width / len(grid),
                                     end[0] * self.canvas_height / len(grid[0]),
                                     (end[1] + 1) * self.canvas_width / len(grid),
                                     (end[0] + 1) * self.canvas_height / len(grid[0]),
                                     fill="#176785")
        
    # Puts the buttons and canvas onto the window
    def make_widgets(self, master):
        pathBtn = Button(text="Path", fg="red", command=self.startPath)
        pathBtn.pack()
        resetBtn = Button(text="Reset", fg="red", command=self.resetCanvas)
        resetBtn.pack(side=TOP)
        self.canvas = Canvas(master,
                             width=self.canvas_width,
                             height=self.canvas_height)
        self.canvas.bind("<ButtonPress-1>", self.click)
        self.canvas.bind("<ButtonRelease-1>", self.unClick)
        self.canvas.pack()
        self.repaintCanvas()


# Creates the window
root = Tk()
root.title("Simple Pathfinder")
app = Window(root)

root.mainloop()
