'''
main.py

The central manager for our study app.

History: 
22 Oct 2025 - Created, add terrible mock menu
'''

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen

from screens.editscreen import EditScreen

class MenuScreen(Screen):
    '''
    Default screen that is loaded on instantiating StudyApp
    '''
    screens = ['editSet']

class StudyApp(App):
    '''
    StudyApp kivy.app inherited class
    '''
    def build(self): 
        Builder.load_file('global-styles.kv')
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(EditScreen(name='editSet'))

        return sm
    

if __name__ == "__main__":
    StudyApp().run()