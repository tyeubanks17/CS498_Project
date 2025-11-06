'''
fileio.py
04 Nov 2025

Methods for creating popups and reading/deleting files
History:
04 November 2025 - Created
06 November 2025 - Added load_csv functions for the set viewer
'''
import os, csv

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

from widgets import FileChooserCsv, CsvHeaderSelectPopup

def open_filechooser():
    fc = FileChooserCsv()
    def read_csv_callback(instance):
        if hasattr(fc, 'selection') and fc.selection:
            csv_path = fc.selection
            print(f"Selected CSV: {csv_path}")
            rows = read_csv(csv_path)
    fc.bind(on_dismiss=read_csv_callback)
    fc.open()

def read_csv(csv_path):
    print(f"Reading CSV from: {csv_path}")
    file_name = os.path.basename(csv_path)
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=('term', 'definition'))
            headers = reader.fieldnames
            rows = [list(row.values()) for row in reader]
            if rows[0] == list(reader.fieldnames): 
                # Ignore first row if header row
                rows.pop(0)
        print(f"Headers found: {headers}")
        # self.open_header_selector(rows)
        header_select = CsvHeaderSelectPopup(options=headers)
        def csv_select_callback(instance):
            if hasattr(header_select, 'selection') and header_select.selection:
                create_custom_csv(file_name, rows, header_select.selection)
        header_select.bind(on_dismiss=csv_select_callback)
        header_select.open()

    except Exception as e:
        popup = Popup(title="Error", content=Label(text=f"Error reading CSV:\n{e}"),
                        size_hint=(0.6, 0.4))
        popup.open()

def load_csvs(directory="sets"):
    sets = []
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        return sets
    for files in os.listdir(directory):
        if files.endswith(".csv"):
            path = os.path.join(directory, files)
            try:
                with open(path, newline='', encoding='utf-8') as csvf:
                    reader = csv.DictReader(csvf)
                    terms, defs = [], []
                    for row in reader:
                        t = row.get("term", "").strip()
                        d = row.get("definition", "").strip()
                        if t or d:
                            terms.append(t)
                            defs.append(d)
            except Exception as e:
                print(f"[ERROR] Could not read {files}: {e}")
                continue
            if terms:
                sets.append({
                    "name": files.replace(".csv", ""),
                    "terms": terms,
                    "defs": defs,
                })
    return sets


def create_custom_csv(file_name, data, term_column):
    try:
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

        popup = Popup(title="Success",
                        content=Label(text=f"CSV created successfully!\nSaved to:\n{new_csv_path}"),
                        size_hint=(0.7, 0.5))
        popup.open()

    except Exception as e:
        popup = Popup(title="Error", content=Label(text=f"Error creating CSV:\n{e}"),
                        size_hint=(0.6, 0.4))
        popup.open()

    
def delete_csv():
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