"""
Purpose: This code defines an abstract base class for drawable objects in a Pygame application. 
It provides common methods and attributes for drawing and manipulating these objects.

Author: Roka
Date: May 7, 2023
"""

import pygame
from abc import ABC, abstractmethod

class Drawable(ABC):
    def __init__(self, x = 0, y = 0, visible = True):
        # Initialize private variable for x, y coordinate
        self.__x = x
        self.__y = y
        self.__visible = visible
    
    @abstractmethod
    def draw(self, surface):
        pass
    
    @abstractmethod
    def get_rect(self):
        pass
    
    def get_loc(self):
        return (self.__x, self.__y)
    
    def set_loc(self, location):
        self.__x = location[0]
        self.__y = location[1]
        
    def set_x(self, x):
        self.__x = x
        
    def set_y(self, y):
        self.__y = y
        
    def is_visible(self):
        return self.__visible
    
    def set_visible(self, visible):
        if visible == True:
            self.__visible = True
        else:
            self.__visible = False
            
    def intersects(self, other):
        rect1 = self.get_rect()
        rect2 = other.get_rect()
        if (rect1.x < rect2.x + rect2.width) and (rect1.x + rect1.width > rect2.x) and\
        (rect1.y < rect2.y + rect2.height) and (rect1.height + rect1.y > rect2.y):
            return True
        else:
            return False 
        
        
    