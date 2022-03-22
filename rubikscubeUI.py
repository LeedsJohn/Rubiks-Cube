# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 15:32:57 2021

@author: John Leeds

Special thanks to John Zelle for graphics.py

This file contains the code to handle most of the UI processes such as 
the menu sequences and drawing and updating the Rubik's Cube.
"""
from graphics import * # Written by John Zelle
from rubikscube import *
from button import * # Code inspired by button.py written in class by Professor Janet Davis
from time import sleep

class Menu:
    """
    This class handles the menu sequences.
    """
    def __init__(self):
        self.win = GraphWin("Menu", 1280, 720)
    
    def mainMenu(self):
        """
        Goes through the main menu sequence and gets the user to click a button
        """
        background = Image(Point(640, 360), "main menu.png")
        background.draw(self.win)
        
        solvePic = Image(Point(400, 450), "solve button.png")
        solveButton = Button(solvePic)
        solveButton.display(self.win)
        
        practicePic = Image(Point(880, 450), "practice button.png")
        practiceButton = Button(practicePic)
        practiceButton.display(self.win)
        
        while True:
            click = self.win.getMouse()
            if solveButton.isClicked(click):
                background.undraw()
                solveButton.hide()
                practiceButton.hide()
                self.win.close()
                return "full solve"
            if practiceButton.isClicked(click):
                background.undraw()
                solveButton.hide()
                practiceButton.hide()
                return self.practiceMenu()
                
    
    def practiceMenu(self):
        """
        Waits for the user to select a practice mode
        """
        background = Image(Point(640, 360), "practice menu.png")
        background.draw(self.win)
        
        buttonNames = ["cross", "bot corners", "mid edges", "orient edges",\
                       "solve edges", "orient corners", "solve corners", "free play"]
        
        height = 400
        width = 265
        buttons = []
        for i in range(8):
            if i == 4: # second row
                height = 600
                width = 265
            pic = Image(Point(width, height), buttonNames[i] + ".png")
            button = Button(pic)
            button.display(self.win)
            buttons.append(button)
            width += 250
        
        modes = ["cross", "corners", "mid edges", "orient edges", "solve edges",\
                 "orient corners", "solve corners", "free play"]
        while True:
            click = self.win.checkMouse()
            for i in range(8):
                if buttons[i].isClicked(click):
                    self.win.close()
                    return modes[i]
    
    def endScreen(self, time, moves):
        """
        Displays the end screen. Shows the move count and time.
        """
        self.win = GraphWin("End Screen", 1280, 720)
        background = Image(Point(640, 360), "end screen.png")
        background.draw(self.win)
        
        timeText = Text(Point(500, 265), time)
        moveText = Text(Point(430, 355), moves)
        timeText.setSize(36)
        moveText.setSize(36)
        timeText.setStyle("bold")
        moveText.setStyle("bold")
        
        timeText.draw(self.win)
        moveText.draw(self.win)
        
        PAPic = Image(Point(400, 550), "play again.png")
        exitPic = Image(Point(890, 550), "big exit.png")
        PAButton = Button(PAPic)
        exitButton = Button(exitPic)
        PAButton.display(self.win)
        exitButton.display(self.win)
        
        while True:
            click = self.win.getMouse()
            if exitButton.isClicked(click):
                self.win.close()
                return False
            if PAButton.isClicked(click):
                self.win.close()
                return True

def drawCube(win, width, height, sideLength):
    """
    Finds the coordinates of the corners of the right square, up square,
    and front square.

    Parameters
    ----------
    win : GraphWin
        the graph win the cube is drawn on
    width : width
        width of the window
    height : int
        height of the window
    sideLength : int
        how long the side of the cube should be

    Returns
    -------
    list
        [[rSquare coords], [uSquare coords], [fSquare coords]]
    """
    fSquare = [Point(width//2 - sideLength//2, height//2 - sideLength//2),\
               Point(width//2 + sideLength//2, height//2 - sideLength//2),\
               Point(width//2 + sideLength//2, height//2 + sideLength//2),\
               Point(width//2 - sideLength//2, height//2 + sideLength//2)]
        
    bSquare = [Point(width//2, height//2 - sideLength),\
               Point(width//2 + sideLength, height//2 - sideLength),\
               Point(width//2 + sideLength, height//2),\
               Point(width//2, height//2)]
    
    #finding the corners of the right and up faces
    rSquare = [fSquare[1], bSquare[1], bSquare[2], fSquare[2]]
    uSquare = [bSquare[0], bSquare[1], fSquare[1], fSquare[0]]
    
    return [rSquare, uSquare, fSquare]

def lineThirds(p1, p2):
    """
    Finds the point one third and two thirds through a line

    Parameters
    ----------
    p1 : Point
        starting point.
    p2 : Point
        end point.

    Returns
    -------
    list
        [one third point, two thirds point].
    """
    thirdX = int((p1.getX() * 2/3) + (p2.getX() * 1/3))
    thirdY = int((p1.getY() * 2/3) + (p2.getY() * 1/3))

    twoThirdX = int((p1.getX() * 1/3) + (p2.getX() * 2/3))
    twoThirdY = int((p1.getY() * 1/3) + (p2.getY() * 2/3))
    
    return [Point(thirdX, thirdY), Point(twoThirdX, twoThirdY)]

def findPolygonPoints(p0, p1, p2, p3):
    """
    Finds the points needed to make the 3x3 grid within each square

    Parameters
    ----------
    p0-p4 : Point
        the points of the outer square starting at the top left and rotating
        clockwise

    Returns
    -------
    polygonPoints : list
        a list of the points needed to make the 3x3 grid within the larger squares
    """
    cases = [[p0, p1]] # form a list of all the vertices
    thirdCases1 = lineThirds(p0, p3)
    thirdCases2 = lineThirds(p1, p2)
    cases.append([thirdCases1[0], thirdCases2[0]])
    cases.append([thirdCases1[1], thirdCases2[1]])
    cases.append([p3, p2])
    
    polygonPoints = []
    for case in cases:
        level = []
        level.append(case[0])
        thirds = lineThirds(case[0], case[1])
        level.append(thirds[0])
        level.append(thirds[1])
        level.append(case[1])
        
        polygonPoints.append(level)
    
    return polygonPoints

def createPolygons(polygonPoints):
    """
    Creates the polygons that represent the 3x3 grid of squares
    the top row squares are squares 0-2, the middle row is 3-5, bottom = 6-8

    Parameters
    ----------
    polygonPoints : list
        the points to create the squares from

    Returns
    -------
    polygons : list
        the 3x3 grid of squares
    """
    polygons = []
    for vertical in range(3):
        for horizontal in range(3):
            p0 = polygonPoints[vertical][horizontal]
            p1 = polygonPoints[vertical][horizontal + 1]
            p2 = polygonPoints[vertical + 1][horizontal + 1]
            p3 = polygonPoints[vertical + 1][horizontal]
            polygons.append(Polygon(p0, p1, p2, p3))
    
    return polygons
        
def fullPolygons(r, u, f):
    """
    Calls create polygons on every visible side

    Parameters
    ----------
    r, u, and f are lists representing the polygonPoints on each side

    Returns
    -------
    polygons : list
        3x3 grid of squares
    """
    polygons = []
    for face in [r, u, f]:
        polygonPoints = findPolygonPoints(face[0], face[1], face[2], face[3])
        facePolygons = createPolygons(polygonPoints)
        polygons.append(facePolygons)
    return polygons

def undrawCube(polygons):
    """
    Undraws the cube so it can be updated

    Parameters
    ----------
    polygons : list
        list of polygons

    Returns
    -------
    None.
    """
    for face in range(3):
        for square in polygons[face]:
            square.undraw()    

def updateCube(win, polygons, cube):
    """
    Updates the Rubik's Cube to represent it's current state

    Parameters
    ----------
    win : GraphWin
        the window to draw it on
    polygons : list
        list of polygons
    cube : RubiksCube
        the Rubik's Cube

    Returns
    -------
    None.
    """
    undrawCube(polygons)
    colors = {"y": "yellow", "o": "orange", "g": "green", "r": "red", \
          "b": "blue", "w": "white", "gr": "gray"}
    
    edges = cube.getEdges()
    corners = cube.getCorners()
    centers = cube.getCenters()
    
    startIndexes = [16, 0, 4]
    for index in range(3):
        face = polygons[index]
        #drawing corners
        count = 0
        for corner in [0, 2, 8, 6]:
            color = colors[corners[startIndexes[index] + count]]
            face[corner].setFill(color)
            face[corner].draw(win)
            count += 1
        #drawing edges
        count = 0
        for edge in [1, 5, 7, 3]:
            color = colors[edges[startIndexes[index] + count]]
            face[edge].setFill(color)
            face[edge].draw(win)
            count += 1
        #drawing centers
        if index == 0:
            color = colors[centers[4]]
        elif index == 1:
            color = colors[centers[0]]
        else:
            color = colors[centers[1]]
        face[4].setFill(color)
        face[4].draw(win)

def showSolve(win, polygons, cube, lastStep = None):
    """
    This function shows the steps taken to solve a Rubik's Cube
    """
    copyCube = cube.copyCube()
    currentIndex = len(cube.getMoves())
    cube.solve(lastStep)
    solution = cube.getMoves()
    solution = solution[currentIndex:]
    betterSolution = cube.formatMoves(solution).split()
    betterSolutionInput = ""
    for move in betterSolution:
        betterSolutionInput += cube.moveToRaw(move)
        
    updateCube(win, polygons, copyCube)
    for move in betterSolutionInput:
        copyCube.rotate(move)
        updateCube(win, polygons, copyCube)
        sleep(0.075)

def convertWord(word):
    """
    Converts inputs stored as words to what their actual input is
    ex: "comma" --> ","
    This function should not be necessary, originally storing them as words
    is dumb D:

    Parameters
    ----------
    word : str
        word to convert

    Returns
    -------
    letter : str
        letter representing the word
    """
    words = ["comma", "period", "semicolon", "slash", "space"]
    characters = [",", ".", ";", "/", " "]
    if word in words:
        letter = characters[words.index(word)]
        return letter

def setUp():
    """
    Generates a Rubik's Cube and the UI
    """
    width = 1280
    height = 720
    win = GraphWin("Rubik's Cube", width, height)
    sideLength = 300
    
    #menuSequence(win)
    # source: wallpaperaccess.com/1280-x-720-cool
    background = Image(Point(640, 360), "background.png")
    background.draw(win)
    coordinates = drawCube(win, width, height, sideLength)
    polygons = fullPolygons(coordinates[0], coordinates[1], coordinates[2])
    return [win, polygons]
    