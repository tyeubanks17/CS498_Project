'''
kivy-demo.py
Updated:
16 Oct 2025
Jacob Schuetter

"Hello, World!" demo for Kivy
'''
import kivy
kivy.require('2.3.1') # Our version

from kivy.app import App
from kivy.uix.label import Label

# Create custom app, inheriting from Kivy's App class
class MyApp(App):
    def build(self): 
        return Label(text="Hello, World!")

# Run app immediately
if __name__ == "__main__":
    MyApp().run()  # Construct new instance of MyApp & run