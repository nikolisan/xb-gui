"""
Copyright (C) 2025  Nikolaos Andreakos

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import re
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QApplication, QComboBox, QDialog, QDialogButtonBox, QFrame, QGroupBox, QHBoxLayout,
                             QLabel, QListWidget, QListView, QPushButton, QRadioButton, QSplitter, QStackedLayout,
                             QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem)

from GUIPanels.InitialConditionsGUI import ICPanel
from GUIPanels.ExtractFromRaster import ExtractRaster
from GUIPanels.about_dialog import AboutDialog


class MainPanel(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.profile_gui = ICPanel('Input: Profile')
        self.stormgui = ICPanel('Input: Storm')
        self.water_level_gui = ICPanel('Input: Water Elevation')

        self.raster_gui = ExtractRaster()

        self.stackLayout = QStackedLayout()
        self.stackLayout.addWidget(self.profile_gui) # -- id 1
        self.stackLayout.addWidget(self.stormgui) # -- id 2
        self.stackLayout.addWidget(self.water_level_gui) # -- id 3
        self.stackLayout.addWidget(self.raster_gui) # -- id 4
        self.setLayout(self.stackLayout)

        self.stackLayout.currentChanged.connect(parent.autoResize)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XBeach-G GUI [unofficial]")

        self.panel = MainPanel(self)
        self.menu = self.menuBar()
        self.main_widget = QWidget(self)

        config_button = QPushButton('Global\nConfiguration')
        config_button.setMinimumHeight(40)


        pages = {'Model Setup': {
                    'Inputs':['Profile_1', 'Storm_2', 'Water level_3'],
                    'Domain': ['Grid_4', 'Non-erodible layer_5'],
                    'Output': ['Run model_6'],
                    },
                  'Model Results':['Analyse_100'],
                  'Extra tools':['Extract from raster_4']
                }
        
        file_menu = self.menu.addMenu('File')
        file_actions = {
            'Create project': ('Create project', 'Ctrl+N'),
            'Open project': ('Open project', 'Ctrl+O'),
            'Save project': ('Save project', 'Ctrl+S'),
            'Save project as': ('Save project as', 'Ctrl+Shift+S'),
            'Exit': ('Exit', 'Ctrl+Q')
        }
        for label, (text, shortcut) in file_actions.items():
            action = file_menu.addAction(text)
            if shortcut:
                action.setShortcut(shortcut)
            action.triggered.connect(lambda checked, name=label: self.menu_action_triggered(name))

        # About as a button (not a dropdown)
        about_action = self.menu.addAction('About')
        about_action.triggered.connect(lambda: self.menu_action_triggered('About'))
        
        self.tree = QTreeWidget()
        self.populate_tree(self.tree, pages)
        self.tree.setHeaderHidden(True)
        self.tree.expandAll()
        self.tree.clicked.connect(self.handle_clicked)

        splitter = QSplitter()
        left_widget = QWidget()
        vlayout = QVBoxLayout()

        vlayout.addWidget(self.tree)
        left_widget.setLayout(vlayout)
        left_widget.setMinimumWidth(200)

        splitter.addWidget(left_widget)
        splitter.addWidget(self.panel)
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)

        handle = splitter.handle(1)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        handle.setLayout(layout)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(splitter)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        # self.setLayout(mainLayout)
        self.main_widget.setLayout(mainLayout)

        self.setCentralWidget(self.main_widget)
        
    def populate_tree(self, parent_widget, data):
        """ Recursively populate the tree with dictionary data, extracting ID but displaying only names. """
        for key, value in data.items():
            item = QTreeWidgetItem(parent_widget, [key, ""])  # Root-level items, hide ID

            if isinstance(value, dict):  # If value is a dictionary, create sub-items
                self.populate_tree(item, value)
            elif isinstance(value, list):  # If value is a list, add child items
                for sub_item in value:
                    match = re.search(r"_(\d+)", sub_item)  # Extract number after "_"
                    id_value = match.group(1) if match else ""  # Assign ID if found

                    QTreeWidgetItem(item, [sub_item.split("_")[0], id_value])  # Remove "_{digit}" from display


    def handle_clicked(self, event):
        item = self.tree.currentItem()
        print(item.text(0))
        if item and item.parent():  # Ensure it's not a top-level item
            myId = item.text(1)
            print(f"Clicked ID: {myId}")  # Print the ID
            try:
                self.panel.layout().setCurrentIndex(int(myId)-1)
            except ValueError:
                print('Not a main page')


    def autoResize(self, index):
        print(self.panel.stackLayout.widget(index).sizeHint())
        if not self.isMaximized():
            self.resize(self.panel.stackLayout.widget(index).sizeHint())
    
    def menu_action_triggered(self, name):
        # Implement your logic for each menu action here
        print(f"Menu action triggered: {name}")
        if name == 'Exit':
            self.close()
        elif name == 'About':
            dlg = AboutDialog()
            dlg.exec_()

if __name__ == '__main__':
    from pathlib import Path
    app = QApplication(sys.argv)
    print(str(Path(__file__).parent.joinpath("assets/icon.png")))
    app.setWindowIcon(QIcon(str(Path(__file__).parent.joinpath("assets/icon.png"))))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())