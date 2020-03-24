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

# #######################################################
# ## Date: 06/30/2019
# ## Author: Zhangyu Guan
# ## Network control and optimization module
# #######################################################

# Sabarish, the learning algorithms go here

# import definitions of network elements 
import net_ntwk
import net_name, net_channel

# network configuration
import netcfg

# discrete simulations
import simpy, numpy as np
import random
import sys, os
os.system('cls')

import random

rate = []
coord = []

def ctl_operation(env, nt):
    
    i=1
    while True:
        list =[]
        print('Iteration Number',i) 
        for bs_name in nt.list_lte_bs:
            #list=[]
            #print('a',bs_name)
            bs_obj = nt.get_netelmt(bs_name)
            #print(bs_obj.__dict__)
            #print('b',bs_obj.served_user)
            name = bs_obj.name
            #print(name)
            list.append(name)
            #sheet1.write(0, a, name) 
            #a+=1
            x_coord = bs_obj.coord_x
            #print(x_coord)
            list.append(x_coord)
            #sheet1.write(1, b, x_coord)
            #b+=1
            y_coord = bs_obj.coord_y
            list.append(y_coord)
            #sheet1.write(2, c, y_coord)
            #c+=1
            z_coord = bs_obj.coord_z
            list.append(z_coord)
            #sheet1.write(3, d, z_coord)
            #d+=1
            if bs_name not in nt.list_lte_bs_mobile:
                bs_obj = nt.get_netelmt(bs_name)
                #print('v',bs_obj.served_user)
                #bs_name_obj = nt.get_netelmt(bs_name) 
                #print(bs_obj_mobile.__dict__)
                rate_list = []
                for serv_usr in bs_obj.served_user:
                    serv_usr_obj = nt.get_netelmt(serv_usr) 
                    #print(bs_name)
                   # print(serv_usr)
                    #print(serv_usr_obj.oper_freq)
                    #rate_1 = 0;rate_2 = 0; rate_3 = 0
                    sinr = serv_usr_obj.sinr
                    if serv_usr_obj.oper_freq == 'micro':
                        rate = serv_usr_obj.rate
                        #print('a',sinr,'...',rate)
                    elif serv_usr_obj.oper_freq == 'milli': 
                        rate = netcfg.milli_bandwidth * np.log2(1 + sinr)
                        #print('b',sinr,'...',rate)
                    else:
                        rate = netcfg.tera_bandwidth * np.log2(1 + sinr)
                        #print('c',sinr,'...',rate)   
                    rate_list.append(rate)
                    #print(rate_list)
                #print('a',rate_list)
                rate = sum(rate_list)
                #print('b',rate)
                if rate == 0:
                    list.append(0.00001)
                else:
                    list.append(rate)
            
            if bs_name in nt.list_lte_bs_mobile:
                #print(bs_name)
                bs_name_obj = nt.get_netelmt(bs_name) 
                bs_obj_mobile = nt.get_netelmt(bs_name)
                #print('w',bs_obj_mobile.served_user)
                rate_mbs = bs_name_obj.rate
                #print(bs_obj.__dict__)
                rate_list = []
                sum_rate = 0
                #print(bs_obj.served_user)
                for serv_usr in bs_obj.served_user:
                    #print(len(bs_obj.served_user))
                    serv_usr_obj = nt.get_netelmt(serv_usr) 
                    #print(bs_name)
                    #print(serv_usr)
                    #print(serv_usr_obj.oper_freq)
                    #rate_1 = 0;rate_2 = 0; rate_3 = 0
                    sinr = serv_usr_obj.sinr
                    if serv_usr_obj.oper_freq == 'micro':
                        rate = serv_usr_obj.rate
                        #print('a',rate)
                    elif serv_usr_obj.oper_freq == 'milli': 
                        rate = netcfg.milli_bandwidth * np.log2(1 + sinr)
                        #print('b',rate)
                    else:
                        rate = netcfg.tera_bandwidth * np.log2(1 + sinr)
                        #print('c',rate) 
                    sum_rate = sum_rate + rate
                #print('sum rate of all users', sum_rate)
                #print('back haul rate',rate_mbs)
                #print('sum rate',sum_rate)
                rate = min(rate_mbs,sum_rate)
                #print('minimum rate', rate)
                # actual_rate = rate/len(bs_obj.served_user)
                # #print(actual_rate)
                # for serv_usr in bs_obj.served_user:
                    # serv_usr_obj.rate = actual_rate
                    # rate_list.append(actual_rate)
                    # #print(rate_list)
                   # # print('a',rate_list)
                # rate = sum(rate_list)
                # #print('mbs rate',rate_mbs)
                # #print('before min',rate)
                # #rate = min(rate_mbs,rate)
                # #print('after min',rate)
                # #print(bs_name,'------',rate)
                if rate == 0:
                    list.append(0.00001)
                else:
                    list.append(rate)
                #print(list)
                #sheet1.write(4, e, num_of_users)
                #e+=1
                current_coord = bs_obj.get_coord()
                new_coord = current_coord
                #print(new_coord)
                #print('aaaaaa',new_coord['x'],'...',new_coord['y'],'...',new_coord['z'])
                new_coord['x'] = new_coord['x'] + random.randint(-15, 15)
                new_coord['y'] = new_coord['y'] + random.randint(-15, 15)
                new_coord['z'] = new_coord['z'] + random.randint(-15, 15)
                #print('bbbbb',new_coord['x'],'...',new_coord['y'],'...',new_coord['z'])
                new_coord['x'] = min(new_coord['x'], netcfg.area_x-random.randint(5, 10)) #* netcfg.num_pixel_per_meter)
                new_coord['y'] = min(new_coord['y'], netcfg.area_y-random.randint(5, 10)) #* netcfg.num_pixel_per_meter)
                new_coord['z'] = min(new_coord['z'], netcfg.area_z-random.randint(5, 10))# * netcfg.num_pixel_per_meter)
                #print('ccccc',new_coord['x'],'...',new_coord['y'],'...',new_coord['z'])
                new_coord['x'] = max(new_coord['x'], 0+random.randint(5, 10))
                new_coord['y'] = max(new_coord['y'], 0+random.randint(5, 10))
                new_coord['z'] = max(new_coord['z'], 0+random.randint(5, 10))
                #print('ddddd',new_coord['x'],'...',new_coord['y'],'...',new_coord['z'])
                #print(new_coord)
                bs_obj.set_coord(new_coord)
                
                nt.ini_dist()                  
                nt.update_association()
                nt.updt_band_association()
                nt.update_association_mbs_bs_link()
                bs_obj.sinr_calc_mbs()
                for user in nt.get_node_list(net_name.lte_ue):
                    #print('1')
                    user_obj = nt.get_netelmt(user)
                    #print('2')
                    user_obj.blk_detection()
                    #print('3')
                    user_obj.set_noise()
                    #print('4')
                    user_obj.sinr_calc()
                    #print('5')
            #print('\n')        
        #print(list)
        num_bs = netcfg.num_lte_bs + netcfg.num_lte_bs_mobile
        data_list = []
        
        a= 0
        for a in range(num_bs * 5):
            data_list.append(list[a])
        #print(data_list)
        
            
        b = 0
        num_bs = netcfg.num_lte_bs + netcfg.num_lte_bs_mobile
        coord_cur = []
        rate_cur = []
        rate_curr = np.array([])
        for b in range(num_bs):
            #print('data list',data_list)
            coord = data_list[1+(5*b):4+(5*b)]
            #print('xyz',coord)
            coord_cur.append(coord)
            #print(coord_cur)
            coord_curr = np.vstack((coord_cur))  

            #print('data list',data_list)
            rate = data_list[4+(5*b)]
            rate_curr = np.hstack((rate_curr,rate))
            #rate_curr = np.array([rate_curr])
            
        #print('cx',coord_curr)
        #print('rx',rate_curr)
        
        
        if i == 1:   
            coord_current = coord_curr
            rate_current = rate_curr
            #print('coord',coord)
            #print('rate', rate_current)
            
            
        else:
            coord_current = np.vstack((coord_current,coord_curr))
            rate_current = np.hstack((rate_current, rate_curr))
            #print('x', coord_current,'\n')
            #print('y', rate_current)
            #print(rate_current.shape)
        
        
        i+=1
        coord = coord_current
        rate = rate_current
        rate = np.array([rate])
        rate = np.transpose(rate)
        #print('cc',coord)
        #print('rr',rate)
        #print('xyz sh',rate.shape)
        #print('co sh', coord.shape)
        nt.rate = rate
        nt.coord = coord
        yield env.timeout(1)
        
        
        
        
































