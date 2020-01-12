import numpy as np

import ESN_training

def esn_data_prep(data1, data2, data3, data4, data5, data6, data7, data8, data9, data10):
    '''
    data1 - distance, data2 - avg tr xyz, data3 - avg rx xyz, data4 - avg tr rpy, data5 - avg rx rpy,
    data6 - var tr xyz,data7 - var rx xyz data8 - var tr rpy, data9 - var rx rpy, data10 - optimal angle
    '''
    final_data_for_esn = np.array([])
    column_1_distance = data1
    #print(column_1_distance)
    #print(column_1_distance.shape[0])
    rep_ind = column_1_distance.shape[0]
    column_2_avg_tr_xyz = np.repeat(data2, rep_ind)
    #print(column_2_avg_tr_xyz)
    column_3_avg_rx_xyz = np.repeat(data3, rep_ind)
    #print(column_3_avg_rx_xyz)
    column_4_avg_tr_rpy = np.repeat(data4, rep_ind)
    #print(column_4_avg_tr_rpy)
    column_5_avg_rx_rpy = np.repeat(data5, rep_ind)
    #print(column_5_avg_rx_rpy)
    column_6_var_tr_xyz = np.repeat(data6, rep_ind)
    #print(column_6_var_tr_xyz)
    column_7_var_rx_xyz = np.repeat(data7, rep_ind)
    #print(column_7_var_rx_xyz)
    column_8_var_tr_rpy = np.repeat(data8, rep_ind)
    #print(column_8_var_tr_rpy)
    column_9_var_rx_rpy = np.repeat(data9, rep_ind)
    #print(column_9_var_rx_rpy)
    column_10_opt_ang = data10
    #print(column_10_opt_ang)
    column_one = np.repeat(1, rep_ind)
    
    final_data_for_esn = column_one
    final_data_for_esn = np.vstack((final_data_for_esn, column_1_distance))
    final_data_for_esn = np.vstack((final_data_for_esn, column_2_avg_tr_xyz))
    final_data_for_esn = np.vstack((final_data_for_esn, column_3_avg_rx_xyz))
    final_data_for_esn = np.vstack((final_data_for_esn, column_4_avg_tr_rpy))
    final_data_for_esn = np.vstack((final_data_for_esn, column_5_avg_rx_rpy))
    final_data_for_esn = np.vstack((final_data_for_esn, column_6_var_tr_xyz))
    final_data_for_esn = np.vstack((final_data_for_esn, column_7_var_rx_xyz))
    final_data_for_esn = np.vstack((final_data_for_esn, column_8_var_tr_rpy))
    final_data_for_esn = np.vstack((final_data_for_esn, column_9_var_rx_rpy))
    final_data_for_esn = np.vstack((final_data_for_esn, column_10_opt_ang))
    #print(final_data_for_esn)
    final_data_for_esn = np.transpose(final_data_for_esn)
    
    #print(final_data_for_esn)
    
    angles = ESN_training.ESN_train(final_data_for_esn)
    
    return angles