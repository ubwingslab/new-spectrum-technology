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
# Date: 02/4/2019
# Author: Zhangyu Guan
# network node class 
#######################################################

# from current folder
from pyrr.geometric_tests import ray_intersect_sphere

import net_name, net_func, net_node, netcfg, net_channel

import ESN1_training 

import random

import numpy as np

from pyrr import geometric_tests as gt
from pyrr import line, plane, ray, sphere
import numpy.linalg as la

def new_group(ntwk_obj, group_name):
    '''
    Func: create a group for base station
    ntwk_obj: the object of the network to which the group is added
    group_name: the name of the group to be created
    '''
    elmt_name = group_name
    elmt_type = None            # Dummy parameter
    elmt_num  = 1               # Dummy parameter
    
    # network topology info, 1 network created
    addi_info = {'ntwk':ntwk_obj, 'parent':ntwk_obj}
    info = net_func.mkinfo(elmt_name, elmt_type, elmt_num, addi_info)    

    # create the group
    return node_group(info)  
       
class node_group(net_func.netelmt_group):
    '''
    Definition of the node group class
    '''
    def __init__(self, net_info):      
        # from base network element
        net_func.netelmt_group.__init__(self, net_info) 
        
    
    def add_node(self, node_type, num_node):        
        '''
        func: add new nodes to the group. For each new node, an new object will be created based on the 
        definition class
        node_type: the type of node to be added: BS, EU,...
        num_node: the number of nodes to be added
        '''
        
        # Construct the name of the node type        
        print('Adding '+node_type+'...')
        
        # Add node one by one, num_node will be added in total
        # node_id starts from 1 rather than 0
        for node_id_minus_1 in range(num_node):
            node_id = node_id_minus_1 + 1
            
            # construct the name of current node
            node_name = self.get_node_name(node_type, node_id)
            
            ###################################################################
            elmt_name = node_name
            elmt_type = node_type       
            elmt_num  = 1               # Dummy parameter
            
            # network topology info, 1 network created
            addi_info = {'ntwk':self.ntwk, 'parent':self}
            info = net_func.mkinfo(elmt_name, elmt_type, elmt_num, addi_info)

            # create node object            
            def_class = getattr(net_node, node_type)    # first, get the defining class for the node type
            node_obj  = def_class(info)                 # second, create the node object   
            #node_obj  = net_node.node(info)

            # add the node to the corresponding group
            self.addmember(elmt_name)
            #self.ping()
            ###################################################################            
            
    def get_node_name(self, node_type, node_id):
        '''
        func: construct an unique name with give node type and node id
        node_type: the type of the node
        node_id: the id of the node
        reutrn: constructed node name
        '''            
        return node_type + '_' + str(node_id)
        
    def get_node_obj(self, node_id):
        '''
        Func: return the node object with given node id
        node_id: the id of the node
        '''
        # construct the name of the node with node id and node type
        # the node type is recored in the group subtype when the group is created
        node_name = self.get_node_name(self, self.stype, node_id)
        return self.get_netelmt(node_name)
        
        
class node(net_func.netelmt_group):
    '''
    Definition of a general network node
    will server as the base class of LTE BS and UE, WiFi AP and users
    '''
    def __init__(self, net_info):      
        # from base network element
        net_func.netelmt_group.__init__(self, net_info)  
        
        # Transmit power, in mW, initialized to the maximum
        self.pwr = netcfg.max_pwr 
        
        # Frequency (GHz) and bandwidth (MHz)
        self.freq = 5 
        self.bandwidth = 20 

        # Number of antennas
        self.num_ant = netcfg.dft_num_ant
        
        # Add the node to the list of all nodes in the network
        # to maintain the full list of nodes in the network
        self.ntwk.name_list_all_nodes.append(self.type)             # Node name
        
        # Initialize the coordinate of the node
        self.coord_x = random.randint(0, self.ntwk.net_width)
        self.coord_y = random.randint(0, self.ntwk.net_length)                      
        self.coord_z = random.randint(0, self.ntwk.net_height)

        # Add the node location the list of all nodes in the network
        # to maintain the information of the full list of nodes in the network
        self.ntwk.axis_x.append(self.coord_x)                     
        self.ntwk.axis_y.append(self.coord_y)
        self.ntwk.axis_z.append(self.coord_z)   
		
		#Initializing the dimensions
        self.l = 0
        self.w = 0
        self.h = 0
        
		
        # # Add the node dimension to the list of all nodes in the network
        # # to maintain the information of the full list of nodes in the network
        # self.ntwk.dim_l.append(self.l)                     
        # self.ntwk.dim_w.append(self.w)
        # self.ntwk.dim_h.append(self.h) 

        # Network-wide index, calculated based on the total number of nodes in the network
        # The index of the first node is 0, incremented by 1 everytime a new node is created
        self.ntwk_wide_index = self.ntwk.tot_node_num
        
        # Increase the total number of nodes by 1
        self.ntwk.tot_node_num += 1
        
        # Channel module, initialized to None, updated in flyingbeam.pre_processing after all nodes have been 
        # created
        self.channel = None
        
    def ini_channel(self):
        '''
        Func: After the nodes have been created for the network, generate a channel module for 
        each node. The channel module will be used to manage the channel information from the node 
        to each of the other nodes in the network
        '''
        
        # Check if the channel module has been created, do nothing if yes
        if self.channel is not None:
            print('Warning: The channel module has already been created for {}'.format(self.type))
            return 0
        
        # Otherwise, create the channel module for the node
        ###################################################################
        elmt_name = self.type + '_' + net_name.chnl
        elmt_type = net_name.chnl
        elmt_num  = 1               # Dummy parameter
        
        # network topology info, 1 network created
        addi_info = {'ntwk':self.ntwk, 'parent':self}
        info = net_func.mkinfo(elmt_name, elmt_type, elmt_num, addi_info)

        # create node object            
        chnl_obj  = net_channel.channel(info)      
        ###################################################################         
        
        # update the channel module for this node
        self.channel = chnl_obj
        print('Channel modulate created for node {}'.format(self.type))
        
    def operation(self, env):
        '''
        test function
        '''
        while True:
            print(self.type + ': Start sensing at %d' % env.now)
            sensing_duration = 1500
            yield env.timeout(sensing_duration)
            
            # Transmission 
            print(self.type + ': Start transmitting at %d' % env.now)           
            yield env.timeout(netcfg.wifi_tsmt_time_tick)        
        
    def get_coord(self):
        '''
        Func: get the current coordinates of the node
        return: the x-, y- and z- coordinates 
        '''
        return {'x':self.coord_x, 'y': self.coord_y, 'z':self.coord_z}
    
    def set_coord(self, dict_xyz):
        '''
        Func: Set the coordinates of the node, and update ntwk.axis_x, ntwk.axis_y, ntwk.axis_z accordingly
        '''
        self.coord_x = dict_xyz['x']
        self.coord_y = dict_xyz['y']
        self.coord_z = dict_xyz['z']
        
        # we need to update the coordinates of the list of all nodes
        # First step, identify the index of this node in the node list
        
        this_node_name = self.name                                      # identify the name of this node            
        idx = self.ntwk.name_list_all_nodes.index(this_node_name)       # find the index of this name
        
        # Second, update the corresponding coordinates
        self.ntwk.axis_x[idx] = self.coord_x
        self.ntwk.axis_y[idx] = self.coord_y
        self.ntwk.axis_z[idx] = self.coord_z
        
