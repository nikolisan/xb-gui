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

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout
from pathlib import Path
import json

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        config_path = Path(__file__).parent.parent.joinpath('configuration.conf')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                version_str = str(config.get('version', 'Unknown'))
        except Exception as e:
            print(e)


        # Top labels
        title = QLabel("<b>XBeach-G GUI [unofficial]</b>")
        version = QLabel(f"Version {version_str}")
        author = QLabel(f"Copyright © 2025 Nikolaos Andreakos")
        disclaimer = QLabel("<b>DISCLAIMER:</b>")
        disclaimer_text_1 = QLabel('''    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.''')
        disc_text_2 = QLabel('''    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.''')
        
        url_link = '<a href="https://www.gnu.org/licenses/">https://www.gnu.org/licenses/</a>'
        disc_text_3 = QLabel('    You should have received a copy of the GNU General Public License')
        disc_text_4 = QLabel(f'along with this program.  If not, see {url_link}.')
        
        disc_text_4.setOpenExternalLinks(True)
        disc_text_5 = QLabel('''By using this software you agree with this LICENSE''')




                                #  "The author(s) bear no liability for any damages may incurr by using the software.\n" \
                                #  "By using this software you agree with the license")
                            
        layout.addWidget(title)
        layout.addWidget(version)
        layout.addWidget(author)
        layout.addWidget(disclaimer)
        layout.addWidget(disclaimer_text_1)
        layout.addWidget(disc_text_2)
        layout.addWidget(disc_text_3)
        layout.addWidget(disc_text_4)
        layout.addWidget(disc_text_5)

        # License text box (non-editable)
        license_box = QTextEdit()
        license_box.setReadOnly(True)

        # Read license text from file
       
        license_path = Path(__file__).parent.parent.joinpath('assets/LICENSE')
        try:
            with open(license_path, 'r', encoding='utf-8') as f:
                license_text = f.read()
        except Exception as e:
            license_text = f"Could not load license file:\n{e}"

        license_box.setPlainText(license_text)
        layout.addWidget(license_box)

        # OK button
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = AboutDialog()
    window.show()
    sys.exit(app.exec_())