# -*- coding: utf-8 -*-
"""
一个简单的数字棋盘游戏
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class OddEvenMatrix(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN))

        noticeLabel = toga.Label(
            '执行 >>>',
            style=Pack(padding=(0, 5))
        )
        self.inputBox = toga.TextInput(style=Pack(flex=1))

        cmd_box = toga.Box(style=Pack(direction=ROW, padding=5))
        cmd_box.add(noticeLabel)
        cmd_box.add(self.inputBox)

        button = toga.Button(
            'Run',
            on_press=self.runrun,
            style=Pack(padding=5)
        )

        

        main_box.add(cmd_box)
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def runrun(self, widget):
        print("Run ", self.inputBox.value)


def main():
    return OddEvenMatrix()
