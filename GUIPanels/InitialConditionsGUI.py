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
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QSplitter, QWidget, QLabel, QLineEdit, QFileDialog, QTableView, QHBoxLayout, QSizePolicy
import pandas as pd
from pyqtgraph import PlotWidget, mkPen

class PandasModel(QAbstractTableModel):
    """ Model for displaying pandas DataFrame in QTableView """
    def __init__(self, data=pd.DataFrame()):
        super().__init__()
        self.df = data

    def rowCount(self, parent=None):
        return self.df.shape[0]

    def columnCount(self, parent=None):
        return self.df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self.df.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.df.columns[section] if orientation == Qt.Horizontal else str(section)
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            try:
                # Convert value to float if necessary
                if self.df.iloc[index.row(), index.column()].dtype == 'float64':
                    value = float(value)
                elif self.df.iloc[index.row(), index.column()].dtype == 'int64':
                    value = int(value)

                self.df.iloc[index.row(), index.column()] = value
                self.dataChanged.emit(index, index)
                return True
            except ValueError:
                return False  # Prevent setting an invalid dtype
        return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable


class ICPanel(QWidget):
    def __init__(self, name):
        super().__init__()
        self.page_name = name
        self.df = pd.DataFrame()

        main_layout = QVBoxLayout(self)
        page_lbl = QLabel(self.page_name)
        page_lbl.setStyleSheet("QLabel{font-size: 16pt;}")
        page_lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        main_layout.addWidget(page_lbl)

        # File selection
        top_layout = QHBoxLayout()
        label = QLabel("Select file:")
        self.textbox = QLineEdit()
        top_button = QPushButton("Browse")
        top_button.clicked.connect(self.load_csv)
        top_layout.addWidget(label)
        top_layout.addWidget(self.textbox)
        top_layout.addWidget(top_button)
        main_layout.addLayout(top_layout)

        # Split interface
        splitter = QSplitter()
        main_layout.addWidget(splitter)

        # Left panel (CSV table)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Add/remove rows
        row_controls = QHBoxLayout()
        self.add_row_above_button = QPushButton("Add Row Above")
        self.add_row_above_button.clicked.connect(self.add_row)
        row_controls.addWidget(self.add_row_above_button)
        self.add_row_below_button = QPushButton("Add Row Below")
        self.add_row_below_button.clicked.connect(self.add_row)
        row_controls.addWidget(self.add_row_below_button)
        self.delete_row_button = QPushButton("Delete Row")
        self.delete_row_button.clicked.connect(self.delete_row)
        row_controls.addWidget(self.delete_row_button)
        left_layout.addLayout(row_controls)

        # Sort & Save buttons
        file_controls = QHBoxLayout()
        self.sort_btn = QPushButton("Sort")
        self.sort_btn.clicked.connect(self.sort_csv)
        file_controls.addWidget(self.sort_btn)
        self.save_csv_button = QPushButton("Save")
        self.save_csv_button.clicked.connect(self.save_csv)
        file_controls.addWidget(self.save_csv_button)
        left_layout.addLayout(file_controls)

        # Table view
        self.csv_table = QTableView()
        left_layout.addWidget(self.csv_table)
        splitter.addWidget(left_widget)

        # Right panel (Graph)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        self.pygraph = PlotWidget()
        self.pygraph.scene().sigMouseClicked.connect(self.on_plot_clicked)
        right_layout.addWidget(self.pygraph)
        splitter.addWidget(right_widget)

        self.setLayout(main_layout)

    def on_plot_clicked(self, event):
        """ Capture mouse click events on the plot and highlight the corresponding row in the table. """
        pos = event.scenePos()
        clicked_x = self.pygraph.plotItem.vb.mapSceneToView(pos).x()
        clicked_y = self.pygraph.plotItem.vb.mapSceneToView(pos).y()

        # Find the closest point in the dataset
        distances = ((self.df.iloc[:, 0] - clicked_x)**2 + (self.df.iloc[:, 1] - clicked_y)**2).pow(0.5)
        closest_index = distances.idxmin()

        self.csv_table.selectionModel().clearSelection()

        self.csv_table.selectionModel().select(
            self.model.index(closest_index, 0), 
            QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows
        )
        self.csv_table.scrollTo(self.model.index(closest_index, 0))  # Ensure the row is visible



    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.textbox.setText(file_path)
            self.df = pd.read_csv(file_path)
            self.display_dataframe()
            self.plot_graph()

    def display_dataframe(self):
        self.df = self.df.round(2)
        self.model = PandasModel(self.df)
        self.csv_table.setModel(self.model)
        self.model.dataChanged.connect(self.plot_graph)
        
    def plot_graph(self):
        self.pygraph.clear()
        if len(self.df) < 20:
            self.pygraph.plot(self.df.iloc[:, 0].astype(float), self.df.iloc[:, 1].astype(float), pen=mkPen(color='b', width=2), symbol='o')
        else:
            self.pygraph.plot(self.df.iloc[:, 0].astype(float), self.df.iloc[:, 1].astype(float), pen=mkPen(color='b', width=1))
        self.pygraph.getPlotItem().showGrid(x=True, y=True)
        vb = self.pygraph.getViewBox()
        vb.setBackgroundColor((255, 255, 255))

    def add_row(self):
        """ Add an empty row above or below the selected cell based on the button clicked. """
        sender_button = self.sender()  # Get the button that triggered the function

        selected_indexes = self.csv_table.selectionModel().selectedRows()
        if selected_indexes:
            row_index = selected_indexes[0].row()  # Get selected row
            if sender_button.text() == "Add Row Below":
                row_index += 1  # Adjust to insert below
        else:
            row_index = len(self.df)  # Default to the bottom

        # Insert an empty row in the DataFrame
        new_row = pd.Series([0] * self.df.shape[1], index=self.df.columns)
        self.df = pd.concat([self.df.iloc[:row_index], new_row.to_frame().T, self.df.iloc[row_index:]], ignore_index=True)

        # Refresh table display
        self.display_dataframe()
        self.plot_graph()


    def delete_row(self):
        selected_indexes = self.csv_table.selectionModel().selectedRows()
        if selected_indexes:
            row_index = selected_indexes[0].row()
            self.df = self.df.drop(index=row_index).reset_index(drop=True)
            self.display_dataframe()
            self.plot_graph()

    def sort_csv(self):
        self.df = self.df.sort_values(by=self.df.columns[0]).reset_index(drop=True)
        self.display_dataframe()
        self.plot_graph()

    def save_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.df.to_csv(file_path, index=False)
    
    def get_data(self):
        return self.df


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ICPanel('Test Page')
    window.show()
    sys.exit(app.exec_())