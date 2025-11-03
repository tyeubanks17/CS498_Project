'''
editScreen.py

Definition for set creation/editing screen

History: 
22 Oct 2025 - Created
'''

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
import os
import csv


class EditScreen(Screen):
    Builder.load_file("./screens/editscreen.kv")

    