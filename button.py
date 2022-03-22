# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 20:46:25 2021

@author: leeds
"""
from graphics import *

class Button:
    def __init__(self, picture):
        center = picture.getAnchor()
        width = picture.getWidth()
        height = picture.getHeight()
        
        self.image = picture
        self.topLeft = Point(center.getX()-width//2, center.getY()-height//2)
        self.botRight = Point(center.getX()+width//2, center.getY()+height//2)
    
    def isClicked(self, click):
        if click != None:
            x = click.getX()
            y = click.getY()
            
            lX = self.topLeft.getX()
            rX = self.botRight.getX()
            tY = self.topLeft.getY()
            bY = self.botRight.getY()
            if (lX <= x <= rX) and (tY <= y <= bY):
                return True
        return False
    
    def display(self, win):
        self.image.draw(win)
    
    def hide(self):
        self.image.undraw()