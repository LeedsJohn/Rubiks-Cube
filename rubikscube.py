# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 09:12:02 2021

@author: John Leeds

This file contains a class to represent a Rubik's Cube
"""
import random
from cubesolver import *

class RubiksCube:
    """
    This class represents a Rubik's Cube. just trust me.
    """
    def __init__(self, edges = None, corners = None, centers = None):
        """
        Creates a solved Rubik's Cube
        edges and corners: numbered 0-23. Each side rotates through clockwise
        centers: numbered 0-5
        rotate through sides in this order:
            u --> f --> l --> b --> r --> d
        moves: a string representing the moves applied to the cube
        """
        if edges == None and corners == None and centers == None:
            edges = []
            corners = []
            centers = []
            colors = ["y", "o", "g", "r", "b", "w"]
            for color in range(6):
                centers.append(colors[color])
                for edge in range(4):
                    edges.append(colors[color])
                    corners.append(colors[color])
        
        self.edges = edges
        self.corners = corners
        self.centers = centers
        self.moves = ""
    
    
    
    """
    Controls:
        r: j
        u: k
        f: l
        l: f
        d: d
        b: s
        
        r': m
        u': ,
        f': .
        l': v
        d': c
        b': x
        
        m: ;
        e: a
        s: p
        
        m': /
        e': z
        s': q
        
        y: h
        x: n
        z: y
        
        y': g
        x': b
        z': t
    """
    
    rotationPatterns = {"j": [[1, 15, 21, 5], [2, 12, 22, 6]],\
                        "k": [[4, 8, 12, 16], [5, 9, 13, 17]],\
                        "l": [[2, 19, 20, 9], [3, 16, 21, 10]],\
                        "f": [[3, 7, 23, 13], [0, 4, 20, 14]],\
                        "d": [[6, 18, 14, 10], [7, 19, 15, 11]],\
                        "s": [[0, 11, 22, 17], [1, 8, 23, 18]],\
                        ";": [[0, 4, 20, 14], [2, 6, 22, 12], [0, 1, 5, 3]],\
                        "a": [[5, 17, 13, 9], [7, 19, 15, 11], [1, 4, 3, 2]],\
                        "p": [[1, 18, 23, 8], [3, 16, 21, 10], [0, 4, 5, 2]]}
    
    def getEdges(self):
        return self.edges
    def getCorners(self):
        return self.corners
    def getCenters(self):
        return self.centers
    def getMoves(self):
        return self.moves
    
    def setEdges(self, new):
        self.edges = new
    def setCorners(self, new):
        self.corners = new
    def setCenters(self, new):
        self.centers = new
    def setMoves(self, moves):
        self.moves = moves
    
    def copyCube(self):
        """
        Creates a copy of the Rubik's Cube
        """
        return RubiksCube(self.edges.copy(), self.corners.copy(), self.centers.copy())
        """return RubiksCube(self.getEdges.copy(), self.getCorners().copy(), \
                          self.getCenters().copy())"""
    
    def formatMoves(self, moves = None):
        # OPTIMIZE
        """
        Takes the raw input and turns it into a traditional format.
        """
        controls = {"j": "R", "k": "U", "l": "F", "f": "L", "d": "D", "s": "B",\
                ";": "M", "a": "E", "p": "S", "kdddaaa": "y", "j;;;fff": "x", "lsssp": "z"}
        # get moves, but do not adjust for counterclockwise / double moves
        semiFormatted = ""
        if moves == None:
            oldMoves = self.moves
        else:
            oldMoves = moves
        while len(oldMoves) > 0:
            # cube rotations
            if len(oldMoves) >= 7 and oldMoves[0:7] in controls:
                semiFormatted += controls[oldMoves[0:7]]
                oldMoves = oldMoves[7:]
            elif len(oldMoves) >= 5 and oldMoves[0:5] == "lsssp":
                semiFormatted += controls[oldMoves[0:5]]
                oldMoves = oldMoves [5:]
            else:
                semiFormatted += controls[oldMoves[0]]
                oldMoves = oldMoves[1:]
                
        
        formatted = []
        while len(semiFormatted) > 0:
            if len(semiFormatted) >= 3 and\
               semiFormatted[0] == semiFormatted[1] and\
               semiFormatted[0] == semiFormatted[2]:
                   
                formatted.append(semiFormatted[0] + "'")
                semiFormatted = semiFormatted[3:]
            elif len(semiFormatted) >= 2 and semiFormatted[0] == semiFormatted[1]:
                formatted.append(semiFormatted[0] + "2")
                semiFormatted = semiFormatted[2:]
            else:
                formatted.append(semiFormatted[0])
                semiFormatted = semiFormatted[1:]
        
        # fixing redundancies
        formatList = list(formatted)
        temp = []
        count = 0
        for i in range(len(formatList)):
            if len(formatList[i]) == 1:
                count += 1
            elif formatList[i][1] == "2":
                count += 2
            else:
                count += 3
    
            if i != len(formatList) - 1 and formatList[i][0] != formatList[i + 1][0]:
                temp.append([formatList[i][0], count])
                count = 0
        # add last move
        temp.append([formatList[-1][0], count])
        
        # fix for when a move is applied more than one time in a row
        formatted = ""
        for move in temp:
            if move[1]%4 == 1:
                formatted += move[0] + " "
            elif move[1]%4 == 2:
                formatted += move[0] + "2 "
            if move[1]%4 == 3:
                formatted += move[0] + "' "

        return formatted
    
    def moveToRaw(self, move):
        """
        Opposite of formatMoves - converts R U R' U' format to keyboard inputs
        """
        """
        Original code used to create the dictionary:
        moves = ["R", "U", "F", "L", "D", "B", "R'", "U'", "F'", "L'", "D'", "B'",\
                 "M", "E", "S", "x", "y", "z", "M'", "E'", "S'", "x'", "y'", "z'"]
        inputs = "jklfdsm,.vcx;apnhy/zqbgt"
        trans = {}
        for i in range(len(moves)):
            trans[moves[i]] = inputs[i]"""
            
        trans = {'R': 'j', 'U': 'k', 'F': 'l', 'L': 'f', 'D': 'd', \
                 'B': 's', "R'": 'm', "U'": ',', "F'": '.', "L'": 'v', \
                 "D'": 'c', "B'": 'x', 'M': ';', 'E': 'a', 'S': 'p', \
                 'x': 'n', 'y': 'h', 'z': 'y', "M'": '/', "E'": 'z', \
                 "S'": 'q', "x'": 'b', "y'": 'g', "z'": 't'}
        if move in trans:
            return trans[move]
        # double moves
        return trans[move[0]]*2
        
    def countMoves(self):
        """
        Counts the number of moves applied to the Rubik's Cube
        One rotation of an outside or inside face = one move (regardless of
        if it is 90 or 180 degrees)
        """
        moves = self.formatMoves(self.moves)
        count = 0
        for move in moves:
            if move in "RUFLDBMES":
                count += 1
        return count
    
    def wrapAround(self, piece, swaps):
        """
        Updates the piece after a move

        Parameters
        ----------
        piece : list
            represents the stickers to swap
        swaps : list
            the order to swap stuff

        Returns
        -------
        None.
        """
        pieceCopy = piece.copy()
        for i in range(4):
            if i == 0:
                piece[swaps[0]] = pieceCopy[swaps[-1]]
            else:
                piece[swaps[i]] = pieceCopy[swaps[i-1]]
    
    def rotate(self, rotation, patterns = rotationPatterns):
        """
        Performs a rotation to the Rubik's Cube
        Counterclockwise moves are achieved by rotating clockwise x 3
        Whole cube rotations are achieved by rotating the two faces and slice
        """
        translations = {"x": "s", "c": "d", "v": "f",\
                "m": "j", ",": "k", ".": "l",\
                "/": ";", "z": "a", "q": "p",\
                "g": "h", "b": "n", "t": "y"}
        if rotation in "asdfghjkl;zxcvbnm,./qpty" and rotation != "": # valid moves
            if rotation not in translations and rotation not in "yhntgb": 
                # do not overcount counterclockwise moves, rotations
                self.moves += rotation
            if rotation in "xcvm,.z/qtgb": # counter clockwise rotations
                # achieved by rotating clockwise 3 times
                
                for count in range(3):
                    self.rotate(translations[rotation])
                    
            elif rotation in "sdfjkl": # clockwise rotations
                order = ["k", "l", "f", "s", "j", "d"] # used to find what face is being moved
                startIndex = order.index(rotation) * 4
                facePattern = range(startIndex, startIndex + 4)
                # stickers on the rotating face
                self.wrapAround(self.edges, facePattern)
                self.wrapAround(self.corners, facePattern)
                # stickers on the sides
                self.wrapAround(self.edges, patterns[rotation][0])
                self.wrapAround(self.corners, patterns[rotation][0])
                self.wrapAround(self.corners, patterns[rotation][1])
            
            elif rotation in "a;p": # slice moves
                self.wrapAround(self.edges, patterns[rotation][0])
                self.wrapAround(self.edges, patterns[rotation][1])
                self.wrapAround(self.centers, patterns[rotation][2])
                
            elif rotation in "hny": # cube rotations
                if rotation == "h":
                    self.rotate("k")
                    self.rotate("c")
                    self.rotate("z")
                elif rotation == "n":
                    self.rotate("j")
                    self.rotate("/")
                    self.rotate("v")
                elif rotation == "y":
                    self.rotate("l")
                    self.rotate("x")
                    self.rotate("p")
    
    def moveString(self, moves):
        """
        Performs multiple rotations
        """
        for move in moves:
            self.rotate(move)
    
    def scramble(self):
        """
        Scrambles the Rubik's Cube by applying 100 random moves
        """
        possibilities = "asdfzxcvjkl;m,./pq"
        for move in range(100): # 100 random twists
            moveIndex = random.randrange(0, len(possibilities))
            self.rotate(possibilities[moveIndex])
    
    def solve(self, lastStep = None):
        """
        Uses a CubeSolver to find a solution to itself
        """
        solver = CubeSolver(self)
        solver.solve(lastStep)
        
    def checkCross(self):
        """
        Checks to see if the white cross is solved
        """
        cubeCopy = self.copyCube()
        if cubeCopy.edges[20:24] == ["w", "w", "w", "w"]:
            for i in range(4):
                cubeCopy.rotate("h")
                if cubeCopy.edges[6] != cubeCopy.centers[1]:
                    return False # incorrectly positioned
            return True
        return False # not all white edges on bottom
    
    def checkBotCorners(self):
        """
        Checks to see if the bottom corners are solved
        """
        cubeCopy = self.copyCube()
        if cubeCopy.corners[20:24] == ["w", "w", "w", "w"] and self.checkCross():
            for side in range(4):
                cubeCopy.rotate("h")
                if (cubeCopy.corners[6] != cubeCopy.centers[1]) or\
                   (cubeCopy.corners[7] != cubeCopy.centers[1]):
                    return False # incorrectly positioned
            return True
        return False # not all white on bottom
        
    def checkMidEdges(self):
        """
        Checks to see if the middle edges are solved
        """
        if not self.checkBotCorners():
            return False
        edges = [5, 7, 9, 11, 13, 15, 17, 19]
        centers = [1, 1, 2, 2, 3, 3, 4, 4]
        for i in range(8):
            if self.edges[edges[i]] != self.centers[centers[i]]:
                return False
        return True
    
    def checkOrientEdges(self):
        """
        Checks to see if the cube is solved up to the top edges being oriented.
        Could be written more efficiently, but this is more elegant because it
        shows each possibility of the cube not being solved.
        """
        if not self.checkMidEdges():
            return False
        if self.edges[0:4] != ["y", "y", "y", "y"]:
            return False
        return True
    
    def checkSolveEdges(self):
        
        if not self.checkOrientEdges():
            return False
        
        checkPieces = []
        for i in range(4, 17, 4):
            checkPieces.append(self.edges[i])
        # arbitrarily shift the list around until orange is first
        while checkPieces[0] != "o":
            self.wrapAround(checkPieces, [1, 2, 3, 0])
            
        if checkPieces != ["o", "g", "r", "b"]:
            return False
        return True
            
    
    def checkOrientCorners(self):
        
        if not self.checkSolveEdges():
            return False
        if self.corners[0:4] != ["y", "y", "y", "y"]:
            return False
        return True
    
    def checkSolved(self):
        """
        Checks to see if the Rubik's Cube is solved

        Returns
        -------
        bool : 
            True : the cube is solved
        """
        for index in range(6): # for each side
            color = self.centers[index]
            for sticker in range(4): # for each sticker
                if (self.edges[index * 4 + sticker] != color) or \
                    (self.corners[index * 4 + sticker] != color):
                    return False
            
        return True