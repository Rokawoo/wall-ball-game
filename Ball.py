"""
Purpose: This code defines a `Ball` class for a Pygame application, extending the `Drawable` class.
The `Ball` represents a drawable circular object with specific attributes for position, radius, color, and movement. It includes methods for drawing, moving, and boundary detection.

Author: Roka
Date: May 7, 2023
"""


import pygame
from Drawable import Drawable

class Ball(Drawable):
    def __init__(self, x = 0, y = 0, radius = 10, color = (255, 255, 255)):
        super().__init__(x, y)
        self.__radius = radius
        self.__color = color
        self.__speedX = 10
        self.__speedY = 10

    def draw(self, surface):
        if self.is_visible():
            pygame.draw.circle(surface, self.__color, self.get_loc(), self.__radius)

    def get_rect(self):
        currentX, currentY = self.get_loc()
        radius = self.__radius
        
        left = currentX - radius
        top = currentY - radius
        width = self.__radius * 2
        height = self.__radius * 2
        
        rect = pygame.Rect(left, top, width, height)
        return rect
    
    def move(self):
        currentX, currentY = self.get_loc()
        newX = currentX + self.__speedX
        newY = currentY + self.__speedY
        self.set_x(newX)
        self.set_y(newY)
        
        surface = pygame.display.get_surface()
        width, height = surface.get_size()
        
        if newX <= self.__radius or newX + self.__radius >= width:
            self.__speedX *= -1
            
        if newY <= self.__radius or newY + self.__radius >= height:
            self.__speedY *= -1
            
    def get_speedX(self):
        return self.__speedX
            
    def set_speedX(self, speed):
        self.__speedX = speed
 
    def get_speedY(self):
        return self.__speedY
    
    def set_speedY(self, speed):
        self.__speedY = speed
    
    def get_color(self):
        return self.__color
    
    def set_color(self, color):
        self.__color = color
        
    def isTouchingBall(self, other):
        pass
        