class lte_bs(net_node.node):
    '''
    Definition of the LTE base station 
    '''
    def __init__(self, net_info):      
        # from base network element
        net_node.node.__init__(self, net_info)
        
        # set the number of antennas for LTE base station
        self.num_ant = netcfg.dft_num_ant_bs
        
        # Current active lte users, initialized to empty
        # Will be updated as the network runs        
        self.active_usr = []  
        
        # The LTE drone base station should fly with a minimum altitude (which has been set to zero in the father class)
        # so regenerate the initial altitude with the actual minimum altitude                    
        self.coord_z = random.randint(netcfg.min_flying_height, self.ntwk.net_height)

        # update the initial altitude for the LTE drone base station, which is the last element (just appended)
        self.ntwk.axis_z[-1] = self.coord_z      
        
        # Register the LTE BS in the network. For each of the registered LTE BS, channel covariance matrix will be
        # estimated
        self.register_lte_bs()
        
        #Current Served users, initialized to empty 
        self.served_user = []
        
        

    def register_lte_bs(self):
        '''
        Add this node to the list of LTE base stations, maintained by the network object
        For each LTE BS, the channel covariance matrix will be estimated        
        '''
        
        if self.name in self.ntwk.list_lte_bs:
            # already registered, do nothing
            print('Warning: {} already registered.'.format(self.name))
        else:
            self.ntwk.list_lte_bs.append(self.name)
            #print('{} registered.'.format(self.name))
        
        
        
    def esn_train(self):
        '''Train ESN for this node'''

        #print(name_list_bs)
        #print(list) 
        #for bs in self.ntwk.list_lte_bs_mobile:
        name_bs = self.name
        #print(name_bs)
        idx = self.ntwk.list_lte_bs.index(name_bs) 
        #print(idx)
        data = self.ntwk.train_data_all_mbs
        nt_obj = self.ntwk
        #print(nt_obj)
        ESN1_training.esn_training(idx, data, nt_obj)
        
# Sabarish
# define the class of lte_bs_mobile, similar to lte_bs_cog, use lte_bs as parent class            
class lte_bs_mobile(net_node.lte_bs): 
    '''
    Class of cognitive LTE base station with colocated wifi networks. This is a subclass of the LTE base station class. 
    i.e., the lte network shares the same spectrum with wifi networks
    '''
    def __init__(self, net_info):  
        net_node.lte_bs.__init__(self, net_info)
        
        # Channel covariance matrix between this LTE base station and all active interfering nodes (wifi nodes here)
        # Initialized to None, updated by calling self.est_chn_cov_from_wifi()
        self.chn_cov = None
        
        # velocity of the mobile base station, set to default 5 m/s
        self.velocity = 5
        
        # pause time of mobile base station, initialized to 1 second
        self.pause_time = 1
        
        # Register the LTE mobile BS in the network. For each of the registered LTE BS, channel covariance matrix will be
        # estimated
        self.register_lte_bs_mobile()       
        
    def operation(self, env):
        '''
        operation of each mobile base staion in each time slot, which is a tick of the env environment
        '''
        while True:          
            # # move this base station to a new location
            # # first step - get the current coordinates
            # current_coord = self.get_coord()
           
           
            # # second step - we create a new coordinate by adding some random number
            # new_coord = current_coord
            # new_coord['x'] = new_coord['x'] + 1
            # new_coord['y'] = new_coord['y'] + 2
            # new_coord['z'] = new_coord['z'] + 3
            # # third step - update the coordinate of this node
            # self.set_coord(new_coord)
            
            # display the new coordinate
            new_coord = self.get_coord()
            #print(self.type + ' moves to {} at time {}'.format(new_coord, env.now))
            #yield env.timeout(10)         
            
    def register_lte_bs_mobile(self):
        '''
        Add this node to the list of LTE Mobile base stations, maintained by the network object      
        '''
        
        if self.name in self.ntwk.list_lte_bs_mobile:
            # already registered, do nothing
            print('Warning: {} already registered.'.format(self.name))
        else:
            self.ntwk.list_lte_bs_mobile.append(self.name)
            #print('{} registered.'.format(self.name))
            
    def velocity(self):
        '''
        Func: set the current velocity of the node
        return: the v- velocity 
        '''
        return 15 #velocity in metres per second
		
    def pause_time(self):
        '''
        Func: Set the pause time of the node       
        '''
        return 30 #pause time in seconds
		
    #def your_method(self):
        #pass

        
