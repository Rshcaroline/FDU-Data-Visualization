from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import pandas as pd
import random
import matplotlib.cm as cm

#########  数据生成  #########
loc = pd.read_csv("location.csv")
GDP_raw = pd.read_csv("GDP.csv", index_col=0, skiprows=4)

year = list(range(1996,2017))
cty = ["China", "Australia", "Canada", "Japan", "United Kingdom", "Italy",
       "Singapore", "Germany", "France", "Switzerland"]

GDP = GDP_raw[[str(x) for x in year]].loc[cty]

# 采用类似数据库的合并操作 将GDP数据和国家的经纬度数据合并成一个新的表
GDP = pd.merge(GDP, loc, left_index=True, right_on="Country Name")
GDP = GDP.set_index("Country Name")

#########  作图过程  #########
fig = plt.figure(figsize=(12, 8))
lons, lats = [], []

# 画出世界地图
def initialize_map():
    m = Basemap()
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color = 'gray', zorder=0)
    m.drawmapboundary()
    m.drawmeridians(np.arange(0, 360, 30))
    m.drawparallels(np.arange(-90, 90, 30))
    return m

# animation function.  This is called sequentially
def animate(i):
    global cty

    # 设置图例和散点颜色
    C = cm.rainbow(np.linspace(0, 1, len(cty)))
    # ctys=['$'+x+'$' for x in cty]

    # 每新的一年 清空画布上的散点并画出世界地图
    plt.clf()
    m = initialize_map()

    # 取出每一年的GDP数据 将GDP的相对大小当作散点的大小
    GDP_year = GDP[str(1996+i)].values
    size = (GDP_year/np.max(GDP_year))*300
    x, y = m(GDP['lons'].values, GDP['lats'].values)

    for ct in range(len(cty)):
      m.scatter(x[ct], y[ct], s=size[ct], label=cty[ct], c=C[ct], alpha=0.7)

    # 每次都要执行
    plt.title('GDP Map animation of Year ' + str(1996+i))
    plt.legend()

    return m,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, len(year), interval=100, blit=False)

plt.show()
