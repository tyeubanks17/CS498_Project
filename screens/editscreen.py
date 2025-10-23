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

class TermWidget(GridLayout):
    '''
    Widget that will contain term & definition
    text fields, as well as other entry manipulation
    controls
    '''
    # idStr = StringProperty(None)
    pass
    # def __init__(self, idStr=None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if not self.id: 
    #         if not idStr: 
    #             raise ValueError("Must instantiate TermWidget with id!")
    #         self.id = idStr

class EditScreen(Screen):
    Builder.load_file("./screens/editscreen.kv")
    terms = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add initial term objects on load
        self.terms.append(TermWidget())
        self.terms.append(TermWidget())
        self.terms.append(TermWidget())
        for tw in self.terms: 
            self.ids['termlayout'].add_widget(tw)

    def on_pre_enter(self):
        # To execute on screen load
        pass