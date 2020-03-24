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
## Date: 02/26/2019
## Author: Zhangyu Guan
## GUI functions and classes 
#######################################################

import net_name, net_func, netcfg

from tkinter import *

import random

def new_gui(ntwk = None):
    '''
    create a GUI for the network
    ntwk: The network object for which the GUI is created
    '''
    #####################################################
    elmt_name = net_name.gui
    elmt_type = net_name.gui
    elmt_num  = 1    
    
    # network topology info, 1 network created
    addi_info = {'ntwk':ntwk, 'parent':ntwk}
    info = net_func.mkinfo(elmt_name, elmt_type, elmt_num, addi_info)    
    
    obj_gui = gui(info)
    #####################################################
    # create network
    return obj_gui  
    
    
class gui(net_func.netelmt_group):
    '''
    Definition of the gui class
    '''
    def __init__(self, net_info):      
        # from base network element
        net_func.netelmt_group.__init__(self, net_info)
        
        # Canvas dimension        
        self.widt = self.ntwk.net_width * netcfg.num_pixel_per_meter            # width
        self.leng = self.ntwk.net_length * netcfg.num_pixel_per_meter           # length
        self.heig = 0                                                           # height
               
        # Create the canvas
        self.chart = self.crt_canvas()

    def ping(self):
        net_func.netelmt_group.ping()
                
    def crt_canvas(self):   
        # Create a blank canvas with basic configuration information
        root = Tk()
        root.title(net_name.title1)        
        chart = Canvas(root, width=self.widt, height=self.leng, background= "white")
        chart.grid(row=1, column=1)
        
        return chart
    
    def operation(self, env):
        '''
        Operations for GUI
        env: discrete event environment
        '''       
        while True:           
            plot_interval = 30000
            x = random.randint(1, self.widt)
            y = random.randint(1, self.leng)
            self.chart.create_oval(x, y, x + 12, y + 12, fill="purple")
            self.chart.update()
            yield env.timeout(plot_interval)       
        
        

# #chart_1.delete(cur)
# if old is not None:
    # chart_1.delete(old)  
# old = cur
# print('Plotting finished')
# time.sleep(5)    
# # root.mainloop()