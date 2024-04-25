"""
Purpose: This code defines a class for text objects in a Pygame application. 
These text objects are drawable and represent messages displayed on the screen, each with a specified position, color, and size.

Author: Roka
Date: May 7, 2023
"""

import pygame
from Drawable import Drawable

class Text(Drawable):
    def __init__(self, message = "Wall & Ball", x = 0, y = 0, color = (255, 255, 255), size = 24):
        super().__init__(x, y)
        self.__message = message
        self.__color = color
        self.__fontObj = pygame.font.Font("freesansbold.ttf", size)

    def draw(self, surface):
        if self.is_visible():
            self.__surface = self.__fontObj.render(self.__message, True, self.__color)
            surface.blit(self.__surface, self.get_loc())

    def get_rect(self):
        return self.__surface.get_rect()

    def set_message(self, message):
        self.__message = message 
