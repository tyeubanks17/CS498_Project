from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
import os

Builder.load_file("./screens/setselect.kv")


class SetSelectScreen(Screen):
    """Screen that lists available CSV sets in the ./sets folder and allows selection."""
    sets = ListProperty([])  # list of (filename, path)

    def on_pre_enter(self):
        """Refresh the list of sets every time the screen is about to be shown."""
        folder = os.path.join(os.getcwd(), "sets")
        files = []
        try:
            for fn in sorted(os.listdir(folder)):
                if fn.lower().endswith('.csv'):
                    files.append((fn, os.path.join(folder, fn)))
        except Exception:
            files = []
        self.sets = files
        # populate the RecycleView data here (kv can't use list comprehensions)
        try:
            self.ids.rv.data = [{'text': s[0], 'index': i} for i, s in enumerate(self.sets)]
        except Exception:
            # if ids not yet available or rv missing, silently ignore
            pass

    def select_set(self, index):
        """Called when a set row is pressed. Loads the set into the study screen and navigates to it."""
        try:
            if index < 0 or index >= len(self.sets):
                return
            _, path = self.sets[index]
            from kivy.app import App
            app = App.get_running_app()
            # Load the set into cardStudy screen and switch
            card_screen = app.root.get_screen('cardStudy')
            card_screen.load_study_set(path)
            app.root.current = 'cardStudy'
        except Exception as e:
            print(f"Error selecting set: {e}")
