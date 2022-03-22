#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 13:26:56 2021

@author: John Leeds

This file contains a class that can solve any Rubik's Cube.
"""
from rubikscube import *

class CubeSolver:
    """
    This class is used to solve a Rubik's Cube.
    It provides functions for each individual step.
    """
    def __init__(self, rCube):
        self.rCube = rCube
    
    def orient(self):
        """
        Rotates the cube until the white face is on the bottom
        """
        if self.rCube.centers[0] == "y":
            return
        
        for count in range(3): # step 1a
            self.rCube.rotate("y")
            if self.rCube.centers[0] == "y":
                return # oriented correctly
        for count in range(3): # step 1b
            self.rCube.rotate("n")
            if self.rCube.centers[0] == "y":
                return
    
    def prepareEdge(self):
        """
        Moves the white edges closer to being solved each time it is called
        """
        # step 2a (white on u face)
        combos = [[0, 12, "ss"], [1, 16, "jj"], [2, 4, "ll"], [3, 8, "ff"]]
        if "w" in self.rCube.edges[0:4]: # only check if there is one... more efficient
            # check for every possible u move / rotation combination
            for uMove in range(4):
                # check if piece is lined up
                for combo in combos:
                    if self.rCube.edges[combo[0]] == "w" and\
                       self.rCube.edges[combo[1]] == self.rCube.centers[combo[1]//4]:
                        self.rCube.moveString(combo[2])
                        return
                self.rCube.rotate("k")
        
        # step 2b (white on e slice)
        eSlice = []
        for i in range(5, 20, 2):
            eSlice.append(self.rCube.edges[i])
        if "w" in eSlice:
            for rotation in range(4):
                if self.rCube.edges[5] == "w":
                    self.rCube.moveString("jkm")
                    return
                if self.rCube.edges[7] == "w":
                    self.rCube.moveString("v,f")
                    return
                self.rCube.rotate("h")
        # step 2c (white edge on u face but not u sticker)
        uFace = []
        for i in range(4, 17, 4):
            uFace.append(self.rCube.edges[i])
        if "w" in uFace:
            for i in range(4):
                if self.rCube.edges[4] == "w":
                    self.rCube.moveString("j,m")
                    return
                self.rCube.rotate("k")
        # step 2d (white edge on d face but not d sticker)
        dFace = []
        for i in range(6, 19, 4):
            dFace.append(self.rCube.edges[i])
        if "w" in dFace:
            for i in range(4):
                if self.rCube.edges[6] == "w":
                    self.rCube.rotate(".")
                    return
                self.rCube.rotate("h")
        # step 2e (misplaced white edge on d face)
        for count in range(4):
            if self.rCube.edges[20] == "w" and \
               self.rCube.edges[6] != self.rCube.centers[1]:
                   self.rCube.moveString("ll")
                   return
            self.rCube.rotate("h")
            
    def solveEdges(self):
        """
        Calls prepareEdge until the cross is solved
        """
        while not self.rCube.checkCross(): # if the cross isn't solved
            self.prepareEdge()
            
    def prepareCorners(self):
        """
        Moves the white corners one step closer to being solved
        """
        # step 3a
        uFace = []
        for i in [0, 1, 2, 3, 4, 5, 8, 9, 12, 13, 16, 17]:
            uFace.append(self.rCube.corners[i])
        if "w" in uFace:
            for c in range(4): # searching for white corner
                colors = [self.rCube.corners[2], self.rCube.corners[5], self.rCube.corners[16]] # indexes of URF, FRU, RUF stickers
                if "w" in colors: # found white corner
                    for rotation in range(4):
                        #checking positioning
                        if (self.rCube.centers[1] in colors) and (self.rCube.centers[4] in colors):
                            if self.rCube.corners[2] == "w":
                                self.rCube.moveString("jjkjj,jj")
                            elif self.rCube.corners[5] == "w":
                                self.rCube.moveString(".,l")
                            else:
                                self.rCube.moveString("jkm")
                            return
                        self.rCube.moveString("h,")
                self.rCube.rotate("h")
        # step 3b - finding corners incorrectly in bottom
        for c in range(4):
            if (self.rCube.corners[6] != self.rCube.centers[1])\
               or (self.rCube.corners[19] != self.rCube.centers[4]):
                   if self.rCube.corners[6] != "w": # slight optimization - don't move white facing up
                       self.rCube.moveString("jkm") # move corner out of bottom
                   else:
                       self.rCube.moveString(".,l")
                   return
            self.rCube.rotate("h")
    
    def solveCorners(self):
        """
        Repeatedly calls prepareCorners until the white corners are solved
        """
        while not self.rCube.checkBotCorners():
            self.prepareCorners()
    
    def prepareMidEdge(self):
        """
        Moves a middle edge to its appropriate position
        If the middle edges are not solved and there are no middle edges
        on the U face, move one to the U face
        """
        # step 4a - finding middle edges on the top
        for c in range(4):
            if self.rCube.edges[2] in "gobr" and self.rCube.edges[4] in "gobr":
                # found a piece
                for rotation in range(4):
                    if self.rCube.edges[4] == self.rCube.centers[1]:
                        # if it needs to be sent to the left
                        if self.rCube.edges[2] == self.rCube.centers[2]:
                            self.rCube.moveString(",vkfkl,.")
                        else: # send to the right
                            self.rCube.moveString("kj,m,.kl")
                        return
                    self.rCube.moveString("h,")
            # check next piece
            self.rCube.rotate("k")
        
        # step 4b - remove incorrectly placed edges
        for c in range(4):
            if self.rCube.edges[5] != self.rCube.centers[1] or\
               self.rCube.edges[7] != self.rCube.centers[1]:
                # found an incorrect piece
                for rotation in range(4):
                    if self.rCube.edges[2] not in "gobr" or\
                       self.rCube.edges[4] not in "gobr":
                        if self.rCube.edges[7] != self.rCube.centers[1]: # send to left
                            self.rCube.moveString(",vkfkl,.")
                        else: # send to right
                            self.rCube.moveString("kj,m,.kl")
                        return
                    self.rCube.rotate("k")
            self.rCube.rotate("h")
    
    def solveMidEdges(self):
        """
        Repeatedly calls prepareMidEdge until the middle edges are solved
        """
        while not self.rCube.checkMidEdges():
            self.prepareMidEdge()
            
    def orientEdges(self):
        """
        Orients the top edges (all yellow edges on top)
        """
        while self.rCube.edges[0:4] != ["y", "y", "y", "y"]: # while case 1 is not true
            if "y" not in self.rCube.edges[0:4]: # Step 5b - 0 edges oriented
                self.rCube.moveString("ljkm,.kklkj,m.")
            elif self.rCube.edges[1] == "y" and self.rCube.edges[3] == "y": # step 5c - line
                self.rCube.moveString("ljkm,.")
            elif self.rCube.edges[0] == "y" and self.rCube.edges[3] == "y": # step 5d - adjacent
                self.rCube.moveString("lkj,m.")
            self.rCube.rotate("k")
    
    def solveTopEdges(self):
        """
        Positions the top edges correctly relative to each other
        """
        self.auf()
        # Step 6a - if it's already solved
        if [self.rCube.edges[4], self.rCube.edges[8], self.rCube.edges[12], self.rCube.edges[16]] ==\
              [self.rCube.centers[1], self.rCube.centers[2], self.rCube.centers[3], self.rCube.centers[4]]:
            return
        # Step 6b - if it's not solved but two edges can be correct relative to each other
        for rotation in range(4):
            if [self.rCube.edges[12], self.rCube.edges[16]] in\
               [["b", "o"], ["o", "g"], ["g", "r"], ["r", "b"]]:
                   self.rCube.moveString("jkmkjkkmk")
                   return
            self.rCube.rotate("k")
        
        # Step 6c - if this doesn't work, it is a z perm
        self.rCube.moveString(";;k;;k/kk;;kk/")
    
    def orientCorners(self):
        """
        Orient the corners (all yellow corners on top)
        """
        # Step 7a - going through the corners one by one
        for c in range(4):
            if self.rCube.corners[16] == "y":
                self.rCube.moveString("mcjdmcjd")
            elif self.rCube.corners[5] == "y":
                self.rCube.moveString("cmdjcmdj")
            self.rCube.rotate("k")
    
    def auf(self):
        """
        Corrects the top face
        """
        while self.rCube.edges[4] != self.rCube.centers[1]:
            self.rCube.rotate("k")
            
    def solveTopCorners(self):
        """
        Shuffles the top corners around - final step of solving the cube
        """
        # Step 8a - check if the cube is already solved
        self.auf()
        if self.rCube.checkSolved():
            return
        
        # Step 8b
        for c in range(4):
            self.rCube.rotate("h")
            # check if it's an A permutation
            if (self.rCube.edges[8] == self.rCube.corners[9]) and\
               (self.rCube.edges[4] == self.rCube.corners[4]):
                if self.rCube.corners[5] == self.rCube.edges[12]:
                    self.rCube.moveString("mlmssj.mssjj")
                else:
                    self.rCube.moveString("njjddjkmddj,jb")
                self.auf()
                return
        
        # check for H permutation
        if self.rCube.corners[4] == self.rCube.corners[5]:
            self.rCube.moveString("//k//kk//k//")
            self.auf()
            return
        
        # Step 8c - if this doesn't solve it, it must be an E perm
        if self.rCube.corners[4] != self.rCube.edges[8]:
            self.rCube.rotate("h")
        self.rCube.moveString("bj,mdjkmcjkmdj,mcn")
        
        self.auf()
    
    def solve(self, lastStep):
        """
        Solves a Rubik's Cube by calling each step
        """
        moves = [self.orient, self.solveEdges, self.solveCorners,\
                 self.solveMidEdges, self.orientEdges, self.solveTopEdges,\
                 self.orientCorners, self.solveTopCorners]
        # this is cool, I did not know you could put functions in a list
        for i in range(len(moves)):
            moves[i]()
            if i == lastStep:
                return