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

import numpy as np

import ESN_training

def esn_data_prep(data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17, data18):
    '''
    data1= distance_data, data2= var_tr_xyz_1, data3= var_rx_xyz_1, data4= var_tr_rpy_1, data5= var_rx_rpy_1, data6= var_tr_xyz_2, data7= var_rx_xyz_2, data8= var_tr_rpy_2, data9= var_rx_rpy_2,\
    data10= mean_tr_xyz_1, data11 mean_rx_xyz_1, data12= mean_tr_rpy_1, data13= mean_rx_rpy_1, data14= mean_tr_xyz_2, data15= mean_rx_xyz_2, data16= mean_tr_rpy_2, data17= mean_rx_rpy_2, data18= optimal_angle
    '''
    final_data_for_esn = np.array([])
    column_1_distance = data1
    #print('A', column_1_distance)
    #print(column_1_distance.shape[0])
    rep_ind_1 = column_1_distance.shape[0]
    #print('B', rep_ind_1)
    
    rep_ind_2 = int(rep_ind_1/2)
    
    column_2_avg_tr_xyz = np.repeat(data2, rep_ind_2)
    #print('C', column_2_avg_tr_xyz)
    column_3_avg_rx_xyz = np.repeat(data3, rep_ind_2)
    #print('D', column_3_avg_rx_xyz)
    column_4_avg_tr_rpy = np.repeat(data4, rep_ind_2)
    #print('E', column_4_avg_tr_rpy)
    column_5_avg_rx_rpy = np.repeat(data5, rep_ind_2)
    #print('F', column_5_avg_rx_rpy)
    
    column_6_var_tr_xyz = np.repeat(data6, rep_ind_2)
    #print('G', column_6_var_tr_xyz)
    column_7_var_rx_xyz = np.repeat(data7, rep_ind_2)
    #print('H', column_7_var_rx_xyz)
    column_8_var_tr_rpy = np.repeat(data8, rep_ind_2)
    #print('I', column_8_var_tr_rpy)
    column_9_var_rx_rpy = np.repeat(data9, rep_ind_2)
    #print('J', column_9_var_rx_rpy)    
    
    column_10_avg_tr_xyz = np.repeat(data10, rep_ind_2)
    #print('K', column_10_avg_tr_xyz)
    column_11_avg_rx_xyz = np.repeat(data11, rep_ind_2)
    #print('L', column_11_avg_rx_xyz)
    column_12_avg_tr_rpy = np.repeat(data12, rep_ind_2)
    #print('M', column_12_avg_tr_rpy)
    column_13_avg_rx_rpy = np.repeat(data13, rep_ind_2)
    #print('N', column_13_avg_rx_rpy)
    
    column_14_var_tr_xyz = np.repeat(data14, rep_ind_2)
    #print('O', column_14_var_tr_xyz)
    column_15_var_rx_xyz = np.repeat(data15, rep_ind_2)
    #print('P', column_15_var_rx_xyz)  
    column_16_var_tr_rpy = np.repeat(data16, rep_ind_2)
    #print('Q', column_16_var_tr_rpy)
    column_17_var_rx_rpy = np.repeat(data17, rep_ind_2)
    #print('R', column_17_var_rx_rpy)
    
    column_2_10_var_tr_xyz = np.concatenate((column_2_avg_tr_xyz, column_10_avg_tr_xyz))
    column_3_11_var_rx_xyz = np.concatenate((column_3_avg_rx_xyz, column_11_avg_rx_xyz))
    column_4_12_var_tr_rpy = np.concatenate((column_4_avg_tr_rpy, column_12_avg_tr_rpy))
    column_5_13_var_rx_rpy = np.concatenate((column_5_avg_rx_rpy, column_13_avg_rx_rpy))
    
    column_6_14_avg_tr_xyz = np.concatenate((column_6_var_tr_xyz, column_14_var_tr_xyz))
    column_7_15_avg_rx_xyz = np.concatenate((column_7_var_rx_xyz, column_15_var_rx_xyz))
    column_8_16_avg_tr_rpy = np.concatenate((column_8_var_tr_rpy, column_16_var_tr_rpy))
    column_9_17_avg_rx_rpy = np.concatenate((column_9_var_rx_rpy, column_17_var_rx_rpy))
    
    
    column_18_opt_ang = data18
    #print(column_18_opt_ang)
    
    column_one = np.repeat(1, rep_ind_1)
    
    final_data_for_esn = column_one
    final_data_for_esn = np.vstack((final_data_for_esn, column_1_distance))
    final_data_for_esn = np.vstack((final_data_for_esn, column_2_10_var_tr_xyz))
    final_data_for_esn = np.vstack((final_data_for_esn, column_3_11_var_rx_xyz))
    final_data_for_esn = np.vstack((final_data_for_esn, column_4_12_var_tr_rpy))
    final_data_for_esn = np.vstack((final_data_for_esn, column_5_13_var_rx_rpy))
    final_data_for_esn = np.vstack((final_data_for_esn, column_6_14_avg_tr_xyz))
    final_data_for_esn = np.vstack((final_data_for_esn, column_7_15_avg_rx_xyz))
    final_data_for_esn = np.vstack((final_data_for_esn, column_8_16_avg_tr_rpy))
    final_data_for_esn = np.vstack((final_data_for_esn, column_9_17_avg_rx_rpy))
    final_data_for_esn = np.vstack((final_data_for_esn, column_18_opt_ang))
    #print(final_data_for_esn)
    final_data_for_esn = np.transpose(final_data_for_esn)
    
    #print(final_data_for_esn)
    #exit()
    angles = ESN_training.ESN_train(final_data_for_esn)
    
    return angles