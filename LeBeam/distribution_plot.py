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
#import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import gamma
#sns.set(color_codes=True)
#sns.set(context='notebook', style='whitegrid', palette='deep', font='sans', font_scale=1.2, color_codes=True, rc=None)
#sns.set_style("whitegrid"); np.random.seed(0)
import random, math
import statistics

def plots_loc(data):
    #x = np.random.normal(size=100)
    #print(x)
    #print(data)
    data_norm=data
    data_gamma=data
    data_beta=data
    m = statistics.mean(data_norm)
    print('A', m)
    v = statistics.variance(data_norm)
    print('B', v)
    
    font = {'family' : 'sans',
    'size'   : 20}	
    plt.rc('font', **font)

    plt.hist(data_norm, density=True)
    #print(plt.xticks())
    xt = plt.xticks()[0]  
    #print(xt)
    xmin, xmax = min(xt), max(xt)  
    #print(xmin, xmax)
    lnspc = np.linspace(xmin*1.5, xmax*1.5, len(data_norm))
    #print(lnspc)
    #exit()
    # Normal Distribution
    m, s = stats.norm.fit(data_norm) # get mean and standard deviation  
    pdf_g = stats.norm.pdf(lnspc, m, s) # now get theoretical values in our interval  
    plt.plot(lnspc, pdf_g, c='r', linestyle = '--', label="Normal Distribution") # plot it

    # Gamma Distribution
    ag,bg,cg = stats.gamma.fit(data_gamma)  
    pdf_gamma = stats.gamma.pdf(lnspc, ag, bg,cg)  
    plt.plot(lnspc, pdf_gamma, c='b', linestyle = '-.', label="Gamma Distribution")

    # Beta Distribution 
    ab,bb,cb,db = stats.beta.fit(data_beta)  
    pdf_beta = stats.beta.pdf(lnspc, ab, bb,cb, db)  
    plt.plot(lnspc, pdf_beta, c='k', linestyle = '-', label="Beta Distribution")
    plt.xlabel('Values')
    plt.ylabel('Density')
    plt.grid(True)
    plt.legend()
    plt.show()  
    
    


def plots_ang(data):
    #x = np.random.normal(size=100)
    #print(x)
    #print(data)
    data_norm=data
    data_gamma=data
    data_beta=data
    mean = statistics.mean(data_norm)
    print('C', mean)
    variance = statistics.variance(data_norm)
    print('D', variance)
    font = {'family' : 'sans',
    'size'   : 18}	
    plt.rc('font', **font)
    
    plt.hist(data_norm, density=True)
    
    xt = plt.xticks()[0]  
    xmin, xmax = min(xt), max(xt)  
    lnspc = np.linspace(xmin*1.5, xmax*1.5, len(data_norm))
    
    # Normal Distribution
    m, s = stats.norm.fit(data_norm) # get mean and standard deviation  
    pdf_g = stats.norm.pdf(lnspc, m, s) # now get theoretical values in our interval  
    plt.plot(lnspc, pdf_g, c='r', linestyle = '--', label="Normal Distribution") # plot it

    # Gamma Distribution
    ag,bg,cg = stats.gamma.fit(data_gamma)  
    pdf_gamma = stats.gamma.pdf(lnspc, ag, bg,cg)  
    plt.plot(lnspc, pdf_gamma, c='b', linestyle = '-.', label="Gamma Distribution")

    # Beta Distribution 
    ab,bb,cb,db = stats.beta.fit(data_beta)  
    pdf_beta = stats.beta.pdf(lnspc, ab, bb,cb, db)  
    plt.plot(lnspc, pdf_beta, c='k', linestyle = '-', label="Beta Distribution")
    
    plt.xlabel('Values')
    plt.ylabel('Density')
    plt.grid(True)
    plt.legend()
    plt.show()  
