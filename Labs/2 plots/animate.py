import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import animation

minLimit = 0
maxLimit = 31

dataReal = "./datasets/data/world-cup-predictions/wc-20140609-140000.csv"

pdata = pd.read_csv(dataReal,sep=",")
countryList = pdata["country"].values[minLimit:maxLimit]
spiScore = pdata["spi"].values[minLimit:maxLimit]
x_pos = list(range(len(countryList)))
# set up figure, axis, plot element we want to animate
fig, ax = plt.subplots()
ax.grid()
ax.set_ylim(min(spiScore), max(spiScore))
ax.set_xlim(0, len(x_pos))
line, = ax.plot([], [], lw=1)
xdata, ydata = [],[]

def animate(i):
    print ("append_line ",i)
    ax.annotate(countryList[i] + ":" + str(spiScore[i]), (i, spiScore[i] ))
    line.set_data(x_pos[0:i+1], spiScore[0:i+1])
    return line

anim = animation.FuncAnimation(fig, animate,len(x_pos), interval=10, blit=False)
anim.save('animation.mp4', writer='ffmpeg', fps=30)
plt.show()
