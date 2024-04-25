"""
Purpose: This code defines a class for a paddle object in a Pygame application. T
he paddle is a drawable rectangular object that represents a player-controlled shape, with specified size and color.

Author: Augustus Sroka (ays36)
Date: May 7, 2023
"""



import pygame
from Drawable import Drawable

class Paddle(Drawable):
     def __init__(self, width = 10, height = 30, color = (255, 255, 255)):
         surface = pygame.display.get_surface()
         screenWidth, screenHeight = surface.get_size()
         super().__init__(screenWidth/2, screenHeight/2)
         self.__color = color
         self.__width = width
         self.__height = height

     def draw(self, surface):
         if self.is_visible():
             pygame.draw.rect(surface, self.__color, self.get_rect())

     def get_rect(self):
         surface = pygame.display.get_surface()
         screenWidth, screenHeight = surface.get_size()
         mouseX = pygame.mouse.get_pos()[0]
             
         return pygame.Rect(mouseX - self.__width/2, screenHeight - 20 - (self.__height), self.__width, self.__height)
