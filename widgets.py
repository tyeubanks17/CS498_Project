'''
widgets.py
01 Nov 2025

Declarations of common Widgets
'''
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

class IconButton(ButtonBehavior, Image): 
    '''
    Image object with button properties
    Definition taken from Kivy docs: 
    https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#module-kivy.uix.behaviors
    '''
    pass