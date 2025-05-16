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

import os
from tkinter import messagebox
import rasterio
import contextily as ctx
import matplotlib.pyplot as plt
import numpy as np
from rasterio.warp import Resampling
from shapely.geometry import Point
import geopandas as gpd



class RasterLineApp:
    def __init__(self, raster_src=None, raster_path=None, fig=None, ax=None, point_interval=10):
        os.system('cls' if os.name == 'nt' else 'clear')
        if raster_src:
            self.src = raster_src
        elif raster_path:
            self.raster_path = raster_path
            self.src = rasterio.open(self.raster_path, mode='r')

        self.CRS = self.src.crs
        self.lines = []
        self.point_interval_max = point_interval
        print(f'Max interval = {self.point_interval_max}')
        if fig is None and ax is None:
            self.fig, self.ax = plt.subplots(figsize=(10, 10))
        else:
            self.fig = fig
            self.ax = ax
        self.base_scale = 1.5
        self._is_panning = False
        self._pan_start = None
        self._orig_xlim = None
        self._orig_ylim = None

        self._setup_raster()
        self._setup_plot()
        self._connect_events()

    def _setup_raster(self):
        bounds = self.src.bounds
        self.extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        self.data = self.src.read(1, resampling=Resampling.nearest)
        if self.src.nodata is not None:
            self.data = np.ma.masked_equal(self.data, self.src.nodata)
        else:
            self.data = np.ma.masked_invalid(self.data)

    def _setup_plot(self):
        self.ax.set_xlim(self.extent[0] - 1000, self.extent[1] + 1000)
        self.ax.set_ylim(self.extent[2] - 1000, self.extent[3] + 1000)
        ctx.add_basemap(self.ax, crs=self.CRS, zoom="auto", source=ctx.providers.Esri.WorldImagery, alpha=0.5)
        im = self.ax.imshow(
            self.data,
            extent=self.extent,
            cmap='viridis',
            origin='upper',
            alpha=0.8
        )
        # Convert basemap to grayscale if needed
        for im in self.ax.get_images():
            arr = im.get_array()
            if arr.ndim == 3 and arr.shape[2] == 4:  # Select only the basemap
                gray = np.dot(arr[..., :3], [0.2989, 0.5870, 0.1140])
                im.set_data(gray)
                im.set_cmap('gray')
        self.ax.set_xlabel('Easting [m]')
        self.ax.set_ylabel('Northing [m]')


    def _connect_events(self):
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.fig.canvas.mpl_connect('scroll_event',self.zoom_fun)
        self.fig.canvas.mpl_connect('button_press_event', self.on_pan_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_pan_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_pan_release)

    def extract_gdf(self):
        gdf_points = []
        if len(self.lines)<1:
            print("no lines")
            return 0
        
        for line in self.lines:
            label = line[1].get_text()
            xy = line[0].get_xydata()
            x0, y0 = xy[0]
            x1, y1 = xy[1]
            dist = np.hypot(x1 - x0, y1 - y0)
            point_interval = min(np.round(dist/10, 1), self.point_interval_max)
            print(f'{point_interval=}')
            num_points = int(np.floor(dist)/point_interval) + 1
            xs = np.linspace(x0, x1, num_points)
            ys = np.linspace(y0, y1, num_points)
            points = list(zip(xs, ys))
            print(f"Line {label} from ({x0:.2f}, {y0:.2f}) to ({x1:.2f}, {y1:.2f}), {len(points)} points, Distance = {dist}")
            for pt in points:
                gdf_points.append({'label': label, 'geometry': Point(pt)})
        gdf = gpd.GeoDataFrame(gdf_points, crs=self.CRS)
        no_data = self.src.nodata
        coord_list = [(x, y) for x, y in zip(gdf["geometry"].x, gdf["geometry"].y)]
        gdf["value"] = [x[0] if x[0] != no_data else np.nan for x in self.src.sample(coord_list)]
        print(gdf.head())
        return gdf    
        
    def draw_line_advanced(self, label, startx, starty, endx, endy):
        x = [startx, endx]
        y = [starty, endy]
        line = self.ax.plot(x, y, '-r', picker=5)
        scatter1 = self.ax.scatter(startx, starty, color='red', s=50)
        scatter2 = self.ax.scatter(endx, endy, color='red', s=50, marker='X')
        mid_x = (x[0] + x[1]) / 2
        mid_y = (y[0] + y[1]) / 2
        label_text = self.ax.text(mid_x, mid_y, label, fontsize=9, color='blue', fontweight='bold',
                                  bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        self.ax.figure.canvas.draw()
        self.lines.append([line[0], label_text, scatter1, scatter2])

    def draw_line(self, startx, starty):
        xy = plt.ginput(1)
        endX = xy[0][0]
        endY = xy[0][1]
        diag = LineInputDialog(f'P{len(self.lines)+1}', startx, starty, endX, endY)
        diag.mainloop()
        if diag.result:
            name = diag.result["name"]
            startX = diag.result["startX"]
            startY = diag.result["startY"]
            endX = diag.result["endX"]
            endY = diag.result["endY"]
            if startX and startY and endX and endY:
                self.draw_line_advanced(name, startX, startY, endX, endY)
    
    def delete_selected(self):
        ax = self.ax
        if hasattr(ax, 'picked_object') and ax.picked_object:
            ax.picked_object.remove()
            for line in self.lines:
                if ax.picked_object in line:
                    line[1].remove()
                    line[2].remove()
                    line[3].remove()
                    self.lines.remove(line)
                    break
            ax.picked_object = None
            ax.figure.canvas.draw()
    # Event handling
    def on_pan_press(self, event):
        if event.button == 3 and event.inaxes == self.ax:
            self._is_panning = True
            self._pan_start = (event.xdata, event.ydata)

    def on_pan_motion(self, event):
        if self._is_panning and event.inaxes == self.ax:
            if event.xdata is not None and event.ydata is not None:
                dx = event.xdata - self._pan_start[0]
                dy = event.ydata - self._pan_start[1]
                xlim = self.ax.get_xlim()
                ylim = self.ax.get_ylim()
                self.ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
                self.ax.set_ylim(ylim[0] - dy, ylim[1] - dy)
                self.fig.canvas.draw_idle()

    def on_pan_release(self, event):
        if self._is_panning:
            self._is_panning = False
            self._pan_start = None

    def zoom_fun(self, event):
        # get the current x and y limits
        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/self.base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = self.base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print (event.button)
        # set new limits
        self.ax.set_xlim([xdata - cur_xrange*scale_factor,
                     xdata + cur_xrange*scale_factor])
        self.ax.set_ylim([ydata - cur_yrange*scale_factor,
                     ydata + cur_yrange*scale_factor])
        plt.draw() # force re-draw

    def on_click(self, event):
        if event.dblclick:
            if event.button == 1:
                self.draw_line(event.xdata, event.ydata)

    def on_pick(self, event):
        ax = self.ax
        if hasattr(ax, 'picked_object') and ax.picked_object is not None:
            if isinstance(ax.picked_object, plt.Line2D):
                ax.picked_object.set_color('r')
        this_artist = event.artist
        if isinstance(this_artist, plt.Line2D):
            this_artist.set_color('y')
        ax.picked_object = this_artist
        ax.figure.canvas.draw_idle()

    def on_key(self, event):
        ax = self.ax
        if event.key == u'delete':
            self.delete_selected()
        if event.key == u'shift+enter':
            self.extract_gdf()
            # self.src.close()
        if event.key == u'f1':

            messagebox.showinfo('Help',
                                '• Double click on figure to start creating extraction lines\n' \
                                '• To create the line Single click on the next point\n• To select a line single click on top of it\n' \
                                '• To delete a selected line press DELETE\n• To extract the lines npress SHIFT+ENTER\n' \
                                '\n' \
                                '• Scroll to ZOOM\n' \
                                '• Right click drag to PAN'
                                )

    def run(self):
        plt.show()
        self.src.close()

if __name__ == "__main__":
    from custom_line_tk import LineInputDialog
    from pathlib import Path
    path = Path.cwd().joinpath("ExampleInputs/west_bay_dorset.tif")
    app = RasterLineApp(raster_path=path)
    plt.show()


else:
    from GUIPanels.custom_line_tk import LineInputDialog