import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#########  数据生成  #########
GDP_raw = pd.read_csv("GDP.csv", index_col=0, skiprows=4)

year = list(range(1996,2017))
cty = ["China", "Australia", "Canada", "Japan", "United Kingdom", "Italy",
       "Singapore", "Germany", "France", "Switzerland"]
GDP = GDP_raw[[str(x) for x in year]].loc[cty]

#########  作图过程  #########
fig, ax = plt.subplots(figsize=(16,8))
ax.grid(True)
ax.set_ylim(np.min(GDP.values), np.max(GDP.values))
ax.set_xlim(min(year), max(year))
ax.set_xticks(range(1996, 2017, 2))
ax.set_ylabel("GDP value")

ln0, ln1, ln2, ln3, ln4, ln5, ln6, ln7, ln8, ln9 = ax.plot([], [], 'o-',
                                                           [], [], 'v-',
                                                           [], [], '^-',
                                                           [], [], '<-',
                                                           [], [], '>-',
                                                           [], [], 's-',
                                                           [], [], '*-',
                                                           [], [], 'p-',
                                                           [], [], 'P-',
                                                           [], [], '+-',
                                                           animated=False)

x, y0, y1, y2, y3, y4, y5, y6, y7, y8, y9 = year, GDP.values[0], GDP.values[1], GDP.values[2], \
                        GDP.values[3], GDP.values[4], GDP.values[5], GDP.values[6], \
                        GDP.values[7], GDP.values[8], GDP.values[9]

def animate(i):
    ln0.set_data(x[0:i+1], y0[0:i+1])
    ln1.set_data(x[0:i+1], y1[0:i+1])
    ln2.set_data(x[0:i+1], y2[0:i+1])
    ln3.set_data(x[0:i+1], y3[0:i+1])
    ln4.set_data(x[0:i+1], y4[0:i+1])
    ln5.set_data(x[0:i+1], y5[0:i+1])
    ln6.set_data(x[0:i+1], y6[0:i+1])
    ln7.set_data(x[0:i+1], y7[0:i+1])
    ln8.set_data(x[0:i+1], y8[0:i+1])
    ln9.set_data(x[0:i+1], y9[0:i+1])
    return ln0, ln1, ln2, ln3, ln4, ln5, ln6, ln7, ln8, ln9

anim = FuncAnimation(fig, animate, len(year), interval=100, blit=False)
# anim.save('animation.mp4', writer='ffmpeg', fps=30)

plt.title('GDP animation')
plt.legend((ln0, ln1, ln2, ln3, ln4, ln5, ln6, ln7, ln8, ln9), cty, loc="upper left", frameon=False)
plt.show()
