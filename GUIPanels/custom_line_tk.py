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

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class LineInputDialog(tk.Tk):
    def __init__(self, default_name, def_startX="", def_startY="", def_endX="", def_endY=""):
        super().__init__()
        self.title("New line")

        w=365
        h=175
        ws=self.winfo_screenwidth()
        hs=self.winfo_screenheight()
        x=(ws/2)-(w/2)
        y=(hs/2)-(h/2)
        self.geometry('%dx%d+%d+%d'%(w,h,x,y))
        self.minsize(365, 175)
        self.resizable(False, False)
        self.result = None

        label1 = ttk.Label(self, text='Profile name:')
        labelX = ttk.Label(self, text='Easting')
        labelY = ttk.Label(self, text='Northing')
        label2 = ttk.Label(self, text='Start point:')
        label3 = ttk.Label(self, text='End point:')

        self.entryName = ttk.Entry(self)
        self.entryName.insert(0, default_name)
        self.entryName.focus_set()

        self.startX = ttk.Entry(self)
        self.startX.insert(0, def_startX)
        self.startY = ttk.Entry(self)
        self.startY.insert(0, def_startY)
        self.endX = ttk.Entry(self)
        self.endX.insert(0, def_endX)
        self.endY = ttk.Entry(self)
        self.endY.insert(0, def_endY)

        self.columnconfigure(0, weight=1)
        self.columnconfigure((2,3), weight=3)

        self.rowconfigure((0,1,2,3,4), weight=1)


        label1.grid(row = 0, column= 0, sticky='ew', padx=5)
        label2.grid(row = 2, column= 0, sticky='ew', padx=5)
        label3.grid(row = 3, column= 0, sticky='ew', padx=5)

        labelX.grid(row = 1, column= 2, sticky='ew', padx=5)
        labelY.grid(row = 1, column= 3, sticky='ew', padx=5)


        self.entryName.grid(row=0, column=2, columnspan=2, sticky='ew', padx=5)
        self.startX.grid(row=2, column=2, columnspan=1, sticky='ew', padx=5)
        self.startY.grid(row=2, column=3, columnspan=1, sticky='ew', padx=5)
        self.endX.grid(row=3, column=2, columnspan=1, sticky='ew', padx=5)
        self.endY.grid(row=3, column=3, columnspan=1, sticky='ew', padx=5)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=4, column=2, columnspan=2, sticky='e', padx=5)
        ttk.Button(btn_frame, text="Save", width=8, command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", width=8, command=self.on_cancel).pack(side=tk.LEFT, padx=5)

        self.bind('<Return>', lambda event: self.on_ok())
        self.bind('<Escape>', lambda event: self.on_cancel())

    def on_ok(self):
        try:
            startX = float(self.startX.get().strip())
            startY = float(self.startY.get().strip())
            endX = float(self.endX.get().strip())
            endY = float(self.endY.get().strip())
        except ValueError:
            messagebox.showerror("Input Error", "Coordinates must be numeric.")
            return
        
        if not startX or not startY or not endX or not endY:
            messagebox.showerror("Input Error", "All coordinates must be provided.")
            return
        if startX == endX and startY == endY:
            messagebox.showerror("Input Error", "Start and end points cannot be the same.")
            return
        if startX < 0 or startY < 0 or endX < 0 or endY < 0:
            messagebox.showerror("Input Error", "Coordinates must be positive.")
            return
        if startX > 1000000 or startY > 1000000 or endX > 1000000 or endY > 1000000:
            messagebox.showerror("Input Error", "Coordinates are out of bounds.")
            return
        if not self.entryName.get().isalnum():
            messagebox.showerror("Input Error", "Profile name must be alphanumeric.")
            return
        if len(self.entryName.get()) > 10:
            messagebox.showerror("Input Error", "Profile name must be less than 20 characters.")
            return
        if not self.entryName.get()[0].isalpha():
            messagebox.showerror("Input Error", "Profile name must start with a letter.")
            return


        self.result = {
            'name' : self.entryName.get(),
            'startX': startX,
            'startY': startY,
            'endX': endX,
            'endY': endY
        }
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()


if __name__ == '__main__':
    dialog = LineInputDialog('P1')
    dialog.mainloop()
    
    print(dialog.result)