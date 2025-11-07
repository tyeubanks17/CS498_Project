#Make sure kivymd is installed
from kivymd.app import MDApp
from kivy.lang import Builder


class Card(MDApp):
    def build(self):
        return Builder.load_file("card.kv")


if __name__ == "__main__":
    Card().run()