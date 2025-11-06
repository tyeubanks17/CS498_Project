'''
editScreen.py

Definition for set creation/editing screen

History: 
22 Oct 2025 - Created
23 Oct 2025 - Add term/definition fields, tab navigation
27 Oct 2025 - Title/description fields; delete, reorder terms
'''
import os, re, csv

from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.config import Config

from widgets import *

from set import Set

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

#region custom_widgets

class TermTextInput(TextInput):
    '''
    Custom TextInput class to allow hijacking tab
    navigation to add new card
    '''
    def on_focus(self, instance, value):
        '''
        Scroll to text box when focused
        '''
        # On focus, autoscroll to location
        if value: 
            # Test whether element is visible
            left,bot = self.to_window(self.x, self.y)
            right,top = self.to_window(self.right, self.top)
            SCR_PAD = dp(20)
            if bot < 0 or top > Window.height - SCR_PAD:
                # Find ScrollView, scroll to self
                sv = find_ancestor_of_type(self, ScrollView)
                sv.scroll_to(self)
        else: 
            # On unfocus, call update_set()
            tw = find_ancestor_of_type(self, TermWidget)
            tw.update_set_term()


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

class SetTitleInput(TextInput): 
    '''
    Custom TextInput field for set title
    Filters disallowed characters for file
    naming purposes. 
    Based on docs: 
    https://kivy.org/doc/stable/api-kivy.uix.textinput.html#filtering
    '''
    # Disallowed characters regex
    bad_char = Set.ILLEGAL_CHARS_RE
    def insert_text(self, substring, from_undo=False):
        s = re.sub(self.bad_char, '', substring)
        # Display error if user inputs invalid characters (compare s to substring)?
        return super().insert_text(s, from_undo=from_undo)
        

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
    
    def update_set_term(self):
        '''
        Update corresponding term in Set data struct
        '''
        es = find_ancestor_of_type(self, EditScreen)
        es.update_set_term(self)


    def insert_card_below(self): 
        '''
        Inserts a card below self in the editor
        '''
        e = self.get_editor()
        selfidx = e.get_terms().index(self)
        e.insert_card(TermWidget(), selfidx)

#endregion

