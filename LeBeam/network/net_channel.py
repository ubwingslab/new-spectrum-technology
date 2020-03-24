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
# Date: 02/7/2019
# Author: Zhangyu Guan
# wireless channel class and functions
#######################################################

import numpy as np
import net_func, net_name, netcfg, net_channel

class channel(net_func.netelmt_group):
    '''
    Definition of the channel class
    '''
    def __init__(self, net_info):      
        # from base network element
        net_func.netelmt_group.__init__(self, net_info)
        
        # Initialize the channels from this node to all the other nodes
        self.ini_channel_2node()

    def ping(self):
        net_func.netelmt_group.ping()
        
    def ini_channel_2node(self):
        print('Initializing channels from {} to all the other nodes...'.format(self.parent.type))
        
        # Loop over all nodes in the network
        for node_name in self.ntwk.name_list_all_nodes:
            
            # No need to consider the channel from a node to itself
            if node_name == self.parent.type:
                continue 
                                    
            # Otherwise, create the channel module for the node
            ###################################################################           
            # Construct a unique channel name with the names of two nodes
            elmt_name = self.get_name_chanl_2node(self.parent.type, node_name)               
            
            # If the channel module has been created, skip
            # This may happen since only one channel needed for each pair of nodes
            if elmt_name in self.ntwk.name_list_all_n2n_chnl:
                continue 
                       
            elmt_type = net_name.chnl_n2n
            elmt_num  = 1                                  # Dummy parameter
            
            # network topology info, 1 network created
            addi_info = {'ntwk':self.ntwk, 'parent':self, 'node1': self.parent.type, 'node2': node_name}
            info = net_func.mkinfo(elmt_name, elmt_type, elmt_num, addi_info)

            # create node object            
            chnl_obj  = net_channel.channel_node2node(info)      
            ###################################################################   

            # Add the channel name to the overall list maintained by the network
            self.ntwk.name_list_all_n2n_chnl.append(elmt_name)
            print('{} created.'.format(elmt_name))

    def get_name_chanl_2node(self, node_name1, node_name2):
        '''
        Func: Construct a unique name for the channel between two two nodes with node_name1 and node_name2
        Return: The constructed name
        '''
        
        # First get the object of the two nodes, and then the network-wide index of the two nodes
        # The channel name is constructed as chnl_node2node_index1_index2, with index1 the smaller one between 
        # the two indexes    

        # Get node object
        node_obj1 = self.get_netelmt(node_name1)
        node_obj2 = self.get_netelmt(node_name2)
        
        # Get network-wide index
        index1 = node_obj1.ntwk_wide_index
        index2 = node_obj2.ntwk_wide_index
        
        # Construct the channel name 
        if index1 < index2:
            chnl_name = net_name.chnl_n2n + '_' + str(index1) + '_' + str(index2)
        else:
            chnl_name = net_name.chnl_n2n + '_' + str(index2) + '_' + str(index1)
        
        return chnl_name
        
