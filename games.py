#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 14:03:38 2021

@author: John Leeds

Special thanks to John Zelle for graphics.py

This file contains the code to play with a Rubik's cube.
The CubeSetup class contains the information to put a Rubik's Cube in different
starting position.
The Play class brings the user through the sequence of playing a round.
"""
from rubikscube import *
import cubesolver
from rubikscubeUI import setUp, updateCube, showSolve, convertWord
from graphics import Image, Point # Written by John Zelle
from time import time
from button import Button # Inspired by code written in class by Professor Janet Davis

class CubeSetup:
    """
    This class handles setting up the Rubik's Cube for the different
    game modes."""
    def __init__(self, rCube):
        """
        rCube : the Rubik's Cube to set up
        """
        self.rCube = rCube
    
    def getrCube(self):
        return self.rCube
    
    def scrambled(self):
        """
        Scramble the Rubik's Cube
        """
        self.rCube.scramble()
    
    def cross(self, scramble = True):
        """
        Gray out all pieces except ones to solve the cross
        """
        for i in range(24):
            if i not in [6, 10, 14, 18, 20, 21, 22, 23]:
                self.rCube.edges[i] = "gr"
            self.rCube.corners[i] = "gr"
        if scramble:
            self.rCube.scramble()
            self.rCube.solve(0)
    
    def corners(self, scramble = True):
        """
        Gray out all pieces except the ones to solve the bottom corners
        """
        solved = self.rCube.copyCube()
        self.cross(False)
        for i in range(6, 24):
            if (i + 1) % 4 == 0 or (i + 2) % 4 == 0 or i in [20, 21]:
                self.rCube.corners[i] = solved.corners[i]
        if scramble:
            self.rCube.scramble()
            self.rCube.solve(1)
    
    def midEdges(self, scramble = True):
        """
        Gray out all pieces except the ones to solve the middle edges
        """
        solved = self.rCube.copyCube()
        self.corners(False)
        for i in range(5, 20, 2):
            self.rCube.edges[i] = solved.edges[i]
        if scramble:
            self.rCube.scramble()
            self.rCube.solve(2)
    
    def orientEdges(self, scramble = True):
        """
        Gray out all pieces except the ones involved in orienting the top edges
        """
        self.midEdges(False)
        for i in range(0, 4):
            self.rCube.edges[i] = "y"
        if scramble:
            # make sure the user isn't given a solved state
            while self.rCube.checkOrientEdges():
                self.rCube.scramble()
                self.rCube.solve(3)
                
    def solveEdges(self, scramble = True):
        """
        Gray out the top corners
        """
        solved = self.rCube.copyCube()
        self.orientEdges(False)
        for i in range(4, 17, 4):
            self.rCube.edges[i] = solved.edges[i]
        if scramble:
            while self.rCube.checkSolveEdges():
                self.rCube.scramble()
                self.rCube.solve(4)
    
    def orientCorners(self, scramble = True):
        """
        Gray out the non yellow stickers on the yellow corners
        """
        self.solveEdges(False)
        for i in range(0, 4):
            self.rCube.corners[i] = "y"
        if scramble:
            while self.rCube.checkOrientCorners():
                self.rCube.scramble()
                self.rCube.solve(5)
    
    def solveCorners(self):
        """
        Give the user a random permutation of the corners to solve
        """
        while True:
            self.rCube.scramble()
            self.rCube.solve(6)
            for c in range(4): # make sure cube isn't solved
                if self.rCube.checkSolved():
                    break
                if c == 3:
                    return
                self.rCube.rotate("k")
            
class Play():
    """
    Play a round of the Rubik's Cube
    """
    def __init__(self, mode):
        attributes = setUp()
        self.mode = mode
        self.rCube = RubiksCube()
        self.win = attributes[0]
        self.polygons = attributes[1]
    
    def play(self):
        """
        Sequence in which the selected gamemode is executed.
        """
        # set up buttons
        exitPic = Image(Point(1180, 670), "exit.png")
        exitButton = Button(exitPic)
        exitButton.display(self.win)
        
        giveUpPic = Image(Point(650, 630), "give up.png")
        GUButton = Button(giveUpPic)
        GUButton.display(self.win)
        
        setUp = CubeSetup(self.rCube)
        # gamemodes: {"name": [how to set up, win condition, last step to solve]}
        gamemodes = {"free play": [setUp.getrCube, False, None],\
                     "full solve": [setUp.scrambled, self.rCube.checkSolved, None],\
                     "cross": [setUp.cross, self.rCube.checkCross, 1],\
                     "corners": [setUp.corners, self.rCube.checkBotCorners, 2],\
                     "mid edges": [setUp.midEdges, self.rCube.checkMidEdges, 3],\
                     "orient edges": [setUp.orientEdges, self.rCube.checkOrientEdges, 4],\
                     "solve edges": [setUp.solveEdges, self.rCube.checkSolveEdges, 5],\
                     "orient corners": [setUp.orientCorners, self.rCube.checkOrientCorners, 6],\
                     "solve corners": [setUp.solveCorners, self.rCube.checkSolved, 7]}
            
        gamemodes[self.mode][0]()
        self.rCube.moves = ""
        updateCube(self.win, self.polygons, self.rCube)
        startFlag = False
        while self.mode == "free play" or not gamemodes[self.mode][1]():
            move = self.win.checkKey()
            click = self.win.checkMouse()
            if move in ["comma", "period", "semicolon", "slash", "space"]:
                move = convertWord(move)
                
            if move in "asdfghjkl;zxcvbnm,./qpty" and move != "": # valid move
                if not startFlag: # start stopwatch
                    startTime = time()
                    startFlag = True
                self.rCube.rotate(move)
                updateCube(self.win, self.polygons, self.rCube)
            elif exitButton.isClicked(click):
                self.win.close()
                return False
            elif GUButton.isClicked(click):
                if not startFlag: # start stopwatch
                    startTime = time()
                    startFlag = True
                showSolve(self.win, self.polygons, self.rCube, gamemodes[self.mode][2])
            
        endTime = time()
        solveTime = endTime - startTime
        self.win.close()
        solveString = "{}:{}".format(int(solveTime//60), round(solveTime%60, 2))
        # throw on 0s when necessary
        if solveTime < 600:
            solveString = "0" + solveString
        if solveTime%60 < 10:
            solveString = solveString[:3] + "0" + solveString[3:]
        return [solveString, str(self.rCube.countMoves())]          