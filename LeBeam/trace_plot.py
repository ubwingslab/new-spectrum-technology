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
from matplotlib import pyplot as pp

def gyr_plot(data):
    '''roll, pitch, yaw'''
    tle_gyr = ['Variations in roll axis', 'Variations in pitch axis', 'Variations in yaw axis']
    color = ['r','b','k']
    #print(data)
    for i in range(3):
        gnrt_plot(data[:, i+1], i+1, tle_gyr[i], color[i])
    pp.show()
    
def laac_plot(data):
    '''x, y, z coordinates'''
    tle_laac = ['Variations in X axis', 'Variations in Y axis', 'Variations in Z axis']
    color = ['r','b','k']
    #print(data)
    # for i in range(3):
        # gnrt_plot(data[:, i+1], i+1, tle_laac[i],color[i])
    # pp.show()

def gnrt_plot(data,num,title,colr):
    data=data[0:500]
    #pp.figure(num)
    font = {'family' : 'sans',
        'size'   : 16}	
    pp.rc('font', **font)
    axis = 310+num
    pp.subplot(axis)
    pp.xlim(0,500)
    #pp.ylim(-0.8,0.8)
    if axis == 313:
        pp.xlabel('Network Run Time (slot)')
        #pp.ylim(-0.5,0.5)
    if axis == 312:
        pp.ylabel('Angular Velocity (rad/s)') 
    pp.plot(range(len(data)), data,c=colr)
    #pp.title(title)
    pp.grid(True)
