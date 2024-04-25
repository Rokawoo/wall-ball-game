"""
Purpose: This code defines a `Boundary` class for a Pygame application.
The boundary is a drawable object representing a rectangular area with specified position, size, and color.

Author: Roka
Date: May 7, 2023
"""

import pygame
from Drawable import Drawable

class Boundary(Drawable):
    def __init__(self, y = 0, width = 800, height = 10, color = (255, 0, 0)):
        surface = pygame.display.get_surface()
        screenWidth, screenHeight = surface.get_size()
        super().__init__(0, screenHeight - height)
        self.__color = color
        self.__width = width
        self.__height = height

    def draw(self, surface):
        if self.is_visible():
            surface = pygame.display.get_surface()
            screenWidth, screenHeight = surface.get_size()
            pygame.draw.rect(surface, self.__color, self.get_rect())
        
    def get_rect(self):
        surface = pygame.display.get_surface()
        screenWidth, screenHeight = surface.get_size()
        y = self.get_loc()[1]
        return pygame.Rect(0, y, self.__width, self.__height)

    def get_y(self):
        return self.get_loc()[1]

    def set_y(self, newY):
        self.set_y(newY)

