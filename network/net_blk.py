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

#######################################################
# Date: June/7/2019
# Author: Sabarish
# Blockage class and functions
# This module is not used any more, moved to net_node
#######################################################

import numpy as np
import net_func, net_name, netcfg
import net_node

# Sabarish
# Define the blockage class here
class blk_xxx(net_node.node):
    '''
    Definition of the blockage class
    xxx indicated classes not used any more 
    '''
    def __init__(self, net_info):      
        # from base network element
        net_node.node.__init__(self, net_info)
        
        # Initialize the blockage; here you can initialize different attributes        
        # self.x = 0
        # ...
		# Initializing the coordinates
        self.x = 0
        self.y = 0
        self.z = 0
		
		# Add the node location to the list of all nodes in the network
        # to maintain the information of the full list of nodes in the network
        self.ntwk.axis_x.append(self.x)                     
        self.ntwk.axis_y.append(self.y)
        self.ntwk.axis_z.append(self.z) 
	
		
        #Initializing the dimensions
        self.l = 0
        self.w = 0
        self.h = 0
		
		# Add the node dimension to the list of all nodes in the network
        # to maintain the information of the full list of nodes in the network
        self.ntwk.dim_l.append(self.l)                     
        self.ntwk.dim_w.append(self.w)
        self.ntwk.dim_h.append(self.h) 
		
		
    #def method1(self, arg1):
        # comments
		
    def get_coord(self):
        '''
        Func: get the current coordinates of the node
        return: the x-, y- and z- coordinates 
        '''
        return {'x':self.x, 'y': self.y, 'z':self.z}
    
    def set_coord(self, dict_xyz):
        '''
        Func: Set the coordinates of the node       
        '''
        self.x = dict_xyz['x']
        self.y = dict_xyz['Y']
        self.z = dict_xyz['Z']
		
    def get_dim(self):
        '''
        Func: get the dimensions of the blockage
        return: the l-, w- and h- dimensions
        '''
        return {'l':self.l, 'w': self.w, 'h':self.h}
    
    def set_dim(self, dict_xyz):
        '''
        Func: Set the dimensions of the blockage
		'''
        self.l = dict_lwh['l']
        self.w = dict_lwh['w']
        self.h = dict_lwh['h'] 

    def ping(self):
        net_func.netelmt_group.ping()
        