class lte_bs_cog(net_node.lte_bs): 
    '''
    Class of cognitive LTE base station with colocated wifi networks. This is a subclass of the LTE base station class. 
    i.e., the lte network shares the same spectrum with wifi networks
    '''
    def __init__(self, net_info):  
        net_node.lte_bs.__init__(self, net_info)
        
        # Channel covariance matrix between this LTE base station and all active interfering nodes (wifi nodes here)
        # Initialized to None, updated by calling self.est_chn_cov_from_wifi()
        self.chn_cov = None
        
    def est_chn_cov_from_wifi(self, num_chn_smpl=1000):
        '''
        Estimate the channel covariance matrix between all active wifi users and this lte base station
        
        num_chn_smpl: The number of channel samples used for covariance estimation, default 1000
        '''
        
        # dummy operation 
        chn_cov = None
        
        # The sum of channel matrices over all wifi stations
        sum_chn_matrix = None
               
        # Get the list of active wifi stations, including wifi ap and users
        list_active_wifi_sta = self.ntwk.list_active_wifi_sta
        
        
        # For each wifi station, for each symbol duration, generate the channel state information from the wifi station to each antennas
        # of this lte BS
        
        # First get the name of this LTE base station
        name_lte_bs = self.name  
        for name_wifi_sta in list_active_wifi_sta:
            # get the name of the channel between name_lte_bs and name_wifi_sta
            name_chnl = self.channel.get_name_chanl_2node(name_lte_bs, name_wifi_sta)
            #print(name_chnl)
            
            # The corresponding channel object
            obj_chnl = self.get_netelmt(name_chnl)
            
            # Check if all rules followed by the channel
            # This checking is only conducted when estimating channel covariance matrix,
            # because at the moment the estimation supports only single-antenna wifi stations
            # The checking is not needed for other functionalities
            b_passed = obj_chnl.check_rule()
            if b_passed == False:
                print('Error: Failed to pass the channel dimension check.')
                exit(0)
            else:
                pass
                #print('Passed channel dimension check.')     
                
            # Get the dimension of the channel matrix. num_sym_4chn_cov_est is the number of symbols used
            # for covariance estimation, i.e., the third dimension of the dimension
            # The first two dimensions are determined by the number of antennas of the involved two nodes
            # and will be obtained by the function automatically
            # chnl_dim = obj_chnl.get_dimension(6)    # for test only
            third_dim = netcfg.num_sym_4chn_cov_est
            chnl_dim = obj_chnl.get_dimension(third_dim)
            
            # To make sure the generate channel matrix consistent with each other in dimension, the first node
            # must be LTE base station and the second must be wifi station. 
            # Otherwise, matrix transpose will be needed
            if net_name.lte in obj_chnl.node1 and net_name.wifi in obj_chnl.node2:
                # this is the wanted configuration, do nothing
                pass
            elif net_name.wifi in obj_chnl.node1 and net_name.lte in obj_chnl.node2:
                # the first and second dimension needs to be switched
                tmp_dim = chnl_dim[net_name.chn_row]                        # temporary variable for switching
                chnl_dim[net_name.chn_row] = chnl_dim[net_name.chn_col]     # switch
                chnl_dim[net_name.chn_col] = tmp_dim
                                       
            # generate channel matrix for this LTE BS and wifi station
            matx_chnl = obj_chnl.gnrt_chnl_matrix(chnl_dim)
            
            # Add the signals received from this wifi station to the overall signal
            if sum_chn_matrix is None:
                sum_chn_matrix = matx_chnl
            else:
                sum_chn_matrix = sum_chn_matrix + matx_chnl
                        
            #print(matx_chnl)
            #exit(0)
        
        # print(sum_chn_matrix)
        # print(sum_chn_matrix.shape)
        # exit(0)
        
        # Loop over all time slots. For each time slot, get the channel matrix and multiple it by its conjugate
        # transpose. Sum up all multiplication results                
        for slot_id in range(num_chn_smpl):
            # Get the channel state in this time slot
            sum_chnl_this_slot = sum_chn_matrix[:, :, slot_id]
            # print(sum_chnl_this_slot)
            # exit(0)
            
            # get the conjugate transpose
            sum_chnl_this_slot_H = np.matrix.getH(sum_chnl_this_slot)
            
            # Multiple 
            mul_chnl_chnlH = np.matmul(sum_chnl_this_slot, sum_chnl_this_slot_H)
            
            # Add the measurement of this time slot to the overall measurement
            if chn_cov is None:
                chn_cov = mul_chnl_chnlH
            else:
                chn_cov += mul_chnl_chnlH
                
        # Finally, divided the aggregated measurement by the number of time slots
        chn_cov = chn_cov/num_chn_smpl
        
        # print(chn_cov)
        # exit(0)
                
        # Update the channel covariance matrix for this LTE BS
        self.chn_cov = chn_cov
        print('Channel covariance matrix updated for {}'.format(self.name))
        # print(self.chn_cov)
             
