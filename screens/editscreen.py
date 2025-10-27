'''
editScreen.py

Definition for set creation/editing screen

History: 
22 Oct 2025 - Created
'''

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

class EditScreen(Screen):
    Builder.load_file("./screens/editscreen.kv")