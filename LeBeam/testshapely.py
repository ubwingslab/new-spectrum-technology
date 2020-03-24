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
from matplotlib import pyplot
from shapely.geometry.point import Point
import shapely.affinity
from descartes import PolygonPatch
# Note: download figures.py manually from shapely github repo, put it in shapely install directory
from ShapelyFigure import SIZE, GREEN, GRAY, set_limits


# 1st elem = center point (x,y) coordinates
# 2nd elem = the two semi-axis values (along x, along y)
# 3rd elem = angle in degrees between x-axis of the Cartesian base
#            and the corresponding semi-axis
ellipse = ((0, 0),(7, 2),0)

# Let create a circle of radius 1 around center point:
circ = shapely.geometry.Point(ellipse[0]).buffer(4)

print(circ)
print(shapely.affinity.translate(circ, 1, 1, 0))
exit(0)

# # Let create the ellipse along x and y:
# ell  = shapely.affinity.scale(circ, int(ellipse[1][0]), int(ellipse[1][1]))

# # Let rotate the ellipse (clockwise, x axis pointing right):
# ellr = shapely.affinity.rotate(ell,ellipse[2])

# print(ellr)

# If one need to rotate it clockwise along an upward pointing x axis:
# elrv = shapely.affinity.rotate(ell,90-ellipse[2])
# According to the man, a positive value means a anti-clockwise angle,
# and a negative one a clockwise angle.


fig = pyplot.figure()
ax = fig.add_subplot(111)
patch = PolygonPatch(circ, fc=GREEN, ec=GRAY, alpha=0.5, zorder=2)
ax.add_patch(patch)
set_limits(ax, -5, 5, -5, 5)
pyplot.show()