class lte_ue(net_node.node):
    '''
    Definition of the LTE user equipment
    '''
    def __init__(self, net_info):      
        # from base network element
        net_node.node.__init__(self, net_info)
        
        #Serving Base Station
        self.serving_bs = None
        self.interfering_bs = []
        self.interfering_bs_los =[]
        self.interfering_bs_nlos = []

        self.blk_count = []
        self.count_blk_inter = []
        self.count_blk_serving = []
        self.total_abs_coeff = None
        self.blockages_nlos = []
        self.dist_serving_bs = None
        
        self.dist_inter_bs_list = []
        self.interfering_bs_los_distance = []
        self.interfering_bs_nlos_distance = []
        self.noise = {netcfg.band['micro']:None, netcfg.band['milli']:None, netcfg.band['tera']:None}

        #Noise for each User
        
     
        #Indicator of the operating frequency band
        #Take values from the list ['micro', 'milli', 'tera'] - Defined in netcfg
        # e.g., netcfg.band['micro']
        #self.oper_freq = netcfg.band['milli']  
        #print(self.oper_freq)
        #exit(0)
        self.oper_freq = None           
        self.is_blocked = None
        #self.received_power = {netcfg.band['micro']:None, netcfg.band['milli']:None, netcfg.band['tera']:None}
        self.rxd_pwr_serving =[]
        self.rxd_pwr_los_inter =[]
        self.rxd_pwr_nlos_inter =[]
        self.theta_list = []
        #self.interference = None
        self.sinr = None
        
       
        
        # self.oper_bandw = netcfg.bandw['milli']
        # print(self.oper_bandw)
        # exit(0)
        
        # print(self.noise[self.oper_freq])
        # exit(0)
        
        # freq = netcfg.freq[self.oper_freq]
        # bandw = netcfg.bandw[self.oper_freq]
        # print(freq, bandw)
        # exit(0)
        
        #self.set_noise()
        #self.sinr()
        
        #self.updt_band()
        
        #self.blk_detection()
        #print('{} registered.'.format(self.name))
        
    def get_noise(self):
        '''Get the noise of this node for the operating frequency'''
        
        noise = self.noise[self.oper_freq]
        #print(noise)
        #exit(0)
        return noise  
        
    def set_noise(self):
        '''
        Set the noise of this node
        '''
        if self.oper_freq == 'micro':
            #1-Generate noise for microwave 
            band = netcfg.band['micro']         
            bandw = netcfg.bandw[band]         
            noise_thermal_dB = -174 + (10 * np.log10(bandw *10**6)) + netcfg.noise_figure
            self.noise['micro'] = 10**(noise_thermal_dB/10)
            #self.noise['micro'] = 10e-11

        if self.oper_freq == 'milli':
            #2-Generate noise for millimeter
            # first get the bandwidth
            band = netcfg.band['milli']        
            bandw = netcfg.bandw[band]          
            noise_thermal_dB = -174 + (10 * np.log10(bandw *10**6)) + netcfg.noise_figure
            self.noise['milli'] = 10**(noise_thermal_dB/10)
            #self.noise['milli'] = 10e-11
        
        if self.oper_freq == 'tera':
            #3-Generate noise for terahertz
            # first get the bandwidth
            band = netcfg.band['tera']         # first get the band
            bandw = netcfg.bandw[band]          # then get the bandwidth
            noise_thermal_dB = -174 + (10 * np.log10(bandw *10**6)) + netcfg.noise_figure
            self.noise['tera'] = 10**(noise_thermal_dB/10)
            #self.noise['tera'] = 10e-11

       
       ####Later - Consider Absorption Noise for terahertz band####
       ####Later - Convert the noise value from dB to the necessary format####
       
    def updt_band(self): 
        '''Update the band of this node'''
        # Step 1: ... Get the distance of this node to the nearest BS
        #dist_bs = self.dist_serving_bs
        
        # Step 2: ... Check the distance with respect to the ref_dist.

        micro_ref_dist = netcfg.ref_dist[netcfg.band['micro']]
        milli_ref_dist = netcfg.ref_dist[netcfg.band['milli']]
        
        if self.dist_serving_bs > micro_ref_dist:
        # Last step: update the band based on the result from step 2
            new_band = netcfg.band['micro']    # This should be replaced with the new band
            self.oper_freq = new_band
            #print(self.oper_freq)

        elif self.dist_serving_bs > milli_ref_dist: 
            new_band = netcfg.band['milli']
            self.oper_freq = new_band
            #print(self.oper_freq)

        else:
            new_band = netcfg.band['tera']
            self.oper_freq = new_band
            #print(self.oper_freq)

    def blk_detection(self):
        '''Check if this node has a blockage in its path'''
        
        
        # Step 1: Get the coordinates of this user and the serving BS
        coord_usr = [self.coord_x +0.0, self.coord_y+0.0, self.coord_z+0.0]               #Get the coord of this node
        #print (coord_usr,'\n')
        bs = self.get_netelmt(self.serving_bs)                               #Get the obj of this nodes serving bs (here bs is object)
                       # Get the obj of this node interfering bs
        coord_bs  = [bs.coord_x + 0.0, bs.coord_y + 0.0, bs.coord_z + 0.0]                     #Get the coord of this serving bs
        
        #print (coord_bs,'\n')
        
        # Step 2: Construct two Rays, 
        direction_vec_1 = [self.coord_x - bs.coord_x, self.coord_y - bs.coord_y, self.coord_z - bs. coord_z]                  #Calculate direction vector 
        direction_vec_2 = [bs.coord_x - self.coord_x , bs.coord_y - self.coord_y , bs. coord_z - self.coord_z ]               #Calculate direction vector 
        #print (direction_vec_1,'\n')
        #print (direction_vec_2,'\n')
        
        #print(direction_vec_1,direction_vec_2)
        cosang = np.dot(direction_vec_1, direction_vec_2)
        sinang = la.norm(np.cross(direction_vec_1, direction_vec_2))
        angle = np.arctan2(sinang, cosang)
        #print('angle for serving bs',angle)
        #print('angle in degrees', angle*180/np.pi,'\n')
        
        ray1 = np.array([coord_bs, direction_vec_1])      #Ray from the BS
        ray2 = np.array([coord_usr, direction_vec_2])     #Ray from the User
        #print('ray1',direction_vec_1)
        #print('ray2',direction_vec_2)
        cosang = np.dot(direction_vec_1, direction_vec_2)
        sinang = la.norm(np.cross(direction_vec_1, direction_vec_2))
        angle = np.arctan2(sinang, cosang)
        #print('angle in radians',angle)
        #print('angle in degrees', angle*180/np.pi,'\n')
        #exit(0)
        #print ('ray1',ray1)
        #print ('ray2',ray2) 
        # Step 3: Check if the user is blocked by any blockage
             
        list_blk = self.ntwk.get_node_list(net_name.blk) 
        blk_cnt_serv = 0
        for blk in list_blk:
            blk_obj = self.get_netelmt(blk)
            #blk_obj.blk_aabb_box()
            #print('box',blk_obj.aabb)
        
            #print('r1,a',ray1, blk_obj.aabb)
            #print('r2,a',ray2, blk_obj.aabb)
            result_1 = gt.ray_intersect_aabb(ray1, blk_obj.aabb)
            #print('result1',result_1)
        
            result_2 = gt.ray_intersect_aabb(ray2, blk_obj.aabb)
            #print('result2',result_2,'\n')
        
            if not result_1 is None and not result_2 is None:
                    self.is_blocked = True
                    #break
                    blk_cnt_serv += 1
            else:
                    self.is_blocked = False
        self.count_blk_serving.append(blk_cnt_serv)
        #print(self.count_blk_serving)
        #print(sum(self.count_blk_serving))
        micro_ref_dist = netcfg.ref_dist[netcfg.band['micro']]
        milli_ref_dist = netcfg.ref_dist[netcfg.band['milli']]
        
        if self.is_blocked == True:
            if self.dist_serving_bs > micro_ref_dist:
                new_band = netcfg.band['micro']
                self.oper_freq = new_band  
                
            else:
                new_band = netcfg.band['milli']
                self.oper_freq = new_band
        
        interfering_bs_list = self.interfering_bs
        #print(interfering_bs_list)
        #exit()
        nlos_inter_bs_list = []
        los_inter_bs_list = []
        coord_usr = [self.coord_x +0.0, self.coord_y+0.0, self.coord_z+0.0]  
        self.interfering_bs_los = []
        self.interfering_bs_nlos = []
        self.interfering_bs_los_distance = []
        self.interfering_bs_nlos_distance = []
        
        for bs_interferer in interfering_bs_list:
            bs_inter = self.get_netelmt(bs_interferer)                              #Get the obj of this nodes serving bs (here bs is object)
            coord_bs_interferer  = [bs_inter.coord_x + 0.0, bs_inter.coord_y + 0.0, bs_inter.coord_z + 0.0]                     #Get the coord of this serving bs
            direction_vec_3 = [self.coord_x - bs_inter.coord_x, self.coord_y - bs_inter.coord_y, self.coord_z - bs_inter. coord_z]                  #Calculate direction vector 
            direction_vec_4 = [bs_inter.coord_x - self.coord_x , bs_inter.coord_y - self.coord_y , bs_inter. coord_z - self.coord_z ]               #Calculate direction vector 

            ray3 = np.array([coord_bs_interferer, direction_vec_1])      #Ray from the BS
            ray4 = np.array([coord_usr, direction_vec_2])     #Ray from the User
            list_blk = self.ntwk.get_node_list(net_name.blk) 
            blk_cnt = 0
            tot_abs_coeff = 0 
            idx = 0
            #print(list_blk)
            for blk in list_blk:
                blk_obj = self.get_netelmt(blk)
                #print('ray3', ray3)
                #print('aabb',blk_obj.aabb)
                result_3 = gt.ray_intersect_aabb(ray3, blk_obj.aabb)
                #print('result 3 ',result_3)
                #print('ray4', ray4)
                #print('aabb',blk_obj.aabb)
                result_4 = gt.ray_intersect_aabb(ray4, blk_obj.aabb)
                #print('result 4',result_4)
                
            if not result_3 is None and not result_4 is None:
                    blk_cnt += 1  
                    
            else:
                    pass
 
            if blk_cnt == 0:
                self.interfering_bs_los.append(bs_interferer)  
                idx = self.interfering_bs.index(bs_interferer)
                self.interfering_bs_los_distance.append(self.dist_inter_bs_list[idx])
            else:
                self.interfering_bs_nlos.append(bs_interferer)
                idx = self.interfering_bs.index(bs_interferer)
                self.interfering_bs_nlos_distance.append(self.dist_inter_bs_list[idx])
                self.count_blk_inter.append(blk_cnt)  
                
                
        count_blk_length = len(self.count_blk_inter)
        #print(count_blk_length)
        tot_abs_coeff = netcfg.abs_coeff ** count_blk_length
        self.total_abs_coeff = tot_abs_coeff
        
        #for self.dist_serving_bs  self.dist_serving_bs:
        # if self.oper_freq == 'milli':
            # print('milli',self.dist_serving_bs)
        # elif self.oper_freq == 'micro':
            # print('micro', self.dist_serving_bs)
        # else: 
            # print ('tera',self.dist_serving_bs)
        
           
        #exit(0)
        
        # Update if the user is blocked
        #self.is_blocked = new_value   #Update with true or false after the operation
        
        
    def sinr_calc(self):
        '''Calculate the SINR of this node'''
        #print('1 start')      
             
        if self.oper_freq == 'micro':
            serv_pwr = self.calc_rxd_pwr('micro')
            total_inter = self.calc_itf_micro()
            noise = self.noise['micro']

        elif self.oper_freq == 'milli':
            serv_pwr = self.calc_rxd_pwr('milli')
            total_inter = self.calc_itf_milli()
            noise = self.noise['milli']

        else:
            serv_pwr = self.calc_rxd_pwr('tera')
            total_inter = 0  
            noise = self.noise['tera']

        
        #print(total_inter)
        #print(noise)
        #exit(0)
        total_inter_noise = total_inter + noise
        sinr = serv_pwr / total_inter_noise
        self.sinr = sinr
        
        #print('1 end')

    def calc_itf_micro(self):
        ''' Calculate Interference for Microwave band'''
        #print('2 start')
        ''' los interference calculation for microwave'''
        los_inter = 0  
        #print(self.interfering_bs_los)
        #print(self.interfering_bs_los_distance)
        for bs in self.interfering_bs_los:
            freq = netcfg.freq['micro']
            free_space_path_loss = netcfg.constant * ((freq*1e9)**2)
            for dist in self.interfering_bs_los_distance: #looping over bs in los interference list (based on distance list)
                path_loss_exponent = dist ** netcfg.alpha_los
                loss_los = free_space_path_loss * path_loss_exponent
                tsmt_pwr = netcfg.tsmt_pwr['micro']
                rxd_pwr_los_inter = tsmt_pwr *1e-3 / loss_los
                los_inter = los_inter + rxd_pwr_los_inter
            self.rxd_pwr_los_inter.append(los_inter) #LOS interference - it is a list
        #print('2.1 start')    
        ''' nlos interference calculation for microwave'''
        nlos_inter = 0
        for bs in self.interfering_bs_nlos:
            freq = netcfg.freq['micro']
            free_space_path_loss = netcfg.constant * ((freq*1e9)**2)
            for dist in self.interfering_bs_nlos_distance: #looping over bs in nlos interference list (based on distance list)
                path_loss_exponent = dist ** netcfg.alpha_nlos
                loss_nlos = free_space_path_loss * path_loss_exponent
                tsmt_pwr = netcfg.tsmt_pwr['micro']
                rxd_pwr_nlos_inter = tsmt_pwr *1e-3 *self.total_abs_coeff / loss_nlos
                nlos_inter = nlos_inter + rxd_pwr_los_inter
            self.rxd_pwr_los_inter.append(nlos_inter) #NLOS interference - it is a list
        #print('2.2 start')
        #serv_pwr = sum(self.rxd_pwr_serving)                    #Get the rxd power of the serving bs from the list(it is just a single element)
        inter_los = sum(self.rxd_pwr_los_inter)                 #Get the total los interference 
        #print('total los inter',inter_los)
        inter_nlos = sum(self.rxd_pwr_nlos_inter)               #Get the total nlos interference 
        #print('total nlos inter',inter_nlos)
        #print('noise',noise)
        total_inter = inter_los + inter_nlos 
        #print('2 end')
        return total_inter
    
    def calc_itf_milli(self):
        '''Calculate interface for millimeter wave'''
        #print('3 start')
        coord_usr = [self.coord_x +0.0, self.coord_y+0.0, self.coord_z+0.0]               #Get the coord of this node
        bs = self.get_netelmt(self.serving_bs)                               #Get the obj of this nodes serving bs (here bs is object)             
        coord_bs  = [bs.coord_x + 0.0, bs.coord_y + 0.0, bs.coord_z + 0.0]                     #Get the coord of this serving bs
        #print (coord_usr,'...',coord_bs,'\n')
        direction_vec_1 = [self.coord_x - bs.coord_x, self.coord_y - bs.coord_y, self.coord_z - bs. coord_z]                  #Calculate direction vector 
        #print (direction_vec_1)
        interfering_bs_list = self.interfering_bs
        ##print (self.interfering_bs)
        #print('3.1')
        self.theta_list = []
        for bs_interferer in self.interfering_bs:
            
            bs_inter = self.get_netelmt(bs_interferer)   
            #print(bs_inter.served_user,'\n')
            #exit(0)
            coord_bs_interferer  = [bs_inter.coord_x + 0.0, bs_inter.coord_y + 0.0, bs_inter.coord_z + 0.0]                     #Get the coord of this serving bs
            direction_vec_2 = [self.coord_x - bs_inter.coord_x, self.coord_y - bs_inter.coord_y, self.coord_z - bs_inter. coord_z ]               #Calculate direction vector 
            #print(direction_vec_2)
            ray1 = np.array([coord_bs, direction_vec_1])      #Ray from the BS
            ray2 = np.array([coord_bs_interferer, direction_vec_2])     #Ray from the User
            cosang = np.dot(direction_vec_1, direction_vec_2)
            sinang = la.norm(np.cross(direction_vec_1, direction_vec_2))
            angle = np.arctan2(sinang, cosang)
            #print(angle*180/np.pi)
            self.theta_list.append(angle)
        #print(self.theta_list)
        #print('3.2')   
        '''For now the BS and UE beamwidth angle is given in netcfg.py - I think this value should be passed when the user calls the itf milli function in line 742'''
        total_inter = 0       # total interference intialized to 0
        beamwidth_bs = netcfg.theta_bs; beamwidth_ue = netcfg.theta_ue 
        Gmax_bs = netcfg.Gmax_bs; Gmin_bs = netcfg.Gmin_bs; Gmax_ue = netcfg.Gmax_ue; Gmin_ue = netcfg.Gmin_ue
        inter = 0#interferences intialized to zero
        #print('3.3')
        #print(self.theta_list)
        for theta in self.theta_list:                        # loop over the theta in the theta list 
            #print(theta)
            if abs(theta) <= beamwidth_bs:         # if the angle of antennas in boresight direction is less than beamwidth of main lobe of BS,           
                if abs(theta) <= beamwidth_ue:     # we also check if the angle of antenna in boresight direction is less than beamwidth of main lobe of UE, 
                    '''We need to work on the max and min gain too... This is just a framework'''
                    #print('Gmax BS,Gmax UE')
                    inter = self.inter(Gmax_bs,Gmax_ue)         # if yes, we calculate interference based on max gain values for BS and UE              # the return value is stored in inter
                    
                else:
                   # print('Gmax BS, Gmin UE')
                    inter = self.inter(Gmax_bs,Gmin_ue)         # if not, we calculate interference based on max gain for BS but min gain value for UE   # the return value is stored in inter
                    
        
            elif abs(theta) > beamwidth_bs:        # if the angle of antennas in boresight direction is greater than beamwidth of main lobe of BS,      
                if abs(theta) <= beamwidth_ue:     # we check if the angle of antenna in boresight direction is less than beamwidth of main lobe of UE, 
                   # print('Gmin BS, Gmax UE')
                    inter = self.inter(Gmin_bs,Gmax_ue)         # if yes, we calculate interference based on min gain for BS and max gain for UE
                    
                else:
                   # print('Gmin BS, Gmin UE')
                    inter = self.inter(Gmin_bs,Gmin_ue)         #if not, we calculate interference based on min gain for both BS and UE
                    
            total_inter = total_inter + inter        # returned inter value after each theta is added to total inter
        #print('3.4')
        #print('total interference',total_inter)
        #print(total_inter)
        #print('3 end')
        return total_inter
        
        
    def inter(self,gain_1,gain_2):
        '''Calculate interference based on the gain '''
        #print(gain_1,'...',gain_2)
        #print('4 start')
        los_inter = 0
        #print(self.interfering_bs)
        for bs in self.interfering_bs:
            freq = netcfg.freq['milli']
            free_space_path_loss = netcfg.constant * ((freq*1e9)**2)
            for dist in self.dist_inter_bs_list:        #looping over bs in interference list (based on distance list)
                path_loss_exponent = dist ** netcfg.alpha_nlos
                loss = free_space_path_loss * path_loss_exponent
                tsmt_pwr = netcfg.tsmt_pwr['milli']
                '''We need to use the gain passed after the if loop here to get the received power.....'''
                rxd_pwr_los_inter = tsmt_pwr *1e-3 * gain_1 * gain_2 / loss        
                los_inter = los_inter + rxd_pwr_los_inter 
  
        self.rxd_pwr_los_inter.append(los_inter) #Interference - it is a list   
        #print(self.rxd_pwr_los_inter)  
        inter = sum(self.rxd_pwr_los_inter) 
     #   print('inter',inter,'\n')
        #print('4 end')
        return inter

    def calc_itf_tera(self):  
        '''Interference in THz '''
        pass

    
    
    def calc_rxd_pwr(self,name_band):
        ''' Calculate Interference for Microwave band'''
        #print('5 start')
        freq = netcfg.freq[name_band]
        free_space_path_loss = netcfg.constant * ((freq*1e9)**2)
        #print('name band',name_band)
        #xit(0)
        if name_band == 'micro':
            if self.is_blocked is False:
                '''rxd power if the serving bs is in los'''
                path_loss_exponent = self.dist_serving_bs ** netcfg.alpha_los
                loss_los = free_space_path_loss * path_loss_exponent
                tsmt_pwr = netcfg.tsmt_pwr[name_band]
                rxd_pwr = tsmt_pwr *1e-3 / loss_los
            else:
                '''rxd power if the serving bs is in nlos'''
                path_loss_exponent = self.dist_serving_bs ** netcfg.alpha_nlos
                loss_los = free_space_path_loss * netcfg.abs_coeff**sum(self.count_blk_serving)*path_loss_exponent   
                tsmt_pwr = netcfg.tsmt_pwr[name_band]
                rxd_pwr = tsmt_pwr *1e-3 / loss_los
        elif name_band == 'milli':
            if self.is_blocked is False:
                path_loss_exponent = self.dist_serving_bs ** netcfg.alpha_los
                loss_los = free_space_path_loss * path_loss_exponent
                tsmt_pwr = netcfg.tsmt_pwr[name_band]
                rxd_pwr = tsmt_pwr *1e-3 *netcfg.Gmax_bs *netcfg.Gmax_ue/ loss_los
            else:
                '''rxd power if the serving bs is in nlos'''
                path_loss_exponent = self.dist_serving_bs ** netcfg.alpha_nlos
                loss_los = free_space_path_loss * netcfg.abs_coeff**sum(self.count_blk_serving)*path_loss_exponent   
                tsmt_pwr = netcfg.tsmt_pwr[name_band]
                rxd_pwr = tsmt_pwr *1e-3 *netcfg.Gmax_bs *netcfg.Gmax_ue / loss_los
                
        elif name_band == 'tera':
            if self.is_blocked is False:
                path_loss_exponent = self.dist_serving_bs ** netcfg.alpha_los
                loss_los = free_space_path_loss * path_loss_exponent
                tsmt_pwr = netcfg.tsmt_pwr[name_band]
                rxd_pwr = tsmt_pwr *1e-3 *netcfg.Gmax_bs_tera *netcfg.Gmax_ue_tera/ loss_los
      
        
        self.rxd_pwr_serving.append(rxd_pwr)
            
        serv_pwr = sum(self.rxd_pwr_serving)                    #Get the rxd power of the serving bs from the list(it is just a single element) 
        #print(serv_pwr)
        #print('5 end')
        return serv_pwr
         

    def blk_detection_backup(self):
        '''Check if this node has a blockage in its path'''
        
        
        bs_list = self.ntwk.get_node_list(net_name.lte_bs)
        #print(interfering_bs_list)
        #exit()
        nlos_inter_bs_list = []
        los_inter_bs_list = []
        coord_usr = [self.coord_x +0.0, self.coord_y+0.0, self.coord_z+0.0]          
        for bs_interferer in bs_list:
            bs_inter = self.get_netelmt(bs_interferer)                              #Get the obj of this nodes serving bs (here bs is object)
            coord_bs_interferer  = [bs_inter.coord_x + 0.0, bs_inter.coord_y + 0.0, bs_inter.coord_z + 0.0]                     #Get the coord of this serving bs
            direction_vec_3 = [self.coord_x - bs_inter.coord_x, self.coord_y - bs_inter.coord_y, self.coord_z - bs_inter. coord_z]                  #Calculate direction vector 
            direction_vec_4 = [bs_inter.coord_x - self.coord_x , bs_inter.coord_y - self.coord_y , bs_inter. coord_z - self.coord_z ]               #Calculate direction vector 
            #print (direction_vec_1,'\n')
            #print (direction_vec_2,'\n')
            ray3 = np.array([coord_bs_interferer, direction_vec_1])      #Ray from the BS
            ray4 = np.array([coord_usr, direction_vec_2])     #Ray from the User

            #print ('ray1',ray1)
            #print ('ray2',ray2) 
            # Step 3: Check if the user is blocked by any blockage
            
            # print(ray3)
            # print(ray4)
            
             
            list_blk = self.ntwk.get_node_list(net_name.blk) 
            blk_cnt = 0
        
            #print(list_blk)
            for blk in list_blk:
                blk_obj = self.get_netelmt(blk)
                #blk_obj.blk_aabb_box()
                #print('box',blk_obj.aabb)
            
                #print('r1,a',ray1, blk_obj.aabb)
                #print('r2,a',ray2, blk_obj.aabb)
                result_3 = gt.ray_intersect_aabb(ray3, blk_obj.aabb)
                #print('result3',result_3,'\n')
            
                result_4 = gt.ray_intersect_aabb(ray4, blk_obj.aabb)
                #print('result4',result_4,'\n')
                
                if not result_3 is None and not result_4 is None:
                        blk_cnt += 1  
                else:
                        pass
            
            
            
            
            if blk_cnt == 0:
                self.interfering_bs_los.append(bs_interferer)    
            else:
                self.interfering_bs_nlos.append(bs_interferer)
                self.count_blk.append(blk_cnt)
                
               
        
        
