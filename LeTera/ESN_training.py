from pyESN import ESN

import numpy as np

import flytera_cfg

from matplotlib import pyplot as pp

import beam_plot

def ESN_train(data):
    #print(data)
    total_col = data.shape[1]
    
    opt_ang_col = data[:, total_col-1]
    #print(opt_ang_col)
    
    max_angle = max(opt_ang_col)
    #print(max_angle)
    opt_ang_col = opt_ang_col/max_angle/2
    
    #print(opt_ang_col)
    
    opt_ang_col = np.transpose(opt_ang_col)
    
    #print(opt_ang_col)
    
    N=flytera_cfg.sim_tick
    
    rng = np.random.RandomState(42)   
    traintest_cutoff = int(np.ceil(0.9*N))
    train_data, train_data_angle = data[:traintest_cutoff], opt_ang_col[:traintest_cutoff]
    test_data, test_data_angle = data[traintest_cutoff:], opt_ang_col[traintest_cutoff:]
    #print('TEST DAtA ANGLE', test_data_angle)
    rows_zeros_ip_shift = np.zeros(total_col)
    #print('zeros', zeros)
    rows_ones_ip_scale = np.ones(total_col)
    
    esn = ESN(n_inputs=total_col,
              n_outputs=1,
              n_reservoir=50,
              spectral_radius=0.25,
              sparsity=0.25,
              noise=0.001,
              input_shift = rows_zeros_ip_shift,
              input_scaling = rows_ones_ip_scale,
              #input_scaling=[1, 1],
              teacher_scaling=0.4,
              #teacher_scaling=1,
              teacher_shift=0,
              #teacher_shift=0,
              # teacher_scaling = None,
              # teacher_shift = None,
              out_activation=np.tanh,
              inverse_out_activation=np.arctanh,
              random_state=rng,
              silent=False)
     
     
    print ('n_inputs=', esn.n_inputs)
    print ('n_outputs=', esn.n_outputs)
    print ('n_reservoir=', esn.n_reservoir)
    print ('spectral radius=', esn.spectral_radius)
    print ('sparsity=', esn.sparsity)
    print ('noise=', esn.noise)
    print ('input_shift=', esn.input_shift)
    print ('input_scaling=', esn.input_scaling)
    print ('teacher_forcing=', esn.teacher_forcing)
    # print ('feedback_scaling=' , esn1.feedback_scaling)
    print ('teacher_scaling=', esn.teacher_scaling)
    print ('teacher_shift=', esn.teacher_shift)
    print ('out_activation=', esn.out_activation)
    print ('inverse_out=', esn.inverse_out_activation)
    print ('random_state=', esn.random_state)
    print ('silent=', esn.silent)


    pred_train = esn.fit(train_data, train_data_angle)
    #print(pred_train)
    pred_test = esn.predict(test_data)
    #print('PREDICTED TEST', pred_test)
    pred_max_angle = max(pred_test)*2*max_angle
    return_angles = np.ceil(pred_test*2*max_angle)
    pred_max_angle = int(np.ceil(pred_max_angle))
    #print(pred_max_angle)
    #exit()
    pp.figure(1)
    font = {'family' : 'sans',
        'size'   : 14}	
    pp.rc('font', **font)
    pp.xlim(0,100)
    pp.ylim(0,20)
    pp.xlabel('Network Run Time (slot)')
    pp.ylabel('Directivity Angle (degree)') 
    #print()
    #print()
    a=(test_data_angle*2*max_angle)[0]
    b=(pred_test*2*max_angle)[0]
    #print(a)
    #print(b)
    acc = 100-((a-b)/a)*100
    #print(acc)
    #exit()
    #print(test_data_angle*2*max_angle)
    #print(pred_test*2*max_angle)
    before = sum(test_data_angle*2*max_angle)
    after = sum(pred_test*2*max_angle)
    #print(before)
    #print(after)
    error = (abs(after-before)/after)*100
    #print(accuracy1)
    #accuracy2 = (after/before)*100
    #print(accuracy2)
    
    pp.plot(range(len(test_data_angle)), test_data_angle*2*max_angle,c='r',marker = 'o', label='Optimal Directivity Angle')
    pp.plot(range(len(test_data_angle)), pred_test*2*max_angle,c='k', linestyle='--',label='Predicted Directivity Angle')
    pp.legend()
    pp.grid(True)
    pp.show()
    exit()
    list_angles = [(pred_max_angle), (pred_max_angle)*2, (pred_max_angle)*4, (pred_max_angle)*6, (pred_max_angle)*8]
    #print(list_angles)
    
    
    
    
    return return_angles
    
    
    
    
    
    
