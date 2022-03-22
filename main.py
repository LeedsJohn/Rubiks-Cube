#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 13:56:54 2021

@author: John Leeds

Special thanks to John Zelle for graphics.py

Background image source:
wallpaperaccess.com/1280-x-720-cool

This files runs the game repeatedly until exited.
"""
from games import *
from rubikscubeUI import Menu
 
def main():
    
    flag = True
    while flag:
        menu = Menu()
        mode = menu.mainMenu()
        game = Play(mode)
        stats = game.play()
        if stats != False: # exit button not clicked
            flag = menu.endScreen(stats[0], stats[1])
        else:
            break

if __name__ == "__main__":
    main()