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
import net_name, net_func, net_node, netcfg, net_channel

# Antenna model
import antmdl

import random, math

import flytera_cfg

import numpy as np

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
        #print('Adding '+node_type+'...')
        
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
            addi_info = {'ntwk':self.ntwk, 'parent':self, 'node_id': node_id}
            info = net_func.mkinfo(elmt_name, elmt_type, elmt_num, addi_info)

            # create node object            
            def_class = getattr(net_node, node_type)    # first, get the defining class for the node type
            node_obj  = def_class(info)                 # second, create the node object   
            #node_obj  = net_node.node(info)

            # add the node to the corresponding group
            self.addmember(elmt_name)
            # self.ping()
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
        
        # record node id within the group, starting from 1
        self.ingroup_id = net_info['addi_info']['node_id']         
        
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
            
            # # Transmission 
            # print(self.type + ': Start transmitting at %d' % env.now)           
            # yield env.timeout(netcfg.wifi_tsmt_time_tick)        
        
    def get_coord(self):
        '''
        Func: get the current coordinates of the node
        return: the x-, y- and z- coordinates 
        '''
       
        return {'x':self.coord_x, 'y': self.coord_y, 'z':self.coord_z}
    
    def set_coord(self, dict_xyz):
        '''
        Func: Set the coordinates of the node       
        '''
        # update coordinate information of this node
        self.coord_x = dict_xyz['x']
        self.coord_y = dict_xyz['y']
        self.coord_z = dict_xyz['z']
        
        # update the information recorded in the network
        self.ntwk.axis_x[self.ntwk_wide_index] = self.coord_x
        self.ntwk.axis_y[self.ntwk_wide_index] = self.coord_y
        self.ntwk.axis_z[self.ntwk_wide_index] = self.coord_z
        
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
            print('{} registered.'.format(self.name))

        
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

