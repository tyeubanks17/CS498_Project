'''
viewscreen.py

Definition for viewing imported sets and their terms

History: 
6 November 2025 - Created
'''

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.lang import Builder
import fileio

Builder.load_file("screens/viewscreen.kv")

# Set Viewer class
class ViewScreen(Screen):

    sets = ListProperty([])
    selected_set = None
    selected_name = StringProperty("")
    # Data to be displayed in the RecycleView
    rv_data = ListProperty([])

    # On startup, refresh the screen to check for new sets
    def on_pre_enter(self):
        self.refresh_set()

    # Refresh the screen, loading the csv files again.
    def refresh_set(self):
        try:
            self.sets = fileio.load_csvs("sets") or []
            self.selected_set = None
            self.selected_name = ""
            self.rv_data = []
        except Exception as e:
            print(f"[ERROR] Could not load sets: {e}")
            self.sets = []
            self.rv_data = []
    # Select a set on click, and filling out the table of terms and defs.
    def select_set(self, set_info):
        self.selected_set = set_info
        self.selected_name = set_info["name"]
        self.rv_data = [
            {"term": t, "definition": d}
            for t, d in zip(set_info["terms"], set_info["defs"])
        ]
    # Open the set importer.
    def import_set(self):
        fileio.open_filechooser()