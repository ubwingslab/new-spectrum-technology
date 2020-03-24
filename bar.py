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
import matplotlib.pyplot as plt

font = {'family' : 'sans',
        'size'   : 19}	
plt.rc('font', **font)

# data to plot
n_groups = 7
mobile = (0.96, 0.59, 0.7, 0.72, 0.79, 0.58, 0.98)
static = (0.92, 0.42, 0.5, 0.49, 0.56, 0.38, 0.60)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
#print(index)
bar_width = 0.25
opacity = 1


rects1 = plt.bar(index, mobile, bar_width, color='b', edgecolor='black', hatch='\\', label='Mobile Base Station')

rects2 = plt.bar(index + bar_width, static, bar_width, color='g', edgecolor='black', hatch='//', label='Static Base Station' )

#plt.xlabel('Frequency Bands')
plt.ylabel('Jain\'s Fairness Index')
plt.xticks(index+ 0.15, ('Micro only', 'Milli only', 'Tera only', 'Micro & Milli', 'Micro & Tera', 'Milli & Tera', 'All three bands'))
plt.legend()
plt.grid(True)
#plt.tight_layout()
plt.show()

# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np



# labels = ['Micro only', 'Milli only', 'Tera only', 'Micro & Milli', 'Micro & Tera', 'Milli & Tera', 'All three bands']
# mobile = [0.96, 0.59, 0.7, 0.72, 0.79, 0.58, 0.98]
# static = [0.92, 0.42, 0.5, 0.49, 0.56, 0.38, 0.60]

# x = np.arange(len(labels))  # the label locations
# width = 0.25  # the width of the bars

# fig, ax = plt.subplots()
# rects1 = ax.bar(x - width/2, mobile, width, edgecolor='black', hatch='\\', label='Mobile Base Station')
# rects2 = ax.bar(x + width/2, static, width, edgecolor='black', hatch='//', label='Static Base Station')

# font = {'family' : 'sans',
        # 'size'   : 19}	
# #ax.rc('font', **font)

# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_ylabel('Jain\'s Fairness Index')
# #ax.set_title('Scores by group and gender')
# ax.set_xticks(x)
# ax.set_xticklabels(labels)
# ax.legend()


# # def autolabel(rects):
    # # """Attach a text label above each bar in *rects*, displaying its height."""
    # # for rect in rects:
        # # height = rect.get_height()
        # # ax.annotate('{}'.format(height),
                    # # xy=(rect.get_x() + rect.get_width() / 2, height),
                    # # xytext=(0, 3),  # 3 points vertical offset
                    # # textcoords="offset points",
                    # # ha='center', va='bottom')


# # autolabel(rects1)
# # autolabel(rects2)

# fig.tight_layout()

# plt.show()