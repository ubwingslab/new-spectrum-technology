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

############################################################
## Antenna model: Cone model

## poly1 = ellipse()
## poly2 = ellipse()

## info = {'center':(0, 0), 'semi_xy':(1, 2), 'angle': 15}
## polygon1 = poly1.get_ploygon(info)
## info = {'center':(0.5, 0.7), 'semi_xy':(1, 1), 'angle': 0}
## polygon2 = poly1.get_ploygon(info)

## print(polygon1.intersection(polygon2).area)  
############################################################

from matplotlib import pyplot
from shapely.geometry.point import Point
import shapely.affinity
from descartes import PolygonPatch

class cone_mdl:
    '''
    cone model for radio radiation pattern 
    '''
    def __init__(self):
        # Center point
        self.center_x = 0
        self.center_y = 0
        self.center_z = 0
        
        # Semi-axis along x and y
        self.semi_x = 1
        self.semi_y = 1

        # Angle in degrees between x-axis and semi_x
        self.angle = 0
        
        # Polygon of the initial ellipse 
        self.polygon = self.ini_polygon()
        
    def ini_polygon(self):
        '''
        Initialize the wavefront polygon, a circle centered at (0, 0) with radius 1   
        '''
        return shapely.geometry.Point((self.center_x, self.center_y)).buffer(1)
    
    def get_polygon(self, info):
        '''
        Get the polygon of the ellipse with given information
        '''
        
        # First, initial the polygon
        self.polygon = self.ini_polygon()
        
        # Center point
        self.center_x = info['center'][0]
        self.center_y = info['center'][1]
        
        # Semi-axis along x and y
        self.semi_x = info['semi_xy'][0]
        self.semi_y = info['semi_xy'][1]

        # Angle in degrees between x-axis and semi_x
        self.angle = info['angle']    
            
        # Create the ellipse along x and y:
        polygon  = shapely.affinity.scale(self.polygon, self.semi_x, self.semi_y)

        # Rotate the ellipse (clockwise, x axis pointing right):
        polygon = shapely.affinity.rotate(polygon, self.angle)
        
        # Move the ellipse to the center
        polygon = shapely.affinity.translate(polygon, self.center_x, self.center_y, self.center_z)
        
        return polygon
    
      