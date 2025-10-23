'''
editScreen.py

Definition for set creation/editing screen

History: 
22 Oct 2025 - Created
'''

from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

class TermWidget(BoxLayout):
    '''
    Widget that will contain term & definition
    text fields, as well as other entry manipulation
    controls
    '''
    pass

class EditScreen(Screen):
    Builder.load_file("./screens/editscreen.kv")
    terms = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add initial term objects on load
        self.terms.append(TermWidget())
        self.terms.append(TermWidget())
        for tw in self.terms: 
            self.ids['termlayout'].add_widget(tw)

    def on_pre_enter(self):
        # To execute on screen load
        # Reset screen here or on_leave?
        pass

    def add_card(self): 
        '''
        Add a blank flashcard to the editor interface
        '''
        self.terms.append(TermWidget())
        self.ids['termlayout'].add_widget(self.terms[-1])