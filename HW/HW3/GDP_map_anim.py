from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import pandas as pd

#########  数据生成  #########
loc = pd.read_csv("location.csv")
GDP_raw = pd.read_csv("GDP.csv", index_col=0, skiprows=4)

year = list(range(1996,2017))
cty = ["China", "Australia", "Canada", "Japan", "United Kingdom", "Italy",
       "Singapore", "Germany", "France", "Switzerland"]

GDP = GDP_raw[[str(x) for x in year]].loc[cty]

"""
on : label or list
        Field names to join on. Must be found in both DataFrames. If on is
        None and not merging on indexes, then it merges on the intersection of
        the columns by default.
right_index : boolean, default False
        Use the index from the right DataFrame as the join key. Same caveats as
        left_index
"""
GDP = pd.merge(GDP, loc, left_index=True, right_on="Country Name")
GDP = GDP.set_index("Country Name")

#########  作图过程  #########
fig = plt.figure(figsize=(12, 8))
lons, lats = [], []

def initialize_map():
    m = Basemap()
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color = 'gray', zorder=0)
    m.drawmapboundary()
    m.drawmeridians(np.arange(0, 360, 30))
    m.drawparallels(np.arange(-90, 90, 30))
    return m

def init():
    return point,

# animation function.  This is called sequentially
def animate(i):
    plt.clf()

    m = initialize_map()
    GDP_year = GDP[str(1996+i)].values
    size = (GDP_year/np.max(GDP_year))*100
    x, y = m(GDP['lons'].values, GDP['lats'].values)
    m.scatter(x, y, s=size, color='r', alpha=0.7)
    return m,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, len(year), interval=100, blit=False)

plt.title('GDP Map animation')
plt.show()
