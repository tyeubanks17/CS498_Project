'''
editScreen.py

Definition for set creation/editing screen

History: 
22 Oct 2025 - Created
23 Oct 2025 - Add term/definition fields, tab navigation
27 Oct 2025 - Title/description fields; delete, reorder terms
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
        # If unfocusing, do nothing
        if not value: 
            return
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
        # Disable if tabbing backward (holding shift)
        if (
            keycode == (9, 'tab') and 
            'shift' not in modifiers and 
            not self.focus_next
        ):
            # If last term, find EditScreen instance
            # and call add_card()
            es = find_ancestor_of_type(self, EditScreen)
            es.add_card()
        
        # Call original method
        super().keyboard_on_key_down(window, keycode, text, modifiers)

class TermIndexInput(TextInput):
    '''
    Custom TextInput field for term index
    Calls move_term method when unfocused
    '''
    multiline = False
    write_tab = False

    def on_focus(self, instance, value): 
        '''
        Update card position on unfocus
        '''
        # Only run on unfocus
        if not value: 
            es = find_ancestor_of_type(self, EditScreen)
            card = find_ancestor_of_type(self, TermWidget)
            es.move_card_to_index(card, int(self.text))
        

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

    def insert_card_below(self): 
        '''
        Inserts a card below self in the editor
        '''
        e = self.get_editor()
        selfidx = e.get_terms().index(self)
        e.insert_card(TermWidget(), selfidx)

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
        Inserts at end of termlayout
        '''
        tw = TermWidget()
        terms = self.get_terms()
        if len(terms) >= 1:
            terms[0].ids['defnfield'].focus_next = tw.ids['termfield']
        else: 
            self.ids['descfield'].focus_next = tw.ids['termfield']
        tw.ids['idxfield'].text = str(len(terms) + 1)
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
        self.do_term_indexing()

    def insert_card(self, card: TermWidget, index_: int):
        '''
        Insert a given card at a particular index
        '''
        self.ids['termlayout'].add_widget(card, index=index_)
        self.do_tab_ordering()
        self.do_term_indexing()
        
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
        else: 
            # If first card, do nothing
            return
        # Fix tab ordering
        terms = self.get_terms()
        if idx >= len(terms)-2:
            self.ids['descfield'].focus_next = terms[idx+1].ids['termfield']
            terms[idx+1].ids['defnfield'].focus_next = terms[idx].ids['termfield']
        else: 
            terms[idx+2].ids['defnfield'].focus_next = terms[idx+1].ids['termfield']
            terms[idx+1].ids['defnfield'].focus_next = terms[idx].ids['termfield']
        if idx > 0:
            terms[idx].ids['defnfield'].focus_next = terms[idx-1].ids['termfield']
        else: 
            terms[idx].ids['defnfield'].focus_next = None
        terms[idx+1].focus = True
        # Update term indices
        terms[idx+1].ids['idxfield'].text = str(len(terms) - (idx+1))
        terms[idx].ids['idxfield'].text = str(len(terms) - idx)

    def move_card_down(self, card: TermWidget):
        '''
        Move card down in widget tree
        '''
        terms = self.get_terms()
        idx = terms.index(card)
        if idx > 0: 
            self.delete_card(card)
            self.ids['termlayout'].add_widget(card, index=idx-1)
        else: 
            # If last card, do nothing
            return
        # Fix tab ordering
        terms = self.get_terms()
        if idx >= len(terms)-1:
            self.ids['descfield'].focus_next = terms[idx].ids['termfield']
            terms[idx].ids['defnfield'].focus_next = terms[idx-1].ids['termfield']
        else: 
            terms[idx+1].ids['defnfield'].focus_next = terms[idx].ids['termfield']
            terms[idx].ids['defnfield'].focus_next = terms[idx-1].ids['termfield']
        if idx > 1: 
            terms[idx-1].ids['defnfield'].focus_next = terms[idx-2].ids['termfield']
        else: 
            terms[idx-1].ids['defnfield'].focus_next = None
        terms[idx-1].focus = True
        # Update term indices
        terms[idx-1].ids['idxfield'].text = str(len(terms) - (idx-1))
        if idx > 1:
            terms[idx-2].ids['idxfield'].text = str(len(terms) - (idx-2))

    def move_card_to_index(self, card: TermWidget, index: int): 
        '''
        Move card to specific index in tree
        '''
        # Convert index to 0-indexed reverse-ordering (to match Widget tree)
        terms = self.get_terms()
        idx = len(terms) - index
        self.delete_card(card)
        if idx < 0: 
            self.insert_card(card, 0)
        elif idx >= len(terms):
            self.insert_card(card, len(terms))
        else: 
            self.insert_card(card, idx)

    def do_tab_ordering(self):
        '''
        Reset tab navigation ordering (focus_next) for all terms
        '''
        terms = self.get_terms()
        if len(terms) <= 0:
            # If no terms, do nothing
            return
        self.ids['descfield'].focus_next = terms[-1].ids['termfield']
        if len(terms) > 1:
            terms[-1].ids['defnfield'].focus_next = terms[-2].ids['termfield']
        for idx in range(len(terms)):
            if idx < len(terms)-1: 
                terms[idx+1].ids['defnfield'].focus_next = terms[idx].ids['termfield']
        terms[0].ids['defnfield'].focus_next = None

    def do_term_indexing(self): 
        '''
        Update index fields for all terms
        '''
        terms = self.get_terms()
        for idx in range(len(terms)):
            terms[idx].ids['idxfield'].text = str(len(terms) - idx)