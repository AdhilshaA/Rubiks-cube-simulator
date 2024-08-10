# colors={0:"white",1:"green",2:"blue",3:"yellow",4:"orange",5:"red"}
# positions={0:"top",1:"front",2:"down",3:"back",4:"left",5:"right"}

import numpy as np
import matplotlib.pyplot as plt

n = 20

xs = []
for i in range(n):
    xs.append(100*(0.75**i))
# print(xs)

ys = []
for i in range(n):
    ys.append(100 - (i*5))
# print(ys)

fig,ax = plt.subplots()

ax.plot(xs,ys)
ax.set_xscale("log")
ax.set_xticks(xs)
# ax.set_xticklabels(xs)
plt.show()

