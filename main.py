'''
main.py

The central manager for our study app.

History: 
22 Oct 2025 - Created, add terrible mock menu
'''

import os, csv

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

from screens.editscreen import EditScreen
from widgets import FileChooserCsv, CsvHeaderSelectPopup

class MenuScreen(Screen):
    '''
    Default screen that is loaded on instantiating StudyApp
    '''
    screens = ['editSet']
    # filechooser = FileChooserCsv()
    DEFAULT_IMPORT_PATH = os.path.join(os.path.expanduser("~"), "Downloads")

    def open_filechooser(self):
        # self.add_widget(FileChooserCsv())
        fc = FileChooserCsv(default_path=self.DEFAULT_IMPORT_PATH)
        def read_csv_callback(instance):
            if fc.selection:
                csv_path = fc.selection[0]
                print(f"Selected CSV: {csv_path}")
                rows = self.read_csv(csv_path)
        fc.bind(on_dismiss=read_csv_callback)
        fc.open()

    def read_csv(self, csv_path):
        print(f"Reading CSV from: {csv_path}")
        self.csv_path = csv_path
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                rows = list(reader)
            print(f"Headers found: {headers}")
            # self.open_header_selector(rows)
            header_select = CsvHeaderSelectPopup(options=headers)
            def csv_select_callback(instance):
                if header_select.selection:
                    self.create_custom_csv(rows, header_select.selection)
            header_select.bind(on_dismiss=csv_select_callback)
            header_select.open()

        except Exception as e:
            popup = Popup(title="Error", content=Label(text=f"Error reading CSV:\n{e}"),
                            size_hint=(0.6, 0.4))
            popup.open()

    # def open_header_selector(self, data):
    #     layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
    #     layout.add_widget(Label(text="Choose the column to use as 'term':"))
    #     spinner = Spinner(text=self.headers[0], values=self.headers, size_hint_y=None, height=44)
    #     layout.add_widget(spinner)
    #     btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
    #     ok_btn = Button(text="OK")
    #     cancel_btn = Button(text="Cancel")
    #     btn_layout.add_widget(ok_btn)
    #     btn_layout.add_widget(cancel_btn)
    #     layout.add_widget(btn_layout)

    #     popup = Popup(title="Select Term Column", content=layout, size_hint=(0.7, 0.6))

    #     def confirm(instance):
    #         term_column = spinner.text
    #         popup.dismiss()
    #         self.create_custom_csv(data, term_column)

    #     def cancel(instance):
    #         popup.dismiss()

    #     ok_btn.bind(on_release=confirm)
    #     cancel_btn.bind(on_release=cancel)
    #     popup.open()

    def create_custom_csv(self, data, term_column):
        try:
            file_name = os.path.basename(self.csv_path)
            script_dir = os.path.dirname(__file__)
            sets_dir = os.path.join(script_dir, 'sets')
            os.makedirs(sets_dir, exist_ok=True)
            print("made dir", sets_dir)
            new_csv_path = os.path.join(sets_dir, file_name)
            new_csv_path = os.path.abspath(new_csv_path)
            with open(new_csv_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['term', 'definition'])

                for row in data:
                    term = row.get(term_column, '')
                    definition_parts = [v for k, v in row.items() if k != term_column and v]
                    definition = '; '.join(definition_parts)
                    writer.writerow([term, definition])
                    print("row:", [term, definition])

            popup = Popup(title="Success",
                            content=Label(text=f"CSV created successfully!\nSaved to:\n{new_csv_path}"),
                            size_hint=(0.7, 0.5))
            popup.open()

        except Exception as e:
            popup = Popup(title="Error", content=Label(text=f"Error creating CSV:\n{e}"),
                            size_hint=(0.6, 0.4))
            popup.open()

        
    def delete_csv(self):
        script_dir = os.path.dirname(__file__)
        sets_dir = os.path.abspath(os.path.join(script_dir, '..', 'sets'))
        os.makedirs(sets_dir, exist_ok=True)
        box = BoxLayout(orientation='vertical', spacing=20)
        filechooser = FileChooserListView(
            path=sets_dir,
            filters=["*.csv"]
        )
        box.add_widget(filechooser)
        buttons = BoxLayout(size_hint_y=None, height=50, spacing=10)
        delete_btn = Button(text="Delete", background_color=(1, 0.3, 0.3, 1))
        cancel_btn = Button(text="Cancel")
        buttons.add_widget(delete_btn)
        buttons.add_widget(cancel_btn)
        box.add_widget(buttons)

        popup = Popup(title="Delete CSV File", content=box, size_hint=(0.9, 0.9))

        def delete_file(instance):
            selected = filechooser.selection
            if selected:
                file_path = selected[0]
                file_name = os.path.basename(file_path)
                try:
                    os.remove(file_path)
                    popup.dismiss()
                    success_popup = Popup(
                        title="Deleted",
                        content=Label(text=f"'{file_name}' deleted successfully."),
                        size_hint=(0.6, 0.4)
                    )
                    success_popup.open()
                except Exception as e:
                    error_popup = Popup(
                        title="Error",
                        content=Label(text=f"Error deleting file:\n{e}"),
                        size_hint=(0.6, 0.4)
                    )
                    error_popup.open()
            else:
                warn_popup = Popup(
                    title="No File Selected",
                    content=Label(text="Please select a CSV file first."),
                    size_hint=(0.6, 0.4)
                )
                warn_popup.open()

        def cancel(instance):
            popup.dismiss()

        delete_btn.bind(on_release=delete_file)
        cancel_btn.bind(on_release=cancel)
        popup.open()

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

        return sm

if __name__ == "__main__":
    StudyApp().run()

