from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import pandas as pd

df_loc = pd.read_csv("data/location.csv")
df_gdp = pd.read_csv("data/GDP.csv", skiprows=4)

print(df_loc.head())
print(df_gdp.head())
df_gdp = pd.merge(df_loc, df_gdp, on="Country Name")

print(df_gdp.head())

plt.figure(figsize=(12, 8))

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
    global size
    global m
    lons, lats =  np.random.random_integers(-130, 130, 2)
    x,y = m(lons, lats)
    point.set_offsets(np.array([[x, y]]))
    point.set_sizes(size*i*100)
    return point,

m = initialize_map()
x,y = m([0], [0])
size = np.array([10])
point = m.scatter(x, y, s=0, alpha = 0.5)

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(plt.gcf(), animate, init_func=init,
                               frames=20, interval=1000, blit=True)

plt.show()