class wifi_sta(net_node.node):
    '''
    Definition of the wifi station
    '''
    def __init__(self, net_info):      
        # from base network element
        net_node.node.__init__(self, net_info) 
        
        # set the initial status to 'on'
        self.set_status(net_name.on)
        
    def set_status(self, status = net_name.on):
        '''
        Set the status of a wifi station: on or off
        status: The status of a network element, on or off
        '''
        if status == net_name.on:
            if self.name not in self.ntwk.list_active_wifi_sta:
                self.ntwk.list_active_wifi_sta.append(self.name)
                print('{} is set on.'.format(self.name))
            else:
                print('Warning: {} is already active.'.format(self.name))
        elif status == net_name.off: 
            if self.name in self.ntwk.list_active_wifi_sta:
                self.ntwk.list_active_wifi_sta.remove(self.name)
                print('{} is set off.'.format(self.name))
            else:
                print('Warning: {} is already inactive.'.format(self.name))
        else:
            print('Errror: Unsupported network node status.')
            exit(0)
        

class wifi_ap(net_node.wifi_sta):
    '''
    Definition of the wifi access point
    '''
    def __init__(self, net_info):      
        # from base network element
        net_node.wifi_sta.__init__(self, net_info) 


class wifi_usr(net_node.wifi_sta):
    '''
    Definition of the wifi user
    '''
    def __init__(self, net_info):      
        # from base network element
        net_node.wifi_sta.__init__(self, net_info)    