class channel_node2node(net_func.netelmt_group):
    '''
    Definition of the class for channels between a node pair
    '''
    def __init__(self, net_info):      
        # from base network element
        net_func.netelmt_group.__init__(self, net_info)
        
        # The two nodes corresponding to the channel
        self.node1 = net_info['addi_info']['node1']
        self.node2 = net_info['addi_info']['node2']
		
        # Dimension of the channel, depending on the number of antennas of the two nodes associated to the channel
		# num_slot: For regular channel updating, this parameter is default 1. For channel covariance estimation, 
		# this is the number of instances of channel states to be generated.
        self.chnl_dim = self.get_dimension(num_slot = 1)		
                
        # Current channel coefficients
        self.chnl_matrix = None
		
        # Effectiveness Indication: False - the channel has expired; True - in effects        
        self.efft = False		
		
		# Initialize current channel coefficients
		# First check if the channel is still in effect, refresh if not, otherwise do nothing
        if self.efft == False:
            self.chnl_matrix = self.gnrt_chnl_matrix(self.chnl_dim)
        else:
            pass
        
        # Set the channel state to be effectiveness, and refresh the channel for the involved receiver
		# No need to refresh the involved receiver, because for any two nodes, the corresponding channel
		# object will be identified by constructing a unique name, which will point to the same channel
		# object involving the transmitter and the receiver. So just set the channel to be effective
        self.efft = True
        
        print('Channel matrix initialized for {} and {}'.format(self.node1, self.node2))
        print(self.chnl_matrix)
        
    def refresh(self):
        '''
        Refresh the channel coefficients, called at the beginning of each channel choerent time interval
        '''
        if self.efft == False:
            self.chnl_matrix = self.gnrt_chnl_matrix(self.chnl_dim)
            self.efft = True
        else:
            pass            
        
    def gnrt_chnl_matrix(self, chnl_dim):
        '''
        Generate a set of channel coefficients for a pair of nodes
        The channel coefficient should be generated differently for different types of transmitter and receivers, 
        depending on the number of antennas
		
		chnl_dim: channel dimension 
        '''   
        
        # # Get the dimension of the channel matrix, row for transmitter, column for receiver 
		# This parameter will be passed by caller function
        # chnl_dim = self.get_dimension()
        
        # Calculate distance-dependent Ricean factor
        # First, get the distance 
        dist = self.get_dist()
        
        # Then, calculate Ricean factor
        ricean_fact = self.calc_rician_coeff(dist)
        
        # Generate Ricean factor
        chnl_matrix = self.gnrt_rician(ricean_fact, chnl_dim)
        
        return chnl_matrix
        
        
    def get_dimension(self, num_slot):
        '''
        Func: get the number of antennas of the transmit and receive nodes
		
		num_slot: The number of time slots for which channel coefficients will be generated. This is the 
		the third dimension (third_dim) is the number of time instance, this dimension is not used for regular
		channel updating in each coherent time interval. This will be used for generating channels 
		for estimating covariance matrix. Set to num_slot.
        '''
        
        # get the objects and then the network-wide index of the two nodes associated with the channel
        node_obj1 = self.get_netelmt(self.node1)            # get objects
        node_obj2 = self.get_netelmt(self.node2)        
        
        # number of antennas
        num_ant1 = node_obj1.num_ant
        num_ant2 = node_obj2.num_ant
        
        return {net_name.chn_row:num_ant1, net_name.chn_col:num_ant2, net_name.chn_third_dim: num_slot}
        
    def ping(self):
        net_func.netelmt_group.ping()

    def get_dist(self):
        '''
        Func: Get the distance for the channel. The distance information is stored in ntwk.dist_matrix and updated 
        if node moves
        '''
        
        # get the objects and then the network-wide index of the two nodes associated with the channel
        node_obj1 = self.get_netelmt(self.node1)            # get objects
        node_obj2 = self.get_netelmt(self.node2)
        
        idx1 = node_obj1.ntwk_wide_index                    # get indexes
        idx2 = node_obj2.ntwk_wide_index
        
        # Get the distance from the distance matrix 
        dist = None
        if self.ntwk.dist_matrix is None:
            print('Error: The distance matrix has not been initialized.')
        else:
            dist = self.ntwk.dist_matrix[idx1][idx2]
        
        return dist
        
    def reset(self):
        '''
        Func: Reset the effectiveness of the channel
        '''
        self.efft = False
        #print('Channel {} has been reset.'.format(self.type))
        
    def set_chnl(self):
        '''
        Func: Reset the channel to be in effects
        '''        
        self.efft = True
        
    def calc_rician_coeff(self, dist):
        '''
        Func: Calculate distance-dependent Rician channel coefficients
        dist: distance in meter
        
        For the LOS case, the Ricean K factor is based on K = 13-0.03*d (dB) where d is the
        distance between MS and BS in meters.  See 
        "Spatial channel model for multiple input multiple output simulations"    
        '''
        
        Rician_K = 13 -  0.03 * dist

        return Rician_K

    def gnrt_rician(self, K, dic_data_size):
        '''
        Func: For given total number of antennas, generate randomly a set of possible channel coefficients
        Then, for any pair of the antennas the channel coefficients will be selected from the pool in each coherent
        time interval
        
        dic_data_size: The total number of channel states to be generated. This is a dictionary: 'row' and 'column'
        K: parameter of the Rician channel
        '''
        # dimension of the channel matrix, row and column
        row = dic_data_size[net_name.chn_row]
        col = dic_data_size[net_name.chn_col]
        third_dim = dic_data_size[net_name.chn_third_dim]
        
        # Ricean channel parameters        
        mu  = np.math.sqrt(K/(K+1))
        s   = np.math.sqrt(1/(2*(K+1)))
        rician_chn = s*(np.random.standard_normal((row, col, third_dim)) + np.random.standard_normal((row, col, third_dim))*1j) + mu
        
        return rician_chn    
        
    def check_rule(self):
        '''
        Check if all rules followed by the channel
        This is only conducted when estimating channel covariance matrix,
        because at the moment the estimation supports only single-antenna wifi stations
        The checking is not needed for any other functionalities
        '''
        
        # if all the rules are met, return True, other return False. Initialized to True
        b_passed = True
        
        # Rule 1: single antenna only for wifi nodes. 
       
        # Check each of the two nodes involved in the channel
        for node in [self.node1, self.node2]:
            if net_name.wifi in node:
                # get the object of the node
                obj_node = self.get_netelmt(node)
                if obj_node.num_ant > 1:
                    b_passed = False
                    break
             
        return b_passed