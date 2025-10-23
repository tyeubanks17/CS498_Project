'''
editScreen.py

Definition for set creation/editing screen

History: 
22 Oct 2025 - Created
23 Oct 2025 - Add term/definition fields, tab navigation
'''

from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.lang import Builder

def find_ancestor_of_type(child, ances_type): 
    '''
    Helper method to find nearest ancestor of given type
    '''
    MAX_COUNT = 100 # Limit number of tree levels to check
    count = 0

    ancestor = child.parent
    while not isinstance(ancestor, ances_type):
        ancestor = ancestor.parent
        if count > MAX_COUNT:
            raise NameError(f"Ancestor of type {ances_type} not found")
        else: 
            count += 1
    return ancestor

class TermTextInput(TextInput):
    '''
    Custom TextInput class to allow hijacking tab
    navigation to add new card
    '''
    # on_focus = root.on_input_focus(self)
    def on_focus(self, instance, value):
        '''
        Scroll to text box when focused
        '''
        # Test whether element is visible
        left,bot = self.to_window(self.x, self.y)
        right,top = self.to_window(self.right, self.top)
        SCR_PAD = dp(20)
        if bot < 0 or top > Window.height - SCR_PAD:
            # Find ScrollView, scroll to self
            sv = find_ancestor_of_type(self, ScrollView)
            sv.scroll_to(self)


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # Tab keycode: (9, 'tab')
        if keycode == (9, 'tab'):
            # If last term, find EditScreen instance
            # and call add_card()
            if not self.focus_next: 
                es = find_ancestor_of_type(self, EditScreen)
                es.add_card()
        
        # Call original method
        super().keyboard_on_key_down(window, keycode, text, modifiers)

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
        for _ in range(3):
            self.add_card()

    def on_pre_enter(self):
        # To execute on screen load
        # Reset screen here or on_leave?
        pass

    def add_card(self): 
        '''
        Add a blank flashcard to the editor interface
        '''
        tw = TermWidget()
        if len(self.terms) >= 1:
            self.terms[-1].ids['defnfield'].focus_next = tw.ids['termfield']
        self.terms.append(tw)
        self.ids['termlayout'].add_widget(self.terms[-1])