class EditScreen(Screen):
    NUM_TERMS_ON_LOAD = 2

    Builder.load_file("./screens/editscreen.kv")
    Config.set('graphics', 'resizable', True)

    def __init__(self, set_=None, **kwargs):
        super().__init__(**kwargs)
        # Initialize Set instance for current editor window
        # Defaults to new set instance (created on title entry), but may be passed in as param
        self.set = set_
        # Add initial term objects on load
        for _ in range(self.NUM_TERMS_ON_LOAD):
            self.add_card()

    def on_pre_enter(self):
        # To execute on screen load
        # Reset screen here or on_leave?
        pass

    def set_err(self, msg): 
        '''
        Set err msg
        '''
        self.ids['errmsg'].text = msg

    def clear_err(self): 
        '''
        Clear err msg
        '''
        self.ids['errmsg'].text = ""

    def csv_import_picker(self):
        '''
        Create a set based on data from a user-selected
        CSV file
        '''
        fc = FileChooserCsv()
        def on_select_callback(instance):
            '''Code to call when file is selected'''
            if fc.selection is None:
                return

            # If file selected, load file into GUI
            # Read csv
            try:
                with open(fc.selection, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    headers = reader.fieldnames
                    rows = [list(row.values()) for row in reader]
                print(f"Headers found: {headers}")
                # self.open_header_selector(rows)
                header_select = CsvHeaderSelectPopup(options=headers)
                def csv_select_callback(instance):
                    if header_select.selection:
                        self.populate_terms(rows)
                    else: 
                        raise ValueError("No term column selected")
                header_select.bind(on_dismiss=csv_select_callback)
                header_select.open()

            except Exception as e:
                popup = Popup(title="Error", content=Label(text=f"Error reading CSV:\n{e}"),
                                size_hint=(0.6, 0.4))
                popup.open()
            
        fc.bind(on_dismiss=on_select_callback)
        fc.open()
    
    def populate_terms(self, data): 
        '''
        Populate term cards from provided data

        Data argument should be a list of 2-element
        lists, where the first element is the term
        and the second is the definiton. 
        '''
        # Remove existing cards
        terms = self.get_terms()
        while len(terms) > 0: 
            self.ids['termlayout'].remove_widget(terms[0])
            terms = self.get_terms()

        # Populate cards from data
        for row in data: 
            if len(row) != 2: 
                raise ValueError("Too many columns in provided data to populate terms")
            self.add_card(*row)

    def update_title(self, text_content, focused): 
        '''
        Update filepath of Set instance when Title 
        field is updated
        '''
        # Run on defocus only
        if not focused: 
            self.clear_err()
            if not text_content: 
                # If text is null, do nothing
                self.set_err("Title cannot be empty.")
                return False
            # Depends on state of self.set
            save_file_path = Set.to_set_path(text_content.strip())
            if self.set is None: 
                # Title contents should not contain illegal characters
                assert not re.match(Set.ILLEGAL_CHARS_RE, text_content)
                # Raise error if file already exists
                if os.path.exists(save_file_path): 
                    self.set_err("A set with this name already exists!")
                    return False
                # Initialize set
                self.set = Set(save_file_path)
            else: 
                # Update Set path
                try: 
                    os.rename(self.set.path, save_file_path)
                    self.set.path = save_file_path
                except FileNotFoundError: 
                    # Savefile does not exist yet
                    self.set.path = save_file_path
                except FileExistsError: 
                    # File with name already exists
                    self.set_err("A set with this name already exists!")
                    return False
            self.update_set()
            return True
        
    def update_set(self): 
        '''
        Update entire set data struct
        Used when reordering terms

        N.B. not called when nudging terms 1 space up/down for efficiency
        '''
        if self.set is None: 
            self.set_err("Invalid title.")
            # Cannot do anything else until title is set and self.set is initialized
            return
        else: 
            self.clear_err()

        terms = self.get_terms()
        for i in range(len(terms)): 
            # Flip indexing to match visual order
            idx = len(terms) - i - 1
            term = terms[idx]
            if i >= len(self.set.data): 
                # Add new entry
                self.set.data.append({
                    'term': term.ids['termfield'].text,
                    'definition': term.ids['defnfield'].text
                })
            else: 
                self.set.data[i] = {
                    'term': term.ids['termfield'].text,
                    'definition': term.ids['defnfield'].text
                }
        print("Set path:",self.set.path)
        print(self.set.data)
        
    def update_set_term(self, input_widget): 
        '''
        Whenever user edits a term/definition,
        update the underlying Set object
        Called in on_focus of TermTextInputs
        '''
        if self.set is None: 
            self.set_err("Invalid title.")
            # Cannot do anything else until title is set and self.set is initialized
            return
        else: 
            self.clear_err()
        
        terms = self.get_terms()
        idx = terms.index(input_widget)
        # Flip indexing to match visual order
        idx = len(terms) - idx - 1
        if idx >= len(self.set.data): 
            # Add new entry
            self.set.data.append({
                'term': input_widget.ids['termfield'].text,
                'definition': input_widget.ids['defnfield'].text
            })
        else: 
            self.set.data[idx] = {
                'term': input_widget.ids['termfield'].text,
                'definition': input_widget.ids['defnfield'].text
            }
        print("Set path:",self.set.path)
        print(self.set.data)
        

    def save_set(self):
        '''
        Save set when save button is clicked
        Run final Set update
        Validate that there is a valid save path
        ''' 
        titleobj = self.ids['titlefield']
        self.clear_err()
        # Check title field and update set, if needed
        # Otherwise, print error
        if not self.update_title(titleobj.text, False): 
            self.ids['errmsg'].text += " Unable to save."
            return False
        # Set should be initialized by now
        # Run one last update and save
        assert self.set is not None
        self.update_set()
        self.set.save()
        return True

    #region card_manipulation_methods
    
    def get_terms(self):
        return self.ids['termlayout'].children

    def add_card(self, term="", defn=""): 
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
        tw.ids['termfield'].text = term
        tw.ids['defnfield'].text = defn
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
        self.update_set()
        
    def move_card_up(self, card: TermWidget):
        '''
        Move card up in widget tree
        '''
        terms = self.get_terms()
        idx = terms.index(card)

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
        self.update_set()

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
        self.update_set()

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

    #endregion
