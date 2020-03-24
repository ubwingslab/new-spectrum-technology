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
# Date: 02/03/2019
# Author: Zhangyu Guan
# Network functions and classes
#######################################################

# from current folder
import net_name

# -------------------------------------------------------------------------
# network element operations
# -------------------------------------------------------------------------

def mkinfo(elmt_type, elmt_subtype, elmt_num, addi_info):
    '''
    basic information to define a network element
    '''
    net_info = {'elmt_type': elmt_type, 'elmt_subtype': elmt_subtype, 'elmt_num': elmt_num, 'addi_info': addi_info}
    return net_info   
    
# -------------------------------------------------------------------------
# basic network element class 
# base class of all other element classes
# -------------------------------------------------------------------------
class netelmt_group:
    def __init__(self, info):
        self.type       = info['elmt_type']                       # network element type: network, node, session, parameter (variable) ...       
        self.name       = self.type                               # The same as type, just for easy use
        
        self.stype      = info['elmt_subtype']                    # subtype: Parameter: power, frequency, rate ...
        self.member     = []                                      # members list in the current group
            
        # pointer to network, parent, and itself
        self.ntwk       = info['addi_info']['ntwk']                 # to network
        if self.ntwk == None:                                       # when creating a network, None 
            self.ntwk = self 

        self.parent     = info['addi_info']['parent']               # to parent

        # register the elelemt according to addi_info
        if net_name.if_rgst in info['addi_info'].keys():
            if info['addi_info'][net_name.if_rgst] == net_name.no:  # no need to register
                b_rgst = 0
            else:
                b_rgst = 1
        else:             
            b_rgst = 1
                      
        if b_rgst == 1:                                             # need to register, or not specified    
            ptr_name = '_'+self.type                                # to itself; pointer name format: node: _node
            if hasattr(self.ntwk, ptr_name):
                print('Error: Duplicated network element!')           
                exit(0)
            else:
                setattr(self.ntwk, ptr_name, self)
        else:
            pass
                                              
    def ping(self):
        '''
        disp information
        '''       
        #print('--------------Basic Information------------------')
        print('Elmt: {}, members: {}'.format(self.type, self.member))
        # print('Sub-elmt: {}'.format(self.subgroup))
        # for subgrp in self.subgroup:           
            # if subgrp == net_name.default:                          # skip the default dumb subgroup
                # pass
            # else:
                # x = getattr(self, subgrp)
                # print('{}, members: {}'.format(x.type, x.member))
                 
    def hasgroup(self, groupname):
        '''
        check if an element has a group 
        '''
        return hasattr(self, groupname)


    def addgroup(self, groupname, groupvalue):
        '''
        add a new group to an element
        '''
        if self.hasgroup(groupname):
            print('Error: group {} already exists.'.format(groupname))
            exit(0)
        else:
            setattr(self, groupname, groupvalue)         # create new subgroup

    def addmember(self, mem_name):
        '''
        add new members to current group; if the member is also in the member list, do nothing
        otherwise append the member
        '''       
        
        if mem_name in self.member:
            print('Warning: {} already in the member list.'.format(mem_name))
        else:        
            self.member.append(mem_name)
            
           
    def delmember(self, mem_num):
        '''
        delete members from current group
        '''                   
        if mem_name not in self.member:
            print('Warning: {} is not in the member list.'.format(mem_name))
        else:        
            self.member.remove(mem_name)
            print('{}, members: {}'.format(self.type, self.member))
        
    def get_memnum(self):
        '''
        the number of members
        '''  
        return len(self.member)
        
    def set_memnum(self, mem_num):
        '''
        set the number of membes in this group
        '''        
        if mem_num < 0:
            print('Error: The number of members must be >= 0! ')
            Exit(0)
        else:
            self.member = range(mem_num)        

    def get_ntwk(self):
        '''
        return the network object
        '''         
        return self.ntwk

    def get_netelmt(self, elmt_name):
        '''
        return the network object
        '''         
        # get network
        ntwk = self.get_ntwk()
         
        # get network element
        _elmt_name = '_'+elmt_name                                            # construct network attribute cosrresponding to elmt_name
        
        if hasattr(ntwk, _elmt_name) == False:      
            #print('Network element {} does not exist, ntwk notified.'.format(_elmt_name))    # the request network element doesn't exist
            
            # if the wanted element does not exist, notify the network
            # will be implemented in future
            
            return None
        else:
            return getattr(ntwk, _elmt_name)             