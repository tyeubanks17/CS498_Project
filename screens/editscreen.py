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
from kivy.config import Config

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
    def get_editor(self):
        '''
        Return the nearest EditScreen instance
        '''
        return find_ancestor_of_type(self, EditScreen)

class EditScreen(Screen):
    NUM_TERMS_ON_LOAD = 2

    Builder.load_file("./screens/editscreen.kv")
    Config.set('graphics', 'resizable', True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add initial term objects on load
        for _ in range(self.NUM_TERMS_ON_LOAD):
            self.add_card()

    def on_pre_enter(self):
        # To execute on screen load
        # Reset screen here or on_leave?
        pass

    def get_terms(self):
        return self.ids['termlayout'].children

    def add_card(self): 
        '''
        Add a blank flashcard to the editor interface
        '''
        tw = TermWidget()
        terms = self.get_terms()
        if len(terms) >= 1:
            terms[-1].ids['defnfield'].focus_next = tw.ids['termfield']
        else: 
            self.ids['descfield'].focus_next = tw.ids['termfield']
        self.ids['termlayout'].add_widget(tw)

    def delete_card(self, card: TermWidget):
        '''
        Delete card from editor
        '''
        terms = self.get_terms()
        idx = terms.index(card)
        # Handle tab naviagation
        # If card was not on extreme end
        if idx >= 1 and len(terms) > idx+1:
            terms[idx-1].ids['defnfield'].focus_next = terms[idx+1].ids['termfield']
        elif idx == 0 and len(terms) > idx+1:
            # If card was first, update descfield focus_next
            self.ids['descfield'].focus_next = terms[idx+1].ids['termfield']
        elif idx == len(terms)-1 and idx >= 1: 
            # If card was last, remove focus_next from previous
            terms[idx-1].ids['defnfield'].focus_next = None
        else: 
            # If card was only one in list, add blank card when removing
            self.add_card()
            self.ids['descfield'].focus_next = terms[-1].ids['termfield']
        self.ids['termlayout'].remove_widget(card)
    def move_card_up(self, card: TermWidget):
        
        '''
        Move card up in widget tree
        '''
        terms = self.get_terms()
        idx = terms.index(card)
        # If last card, do nothing
        if idx < len(terms)-1: 
            self.delete_card(card)
            self.ids['termlayout'].add_widget(card, index=idx+1)
            
    def move_card_down(self, card: TermWidget):
        '''
        Move card down in widget tree
        '''
        terms = self.get_terms()
        idx = terms.index(card)
        # If first card, do nothing
        if idx > 0: 
            self.delete_card(card)
            self.ids['termlayout'].add_widget(card, index=idx-1)
            