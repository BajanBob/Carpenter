"""Carpenter's screens (Toga). Keep the logic in plain modules (no toga import) so it can be tested;
this file only builds the user interface and calls that logic."""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from carpenter import __version__
from carpenter.core import greeting


class Carpenter(toga.App):
    def startup(self):
        box = toga.Box(style=Pack(direction=COLUMN, margin=16, gap=8))
        self.name_input = toga.TextInput(placeholder="Your name")
        self.result = toga.Label("")
        box.add(toga.Label(f"Carpenter {__version__}"))
        box.add(self.name_input)
        box.add(toga.Button("Say hello", on_press=self.say_hello))
        box.add(self.result)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = box
        self.main_window.show()

    def say_hello(self, widget):
        self.result.text = greeting(self.name_input.value)


def main():
    return Carpenter()
