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
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QPushButton, 
                             QSplitter, QWidget, QLabel, QLineEdit, QFileDialog, 
                             QSlider, QHBoxLayout, QFrame,  QSizePolicy, QMessageBox)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

import rasterio
from GUIPanels.raster_extract import RasterLineApp


class ExtractRaster(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.raster = None

        main_layout = QVBoxLayout(self)

        page_lbl = QLabel("Extra Tools: Extract from raster")
        page_lbl.setStyleSheet("QLabel{font-size: 16pt;}")
        page_lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        main_layout.addWidget(page_lbl)

        # File selection
        top_layout = QHBoxLayout()
        label = QLabel("Select raster:")
        self.textbox = QLineEdit()
        top_button = QPushButton("Browse")
        top_button.clicked.connect(self.load_raster)
        top_layout.addWidget(label)
        top_layout.addWidget(self.textbox)
        top_layout.addWidget(top_button)
        main_layout.addLayout(top_layout)

        # Split interface
        splitter = QSplitter()
        main_layout.addWidget(splitter)


        # Left panel
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # --- Controls Frame above Usage ---
        controls_frame = QFrame()
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        # Slider with value label
        slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(50)
        self.slider.setValue(10)
        slider_lbl = QLabel(f'<b>Max point interval</b')
        slider_value_label = QLabel(f'<b>{str(self.slider.value())}m</b')
        slider_layout.addWidget(slider_lbl,0)
        slider_layout.addWidget(self.slider,1)  # Stretch factor 1 for slider
        slider_layout.addWidget(slider_value_label,0)  # Stretch factor 0 for label
        controls_layout.addLayout(slider_layout)

        # Update label when slider moves
        self.slider.valueChanged.connect(lambda val: slider_value_label.setText(f'<b>{str(val)}m</b'))

        # Buttons in horizontal layout
        btn_layout = QHBoxLayout()
        button1 = QPushButton("Extract profiles")
        btn_layout.addWidget(button1)
        button1.clicked.connect(self.on_shift_enter_pressed)
        button2 = QPushButton("Unload raster")
        btn_layout.addWidget(button2)
        button2.clicked.connect(self.close_raster)
        controls_layout.addLayout(btn_layout)

        # Add controls frame to the left layout before the Usage label
        left_layout.addWidget(controls_frame)

        # Help
        
        group_box = QGroupBox("Usage")
        group_layout = QVBoxLayout(group_box)

        # label_title = QLabel("<b><u>Usage</u><b>")
        # label_title.setStyleSheet("font-size: 16pt;")

        label1 = QLabel(
            """• Double click on figure to start creating extraction lines\n
• To create the line Single click on the next point\n
• To select a line single click on top of it\n
• To delete a selected line press DELETE\n
• To extract the lines npress SHIFT+ENTER\n""")
        # label2 = QLabel("")
        # label3 = QLabel("")
        
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)

        label4 = QLabel("""• Scroll to ZOOM\n
• Right click drag to PAN""")
        
        # group_layout.addWidget(label_title)
        group_layout.addWidget(label1)
        # group_layout.addWidget(label2)
        # group_layout.addWidget(label3)
        group_layout.addWidget(hline)
        group_layout.addWidget(label4)
        group_layout.addStretch()


        left_layout.addWidget(group_box)
        splitter.addWidget(left_widget)

        # Right panel (Graph)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        right_layout.addWidget(self.canvas)
        splitter.addWidget(right_widget)

        handle = splitter.handle(1)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        handle.setLayout(layout)

        self.setLayout(main_layout)
    
    def open_raster(self):
        if self.file_path:
            self.raster = rasterio.open(self.file_path, mode='r')
            return self.raster
        return None
    
    def close_raster(self):
        if self.raster:
            self.raster.close()
            self.raster = None
            


    def load_raster(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Open raster", "", "GeoTIFF (*.tif *.tiff)")
        if self.file_path:
            self.textbox.setText(self.file_path)
            self.open_raster()
            self.raster_app = RasterLineApp(raster_src=self.raster, fig=self.fig, ax=self.ax, point_interval=self.slider.value())
            self.canvas.draw()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.on_delete_pressed()
        if event.key() in (Qt.Key_Return, Qt.Key_Enter) and event.modifiers() & Qt.ShiftModifier:
            self.on_shift_enter_pressed()

    def on_shift_enter_pressed(self):
        # Call your RasterLineApp's extraction logic, e.g.:
        if hasattr(self, 'raster_app') and self.raster_app:
            success = self.raster_app.extract_gdf()
            if isinstance(success, int) :
                if int(success) == 0:
                    QMessageBox.critical(self, "Error", "No extraction lines are created.")

    def on_delete_pressed(self):
        # Call your RasterLineApp's delete logic, e.g.:
        if hasattr(self, 'raster_app') and self.raster_app:
            self.raster_app.delete_selected()  # You need to implement this in RasterLineApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExtractRaster()
    window.show()
    sys.exit(app.exec_())