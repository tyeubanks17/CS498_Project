'''
main.py

The central manager for our study app.

History: 
22 Oct 2025 - Created, add terrible mock menu
6 November 2025 - Added the set viewer
'''
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from screens.editscreen import EditScreen
from screens.viewscreen import ViewScreen
import fileio

class MenuScreen(Screen):
    '''
    Default screen that is loaded on instantiating StudyApp
    '''
    screens = ['editSet']

    # Alias methods for access in window
    def open_filechooser(self): 
        fileio.open_filechooser()
    def delete_csv(self):
        fileio.delete_csv()
    

class StudyApp(App):
    '''
    StudyApp kivy.app inherited class
    '''
    def build(self): 
        Builder.load_file('main.kv')
        Builder.load_file('widgets.kv')
        Builder.load_file('global-styles.kv')
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(EditScreen(name='editSet'))
        sm.add_widget(ViewScreen(name='viewSet'))

        return sm

if __name__ == "__main__":
    StudyApp().run()