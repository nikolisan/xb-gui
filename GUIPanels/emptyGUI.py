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
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QSizePolicy


class EmptyPanel(QWidget):
    def __init__(self, name):
        super().__init__()
        self.page_name = name

        main_layout = QVBoxLayout(self)
        page_lbl = QLabel(self.page_name)
        page_lbl.setStyleSheet("QLabel{font-size: 16pt;}")
        page_lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        main_layout.addWidget(page_lbl)

        label = QLabel("<b>This is a placeholder panel<b>")
        label.setStyleSheet("QLabel{font-size: 16pt;}")

        main_layout.addWidget(label)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmptyPanel('Test Page')
    window.show()
    sys.exit(app.exec_())