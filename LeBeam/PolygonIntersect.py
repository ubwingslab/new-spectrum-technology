# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import shapely.geometry as sg
from shapely.geometry import box, Polygon
from matplotlib import pyplot as plt
from descartes import PolygonPatch
import shapely.ops as so

# Example polygon 
xy = [[130.21001, 27.200001], [129.52, 27.34], [129.45, 27.1], [130.13, 26.950001]]
polygon_shape = Polygon(xy)
# Example grid cell
gridcell_shape = box(129.5, -27.0, 129.75, 27.25)
# The intersection
x = polygon_shape.intersection(gridcell_shape).area
print(x)

#constructing the first rect as a polygon
r1 = sg.Polygon([(0,0),(0.8,0.8), (0.85,0.85), (0.87,0.87), (1,1), (0.95,0.9),(0.7,0),(0,0)])

#a shortcut for constructing a rectangular polygon
r2 = sg.box(0.5,0.5,1.5,1.5)

y = r1.intersection(r2).area
print(y)

#cascaded union can work on a list of shapes
new_shape = so.cascaded_union([r1,r2])

#exterior coordinates split into two arrays, xs and ys
# which is how matplotlib will need for plotting
xs, ys = new_shape.exterior.xy

#plot it
fig, axs = plt.subplots()
axs.fill(xs, ys, alpha=0.5, fc='r', ec='none')
plt.show() #if not interactive