# Define the blockage class here
class blk(net_node.node):
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
        self.x = random.randint(0, self.ntwk.net_width)
        self.y = random.randint(0, self.ntwk.net_width)
        self.z = random.randint(0, self.ntwk.net_width)
		
		# Add the node location to the list of all nodes in the network
        # to maintain the information of the full list of nodes in the network
        self.ntwk.axis_x.append(self.x)                     
        self.ntwk.axis_y.append(self.y)
        self.ntwk.axis_z.append(self.z) 
	
		
        #Initializing the dimensions, in meter
        # should be generated following certain distribution, do this here
        self.l = random.randint(netcfg.min_blk_dim, netcfg.max_blk_dim)
        self.w = random.randint(netcfg.min_blk_dim, netcfg.max_blk_dim)
        self.h = random.randint(netcfg.min_blk_dim, netcfg.max_blk_dim)
		
		# Add the node dimension to the list of all nodes in the network
        # to maintain the information of the full list of nodes in the network
        self.ntwk.dim_l.append(self.l)                     
        self.ntwk.dim_w.append(self.w)
        self.ntwk.dim_h.append(self.h) 
        
        self.aabb = self.blk_aabb_box()
        
        #print('{} registered.'.format(self.name))
        
    def ping(self):
        net_func.netelmt_group.ping()      

    
    def blk_aabb_box(self):
     
        coord_blk = [self.x+0.00001, self.y+0.00001, self.z+0.00001] 
        dim_blk = [self.l, self.w, self.h]   
        
        box_min = coord_blk
        box_max = [self.x +0.00001 + self.l, self.y +0.00001 + self.w, self.z +0.00001 + self.h]
        #print('box min', box_min)
        #print('dim blk', dim_blk)
        #print('box max', box_max)
       
        aabb = np.array([box_min,box_max])
        
        #print('aabb', aabb)
        
        return aabb
        
   
        
        
    
        