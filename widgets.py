'''
widgets.py
01 Nov 2025

Declarations of common Widgets
'''
import os, csv

from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ListProperty

class IconButton(ButtonBehavior, Image): 
    '''
    Image object with button properties
    Definition taken from Kivy docs: 
    https://kivy.org/doc/stable/api-kivy.uix.behaviors.html#module-kivy.uix.behaviors
    '''
    pass

class FileChooserCsv(Popup):
    '''
    File chooser for importing/deleting set files
    '''
    default_path = StringProperty(os.path.join(os.path.expanduser("~"), "Downloads"))
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.selection = None
        # Builder.load_file("./widgets.kv")

    def set_selection(self):
        self.selection = self.ids['filechooser'].selection
        self.dismiss()

    def cancel(self): 
        self.selection = None
        self.dismiss()

class CsvHeaderSelectPopup(Popup):
    '''
    Popup dialog for choosing CSV header for 
    term field
    '''
    options = ListProperty()

    def set_selection(self): 
        self.selection = self.ids['headerchoices'].text
        self.dismiss()