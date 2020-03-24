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
#######################################################
# Date: 02/3/2019
# Author: Zhangyu Guan
# network class 
#######################################################

# from current folder
import net_name, net_func, net_node, netcfg, net_channel, net_gui

# Sabarish
# Import net_blk module here
import net_blk

import math, numpy as np

import ESN1_training

def new_ntwk(ntwk_type = None):
    '''
    create a network of the specified network type
    '''
    elmt_name = net_name.ntwk
    elmt_type = ntwk_type
    elmt_num  = 1    
    
    # network topology info, 1 network created
    addi_info = {'ntwk':None, 'parent':None}
    info = net_func.mkinfo(elmt_name, elmt_type, elmt_num, addi_info)    

    # create network
    return net_ntwk(info)                                                

class net_ntwk(net_func.netelmt_group):
    def __init__(self, net_info):      
        # from base network element
        net_func.netelmt_group.__init__(self, net_info) 

        # default network width and length in meter
        self.net_width  = 3000
        self.net_length = 3000
        
        # Maintain the list of all nodes in the network, initialized to empty list
        # Updated when nodes are created
        self.name_list_all_nodes = []
        
        # The list of the names of all node_to_node channel modules
        # Initialized to empty, updated when channel modules are created 
        # Also updated at each coherent time interval: reset all the channels and generate new channel states
        self.name_list_all_n2n_chnl = []
        
        # Total number of nodes in the network, incremented by 1 when a new node is created
        # The network-wide index of the node is also calculated based on this parameter
        # Initialize to 0
        self.tot_node_num = 0
               
        # x-, y- and z-axis coordinates of the nodes in name_list_all_nodes, updated when nodes created, move
        self.axis_x = []
        self.axis_y = []
        self.axis_z = []
		
		#l-, w- and h- dimensions of the nodes in name_list_all_blk, updated when nodes created, move
        self.dim_l = []
        self.dim_w = []
        self.dim_h = []
        
        # distance from between nodes: row index for transmitter, column index for receiver
        # will be updated when coordinates of the nodes changes
        self.dist_matrix = None 
        
        # positive path loss factor 
        self.positive_pathloss_fact = 4
        
        
        # The list of active wifi stations including the wifi ap
        # Initialized to be empty
        # Will be updated dynamically as wifi stations turn on and off
        self.list_active_wifi_sta = []
        
        # The list of all LTE base stations
        # For each LTE base station, the channel covariance matrix will be estimated
        # Initialized to empty, updated as LTE BSs are created
        self.list_lte_bs = []           # ground base station
        self.list_lte_bs_mobile = []    # mobile base station
        
        
        # GUI, created when the network elements have been created
        self.gui = None
        
        # Sabarish: Maintain a list of all the blockages, initialized to empty, updated when blockages are created
        self.name_list_all_blk = []
        self.train_data_all_mbs = []
        self.coord = []
        self.rate = []
        self.grid_x_coord = []
        self.grid_y_coord = []
        
        print('Blank network created.')
        
    def reset_chnl(self):
        '''
        Reset all the node-to-node channels, called at the beginning of each coherent time interval
        '''
        
        # loop over all channel modules
        for chnl_name in self.name_list_all_n2n_chnl:
            # get the object of the channel modules
            chnl_obj = self.get_netelmt(chnl_name)
            
            # reset the channel
            chnl_obj.reset()
            
    def refresh_chnl(self):
        '''
        Refresh all the node-to-node channels, called at the beginning of each coherent time interval
        '''
        
        # loop over all channel modules
        for chnl_name in self.name_list_all_n2n_chnl:
            # get the object of the channel modules
            chnl_obj = self.get_netelmt(chnl_name)
            
            # reset the channel
            chnl_obj.refresh()            

    def operation(self, env):
        '''
        Periodic network operations
        '''
        while True:
            print(self.name + ': Refreshing channel at {}'.format(env.now))
            self.reset_chnl()                               # set channel to be ineffective
            self.refresh_chnl()                             # regenerate channel state information
            yield env.timeout(netcfg.chn_cohr_time_tic)     # wait for next channel coherent time interval
        
    def pre_processing(self):
        '''
        Func: After all the nodes have been created, initialize some parameters, e.g., the distance matrix        
        '''
        # Initialize distance between nodes
        self.ini_dist()
        
        # Initialize the channels for the network 
        self.ini_channel()
        
        # Initialize the channel variance matrix for each of the registered LTE BSs
        for name_lte_bs in self.list_lte_bs:
            # first get the object of the LTE BS with given name
            obj_lte_bs = self.get_netelmt(name_lte_bs)
            
            # update channel covariance matrix
            obj_lte_bs.est_chn_cov_from_wifi()
            
        # Initialize GUI
        if netcfg.gui == 'on':
            self.gui = net_gui.new_gui(self)
        
    def ini_channel(self):
        '''
        Func: Generate the channel modules for each pair of the nodes in the network
        '''
        
        # Initialize channel for each node
        for node_name in self.name_list_all_nodes:
            node_obj = self.get_netelmt(node_name)          # Get the object of the node 
            node_obj.ini_channel()                          # Initialize channel
        
                
    def ini_dist(self):
        '''
        Calculate the distance between nodes: row index - first node; column index - second node
        '''
        
        # check if there are nodes in the network
        if self.name_list_all_nodes == []:
            print('Error: There are no nodes in the network.')
            exit(0)        
            
        self.dist_matrix = None
        
        # Loop over all node names in self.name_list_all_nodes. For each name, calculate the distance to all other nodes
        # including itself. Then, append the obtained array to the distance matrix.
        for node_name in self.name_list_all_nodes:           
            # Obtain the object of the node, and then get the network-wide node index of the node
            node_obj = self.get_netelmt(node_name)
            node_index = node_obj.ntwk_wide_index
            
            # x-, y- and z-axis of current node
            curr_x = self.axis_x[node_index]
            curr_y = self.axis_y[node_index]
            curr_z = self.axis_z[node_index]
			
			# # l-, w- and h-dimension of current node
            # curr_l = self.dim_l[node_index]
            # curr_w = self.dim_w[node_index]
            # curr_h = self.dim_h[node_index]
            
            # convert x-, y- and z-axis from list to array
            array_axis_x = np.asarray(self.axis_x)
            array_axis_y = np.asarray(self.axis_y)
            array_axis_z = np.asarray(self.axis_z)
			
			# # convert l-, w- and h-dimensions from list to array
            # array_dim_l = np.asarray(self.dim_l)
            # array_dim_w = np.asarray(self.dim_w)
            # array_dim_h = np.asarray(self.dim_h)
            
            # calculate distance 
            curr_dst_array = np.sqrt(np.power(curr_x - array_axis_x, 2) + np.power(curr_y - array_axis_y, 2) + np.power(curr_z - array_axis_z, 2))

            # Update the overall distance matrix
            if self.dist_matrix is None:
                # This is the first row
                self.dist_matrix = curr_dst_array
            else:
                # append the current row to the overall distance matrix
                self.dist_matrix = np.vstack([self.dist_matrix, curr_dst_array])        
    
    def update_association(self):
        '''
        update the association between the user and the BS
        '''
        #1 - Get the list of all users
        #user_name_list = self.get_node_list(net_name.lte_ue)
        #list_base_stations= self.get_node_list(net_name.lte_bs)
        # print(user_name_list)
        # exit(0)
        
        #2 - For each user, get the distance to all BS
        #Find the list of all nodes
        #self.name_list_all_nodes

        #print ('\n')
        #print('all_bs_list:', list_base_stations)
        #exit(0)
        
        for bs in self.get_node_list(net_name.lte_bs):
            bs_obj = self.get_netelmt(bs)
            bs_obj.served_user = []
            bs_obj.served_user_oper_freq = []
            bs_obj.served_mbs = []
            bs_obj.serving_gbs = []
            bs_obj.dist_nearest_gbs = []
            bs_obj.dist_nearest_mbs = []
            bs_obj.interfering_mbs_distance = []
            bs_obj.interfering_gbs_distance = []
            bs_obj.backhaul_oper_freq = []
            bs_obj.interfering_bs_list = []
            
        bs_idx_list = []  #create a empty list for BS index
        ue_idx_list = []
        serving_bs_index_list = []
        serving_bs_name_list = []
        dist_serving_bs_list = []
        
        list_base_stations = self.get_node_list(net_name.lte_bs)
        #print(list_base_stations)
        #exit(0)
        user_name_list = self.get_node_list(net_name.lte_ue)
        
        #print (interfering_bs_list)
        #exit(0)
        
        for bs in list_base_stations:                    
            idx_bs = self.name_list_all_nodes.index(bs)       # find the index of this name
            bs_idx_list.append(idx_bs)
        #print ('bs idx list:' , bs_idx_list,'\n')
        
        list_users = self.get_node_list(net_name.lte_ue)
        #print('all users list', list_users)
        for user in list_users:
            idx_ue = self.name_list_all_nodes.index(user)
            ue_idx_list.append(idx_ue)
        #print ('ue idx list:', ue_idx_list,'\n')
		
        #exit(0)
		
        #Find the index of current user in list of all nodes
        #user_dist_row_to_bs_list = []
        for user in user_name_list:
            user_dist_row_to_bs_list = []
            idx = self.name_list_all_nodes.index(user)       # find the index of this name
            #print ('self.dist_matrix:', self.dist_matrix[idx])
            for bs in bs_idx_list:
                user_dist_row_to_bs = self.dist_matrix[idx][bs]
                user_dist_row_to_bs_list.append(user_dist_row_to_bs)
                
                # dist_serving_bs = min(user_dist_row_to_bs_list)
                # dist_serving_bs_list.append(dist_serving_bs)
            
            #exit(0)
            #print('all distance',user_dist_row_to_bs_list)
            #print(min(user_dist_row_to_bs_list))
            a=min(user_dist_row_to_bs_list)
            #print('nearest distance',a)
            
            nearest_bs_index = user_dist_row_to_bs_list.index(min(user_dist_row_to_bs_list))
            #print(nearest_bs_index)
            serving_bs_index_list.append(nearest_bs_index)
            
            nearest_bs_name =  list_base_stations[nearest_bs_index]
            serving_bs_name_list.append(nearest_bs_name)
            dist_serving_bs = list_base_stations[nearest_bs_index]
            dist_serving_bs_list.append(dist_serving_bs)
            #print ('user_dist_row_to_bs_list:',user_dist_row_to_bs_list)
            nearest_distance_bs = user_dist_row_to_bs_list[nearest_bs_index]
            #print ("Smallest distance is:", nearest_distance_bs) 
            #print ("Nearest BS Index for '{}' is '{}'".format(user, nearest_bs_name) )
            
            #exit(0)
            #print ("Nearest BS Name for '{}' is '{}'".format(user, nearest_bs_name), '\n')
			
            #print ("Nearest BS Index and Name for '{}' is '{}' and '{}'".format(user, nearest_bs_index, nearest_bs_name) , '\n')
            
            # We have determined the BS for a user, then update the information for this user.
            
        
            #1 - Find the object of this user
            bs_obj = self.get_netelmt(nearest_bs_name)
            user_obj = self.get_netelmt(user)
           
            #print("bs obj", bs_obj.__dict__)
            #print("usr obj", user_obj.__dict__)
            #print('\nusr obj', user_obj.serving_bs)
            #exit(0)
        
            #2 - Update the information
            
        
            user_obj.serving_bs = nearest_bs_name        #Update nearest bs name
            user_obj.dist_serving_bs = nearest_distance_bs   #Update nearest bs distance
            user_oper_freq = user_obj.oper_freq
            #print("usr obj", user_obj.__dict__)
            #print('usr obj', user_obj.serving_bs)
        
            bs_obj.served_user.append(user)
            bs_obj.served_user_oper_freq.append(user_oper_freq)
            #print(bs_obj.name, bs_obj.served_user,'\n\n')
            #exit(0)
            
            
            count_indiv_BS = {i:serving_bs_name_list.count(i) for i in serving_bs_name_list}
            #print ("User Name List", user_name_list,'\n')
            #print ("Serving BS index for all users list",serving_bs_index_list,'\n')   
            #print ("Serving BS name for all users list",serving_bs_name_list,'\n')
            #print ("Number of Serving BS group", count_indiv_BS,'\n')

            #exit(0)
            
            
            #print(self.dist_matrix[idx])
            #exit(0)
            
            #Obtain the corresponding row of the matrix

         #### Determine the interfering BS
        #interfering_bs_list = []
        list_base_stations = self.get_node_list(net_name.lte_bs)
        for user in user_name_list:
            user_obj = self.get_netelmt(user)
            user_obj.interfering_bs = []
            idx = self.name_list_all_nodes.index(user) 
            for bs in list_base_stations:
                if bs is not user_obj.serving_bs :
                    user_obj.interfering_bs.append(bs)
                    
            interfering_bs_list = user_obj.interfering_bs
            #print(interfering_bs_list)
        
            bs_idx_list = []
            user_dist_row_to_bs_list=[]
            for bs in interfering_bs_list:                    
                idx_bs = self.name_list_all_nodes.index(bs)       # find the index of this name
                bs_idx_list.append(idx_bs)
            #print(bs_idx_list)
            
            for bs in bs_idx_list:
                user_dist_row_to_bs = self.dist_matrix[idx][bs]
                user_dist_row_to_bs_list.append(user_dist_row_to_bs)
            #print(user_dist_row_to_bs_list,'\n')
            
            user_obj.dist_inter_bs_list = user_dist_row_to_bs_list

            # #print(user_obj.interfering_bs)
        
            # interfering_bs_list = user_obj.interfering_bs
            #print(interfering_bs_list)
            
    def update_association_mbs_bs_link(self):
        all_bs_list = self.get_node_list(net_name.lte_bs)
        ground_bs_list = all_bs_list[0:netcfg.num_lte_bs]
        mobile_bs_list = all_bs_list[netcfg.num_lte_bs:netcfg.num_lte_bs+netcfg.num_lte_bs_mobile+1]
       #print(all_bs_list,'\n',ground_bs_list,'\n',mobile_bs_list)
        
        ground_bs_idx_list = []  #create a empty list for BS index
        mobile_bs_idx_list = []
        serving_ground_bs_index_list = []
        serving_ground_bs_name_list = []
        dist_ground_serving_bs_list = []
        
        list_base_stations = self.get_node_list(net_name.lte_bs)
        #print(list_base_stations)
        #exit(0)
        user_name_list = self.get_node_list(net_name.lte_ue)
        
        #print (interfering_bs_list)
        #exit(0)
        
        for bs in ground_bs_list:                    
            idx_gbs = self.name_list_all_nodes.index(bs)       # find the index of this name
            ground_bs_idx_list.append(idx_gbs)

        for bs in mobile_bs_list:
            idx_mbs = self.name_list_all_nodes.index(bs)
            mobile_bs_idx_list.append(idx_mbs)#-netcfg.num_lte_bs)
        
        #print(ground_bs_idx_list,mobile_bs_idx_list)
        actual_list = mobile_bs_list
        for mbs in mobile_bs_list:
            #print('a',mbs)
            mbs_dist_row_to_gbs_list = []
            idx = self.name_list_all_nodes.index(mbs)
            interfering_distances = []
            for gbs in ground_bs_idx_list:
                #print('b',mbs)
                mbs_dist_row_to_gbs = self.dist_matrix[idx][gbs]
                mbs_dist_row_to_gbs_list.append(mbs_dist_row_to_gbs)
                #print('c',mbs_dist_row_to_gbs_list)
            #print('d',mbs_dist_row_to_gbs_list)
            smallest_distance = min(mbs_dist_row_to_gbs_list)
            #print(smallest_distance)
            if smallest_distance > netcfg.backhaul_tera_threshold:
                new_band = netcfg.band['milli']      
            else:
                new_band = netcfg.band['tera']   

            nearest_gbs_index = mbs_dist_row_to_gbs_list.index(smallest_distance)
            #print('e',nearest_mbs_index)
            nearest_gbs_name = ground_bs_list[nearest_gbs_index]
            #print('f',nearest_mbs_name)
            mbs_dist_row_to_gbs_list.remove(smallest_distance)
            #print(mbs_dist_row_to_gbs_list)
            mbs_obj=self.get_netelmt(mbs)
            gbs_obj=self.get_netelmt(nearest_gbs_name)
            mbs_obj.backhaul_oper_freq = new_band
            gbs_obj.backhaul_oper_freq.append(new_band)
            gbs_obj.served_mbs.append(mbs)
            mbs_obj.serving_gbs = nearest_gbs_name
            gbs_obj.dist_nearest_mbs.append(smallest_distance)
            mbs_obj.dist_nearest_gbs.append(smallest_distance)
            #gbs_obj.interfering_gbs_distance=mbs_dist_row_to_gbs_list
            mbs_obj.interfering_gbs_distance=mbs_dist_row_to_gbs_list
            #mbs_obj.interfering_mbs_list = actual_list.remove(mbs)
        
        for mbs in mobile_bs_list:
            inter_list = []
            mbs_obj = self.get_netelmt(mbs)
            for mbss in all_bs_list:
                if mbss != mbs:
                    inter_list.append(mbss)
            #print(inter_list)
            mbs_obj.interfering_bs_list = inter_list
            
            
    def updt_band_association(self):
        '''
        Update the band of this node with associated operating frequency
        '''
        user_name_list = self.get_node_list(net_name.lte_ue)
        
        for user in user_name_list:
            user_obj = self.get_netelmt(user)
            user_obj.updt_band()
            #print(user_obj.__dict__)
            #print(user_obj.serving_bs, '\t', user_obj.dist_serving_bs,'\t', user_obj.oper_freq)
        
    
    def ping(self):
        '''
        disp network information, only test purpose for now
        '''        
        net_func.netelmt_group.ping(self) 
        
    def set_net_area(self, net_width, net_length, net_height):
        '''
        set the width and length of the network area
        '''
        self.net_width  = net_width
        self.net_length = net_length
        self.net_height = net_height
        print('Network dimension is set to {}x{}x{} in meter.'.format(self.net_width, self.net_length, self.net_height))
    
    def set_grid_mid_points(self):
        '''
        Divide the network area into grids and  set the grid mid points
        '''
        list_x = []
        list_y = []
        
        #print(self.net_width)
        #print(self.net_length)
        area_network = self.net_width * self.net_length
        #print('area of network',area_network)
        #print(netcfg.grid_area_x)
        #print(netcfg.grid_area_y)
        area_grid = netcfg.grid_area_x * netcfg.grid_area_y
        #print('area of grid',area_grid)
        num_grids = area_network / area_grid
        #print('number of grids',num_grids)
        
        list_x = []
        list_y = []
        
        for x in range(0, self.net_length, netcfg.grid_area_x):
            x = x+5
            for y in range(0, self.net_width, netcfg.grid_area_y):
                y = y+5
                list_x.append(x)
                list_y.append(y)
                
        
        
        self.grid_x_coord = list_x
        self.grid_y_coord = list_y
        
        #print('\n')
        #print('x list',self.grid_x_coord,'\n')
        #print(len(self.grid_y_coord),'\n')
        #print('y list',self.grid_y_coord,'\n')
        #print(len(self.grid_y_coord),'\n')

        
        return self.grid_x_coord, self.grid_y_coord
        
        
    def add_gui(self):
        '''
        Add GUI
        '''
        if self.gui == None:
           self.gui = net_gui.new_gui(self)
        else:
           print('GUI is already created')
        
        
    def add_node(self, node_type, node_number):
        '''
        add nodes with given type and number of the nodes
        '''  
        # Check if the node type supported
        if node_type not in net_name.node_type_list:
            print('Error: Node type not supported.')
            exit(0)
        
        # Find out the group name corresponding to the node type
        group_name = net_name.node2group.get(node_type)
                        
        # If the network doesn't support this group, add the group to the network
        # and initialize the group to None 
        if hasattr(self, group_name) == False:
            setattr(self, group_name, None)
                
        # If the group hasn't bee created, create it
        if getattr(self, group_name) == None:            
            # Call the function to create the group object, defined in net_node.py
            new_group_obj = net_node.new_group(self, group_name)    
           
            # Update the group object for the network
            setattr(self, group_name, new_group_obj)
           
        # Add new nodes to the group
        group_obj = getattr(self, group_name)
        group_obj.add_node(node_type, node_number)  
            
    def get_node_list(self, node_type):
        '''
        Func: get the list of nodes with type node_type in the network
        node_type: node type
        '''
        # node list initialized to empty
        node_list = []
        
        # Check if the node type supported
        if node_type not in net_name.node_type_list:
            print('Error: Node type not supported.')
            exit(0)                
        
        # Find out the group name corresponding to the node type
        group_name = net_name.node2group.get(node_type)
                        
        # Get the node list
        if hasattr(self, group_name) == False:
            # If there is no such a group, do nothing
            print('Warning: No such node type {}'.format(group_name))                
        else:
            # Otherwise, get the group object
            group_obj = getattr(self, group_name)
            node_list = node_list + group_obj.member
               
        return node_list        
                      
    # Sabarish
    # Create a new blockage
    def new_blockage(block_name, block_type):
        ###################################################################
        elmt_name = block_name
        elmt_type = block_type       
        elmt_num  = 1               # Dummy parameter
        
        # network topology info, 1 network created
        addi_info = {'ntwk':self.ntwk, 'parent':self.ntwk}
        info = net_func.mkinfo(elmt_name, elmt_type, elmt_num, addi_info)

        # create node object            
        blk_obj  = net_blk.blockage(info)      # create the node object   

        # add the node to the corresponding group
        # Not needed actually
        # self.addmember(elmt_name)
        #self.ping()
        
        # Sabarish: update the self.name_list_all_blk here
        
        ###################################################################        

    def train_data_prep(self):
        '''Prepare data for ESN training'''
        #print('a')
        coord = self.coord
        rate = self.rate
        #print('coord', coord)
        #print('rate', rate)
        #exit(0)
        data_mbs = ESN1_training.data_train(coord, rate)
        #print('a',data_mbs)
        self.train_data_all_mbs = data_mbs
        #data_mbs = self.train_data_all_mbs
        #print('b',self.train_data_all_mbs)
        
        return self.train_data_all_mbs