class dhs(net_node.node):
    '''
    Definition of drone hotspot
    '''
    def __init__(self, net_info):      
        # from base network element
        net_node.node.__init__(self, net_info) 
        
        # Is this node a transmitter or receiver
        self.is_tsmt = None
        self.is_rcvr = None
        
        # Set the dhs as transmitter or receiver according to the ingroup id
        if self.ingroup_id == 1:
            self.ntwk.tsmt = self     # First dhs, set as transmitter
            self.is_tsmt = True 
        elif self.ingroup_id == 2:
            self.ntwk.rcvr = self     # Second dhs, set as receiver
            self.is_rcvr = True
        else:
            print('Error: This experiment requires two dhs only.')
            exit(0)
               
        # Initialize coordinates of the dhs
        self.ini_coord()
        
        # Gyroscope trace and sampling rate
        gyr, smpl_rate = self.set_gyr() 
        self.gyr = gyr                      # gyr trace
        self.gyr_len = self.gyr.shape[0]    # Total number samples         
        self.smpl_rate = smpl_rate          # Sampling rate
        self.smpl_itvl = 1/self.smpl_rate   # Sampling interval
        self.set_bandwidth()
        self.set_noise()
        #print(self.smpl_itvl)
        # print(self.gyr)
        # print(self.gyr.shape[0])
        # print(self.smpl_itvl)
        # exit(0)
        
        # Trace of linear acceleration measurement. No need to return sampling rate for laac, use the same as gyr's
        self.laac = self.set_laac()
                        
        # Velocity of roll, pitch, yaw of the dhs, in angular degree, updated as the network runs
        self.time       = 0
        self.roll_vel   = 0
        self.pitch_vel  = 0
        self.yaw_vel    = 0
        
        # Absolute roll, pitch, yaw, updated in each tick
        self.roll   = 0     
        self.pitch  = 0
        self.yaw    = 0
                       
        # Velocity at x-, y- and z-axis, updated in each tick
        self.vel_x = 0
        self.vel_y = 0
        self.vel_z = 0                   
        
        # Antenna model: cone model
        self.ant_mdl = antmdl.cone_mdl()
        
    def set_laac(self):
        '''
        Set the laac trace for this node
        '''
        # Get the trace id name
        trace_id =  flytera_cfg.lac_trace_id[self.ingroup_id-1]     # ingroup_id starts from 1
        # There are only four sets of data for micro- and small-scale mobility
        # No measurements for large-scale mobility, in which case the laac data will be generated randomly
        trace_name = flytera_cfg.lac_trace_name_new[trace_id] 
        trace = flytera_cfg.dhs_new_trace[trace_name]
        
        # if trace_id in [0, 1]:      # Micro-scale movemenent 
            # # Measured trace     
            # trace_name = flytera_cfg.lac_trace_name_new[trace_id] 
            # trace = flytera_cfg.dhs_new_trace[trace_name]
        # elif trace_id in [2, 3]:    # Small-scale movement
            # # Generated trace
            # # self.gry_len: the same number of lines as the gyroscope measurement
            # # 4 columns: sampling time, x-, y-, z-axis laac
            # trace = np.random.standard_normal((self.gyr_len, 4))                       
        # elif trace_id in [4, 5]:   
            # # Large-scale movement. In flytera_cfg, large-scale measurements are stored in lac_small_1000_inst1.
            # trace_name = flytera_cfg.lac_trace_name_new[trace_id - 2] 
            # trace = flytera_cfg.dhs_new_trace[trace_name]            
        # else:
            # print('Error: Trace id must in [0, 1, 2, 3, 4, 5]')
            # exit(0)
            
        #print(trace)
        # exit(0)
        return trace
                
    def set_gyr(self):
        '''
        Set the gyroscope trace for this dhs
        '''     
                
        # Get the trace id name
        trace_id = flytera_cfg.gry_trace_id[self.ingroup_id-1]      #ingroup_id starts from 1
        trace_name = flytera_cfg.gry_trace_name_new[trace_id]       
        
        # Get the variable with variable name
        trace = flytera_cfg.dhs_new_trace[trace_name]
        
        # Sampling rate
        sampl_rate = flytera_cfg.gry_trace_smpl_rate[trace_id]
        
        return trace, sampl_rate
    
    def set_bandwidth(self):
        '''set the transmission bandwidth'''
        self.oper_freq = flytera_cfg.oper_freq
        data = flytera_cfg.const_data[self.oper_freq]
        self.bandwidth = data[0]
        self.frequency = data[1]
 
        
    def set_noise(self):
        '''set the noise based on the frequency of txn'''
        bandw = self.bandwidth
        noise_thermal_dB = -174 + (10 * np.log10(bandw *10**6)) + netcfg.noise_figure
        self.noise = 10**(noise_thermal_dB/10)

        
    def ini_coord(self):
        '''
        Initialize the coordinates for this dhs based on configuration in flytera_cfg.py
        '''        
        # print(flytera_cfg.ini_axis_x.size)
        # exit(0)
        
        # Check if the initial axis has not been defined for this node 
        if self.ingroup_id > flytera_cfg.ini_axis_x.size:
            # Not defined
            print('Error: The initial axis is not defined for {}'.format(self.name))
            exit(0)
        else:
            # Defined, initialize the coordinates
            x = flytera_cfg.ini_axis_x[0, self.ingroup_id - 1]
            y = flytera_cfg.ini_axis_y[0, self.ingroup_id - 1]
            z = flytera_cfg.ini_axis_z[0, self.ingroup_id - 1]
            
            # Update the node and network
            dict_xyz = {'x':x, 'y':y, 'z':z}            
            self.set_coord(dict_xyz)                     
        
        # print(self.coord_x, self.coord_y, self.coord_z)
        # print(self.ntwk.axis_x)
        # print(self.ntwk.axis_y)
        # print(self.ntwk.axis_z)
        # exit(0)
        
    def operation(self, env):
        '''
        test function
        '''
        meas_idx = 0        # measurement index, starting from 0
        while True:
            # Sampling time
            self.time       =  self.gyr[meas_idx, 0]
            
            # Sampled roll, pitch, yaw
            self.roll_vel   =  self.gyr[meas_idx, -3]
            self.pitch_vel  =  self.gyr[meas_idx, -2]
            self.yaw_vel    =  self.gyr[meas_idx, -1]
            
            # Sampled laac in x-, y-, and z-axis
            laac_x          =  self.laac[meas_idx, -3]
            laac_y          =  self.laac[meas_idx, -2]
            laac_z          =  self.laac[meas_idx, -1]
                       
            # move to the next measurement 
            meas_idx += 1
            
            # If already the last measurement, stay there
            meas_idx = min(meas_idx, self.gyr_len-1) 
            
            # Update the absolute roll, pitch, yaw based on this tick
            self.roll   += self.roll_vel * self.smpl_itvl
            self.pitch  += self.pitch_vel * self.smpl_itvl
            self.yaw    += self.yaw_vel * self.smpl_itvl
                       
            # Update coordinates, this should be done before updating velocity
            x = self.coord_x + self.vel_x * self.smpl_itvl + 0.5 * laac_x * math.pow(self.smpl_itvl, 2)
            y = self.coord_y + self.vel_y * self.smpl_itvl + 0.5 * laac_y * math.pow(self.smpl_itvl, 2)
            z = self.coord_z + self.vel_z * self.smpl_itvl + 0.5 * laac_z * math.pow(self.smpl_itvl, 2)
            
            # Update coordiantes in the network coordinate matrix
            xyz = {'x':x, 'y':y, 'z':z}
            self.set_coord(xyz)            
            
            # Update velocity with acceleration velocity in this tick, for use in the next tick
            self.vel_x  += laac_x * self.smpl_itvl
            self.vel_y  += laac_y * self.smpl_itvl
            self.vel_z  += laac_z * self.smpl_itvl            
            
            # If this node is the transmitter, the coordinates are assumed to be at the origon 
            # Given beamwidth, the wavefront is a circle with radius depending only on the communication distance
            

            # print('Time:', self.time)
            # print(self.name + '(roll, pitch, yaw): ({}, {}, {})'.format(self.roll, self.pitch, self.yaw)) 
            # print(self.name + '(vel_x, vel_y, vel_z): ({}, {}, {})'.format(self.vel_x, self.vel_y, self.vel_z)) 
            yield env.timeout(1)
            
    def updt_tsmt_wavefront(self):
        '''
        Update the wavefront of the transmitter. 
        '''
        
        # This node must be a transmitter
        if self.is_tsmt == False:
            print('Error: updt_tsmt_wavefront() supported by only transmitter.')
            exit(0)
        
        #print('Commun. dist:', self.ntwk.comm_dist)
        
        # The wavefront of the transmitter is a circle in xy-plane, centered at (x=0, y=0). The radius can be calcuulated
        # with given beamwidth and communication distance 
        
        # First calculate radius of the circle
        #print('inside angle', flytera_cfg.angle)
        radius = math.tan(flytera_cfg.angle/180 * math.pi) * self.ntwk.comm_dist
        #print('inside rad', radius)
        # exit(0)
        
        # Information of the wavefront circle 
        info = {'center':(0, 0), 'semi_xy':(radius, radius), 'angle': 0}
        
        # Get the polygon of the transmitter
        self.ant_mdl.polygon = self.ant_mdl.get_polygon(info)
        # print(self.ant_mdl.polygon)
        # exit(0)
        
        return radius
        
    def updt_rcv_area(self):
        '''
        Update the receive area of the receiver. 
        '''
        
        # This node must be a receiver
        if self.is_rcvr == False:
            print('updt_rcv_area() supported by only receiver.')
            exit(0)
            
        # center of the receive circle
        center = (self.ntwk.x_rel_adj, self.ntwk.y_rel_adj)
        # print(center)
        
        # calculate the semi-axis of the ellipse
        semi_x = flytera_cfg.radius * math.cos(self.ntwk.roll_rel_adj)        
        semi_y = flytera_cfg.radius * math.cos(self.ntwk.pitch_rel_adj)   
        
        # rotation of the ellipse
        rotation = self.ntwk.yaw_rel_adj * 180

        # Information of the wavefront circle 
        info = {'center':center, 'semi_xy':(semi_x, semi_y), 'angle': rotation}
        
        # Update the polygon of the receiver
        self.ant_mdl.polygon = self.ant_mdl.get_polygon(info)
        
        rx_area = np.pi * semi_x * semi_y
        self.rx_area = rx_area
        #print(rx_area)
        
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