#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 13:56:08 2020

@author: thausmann
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import time


class Particle():
    q = np.pi/2
    r = 2
    vel = 0
    def __init__(self, position):
        self.x_0, self.y_0 = position
        
    def pos(self):
        return self.x_0 - self.r * np.sin(self.q), self.y_0 - self.r * np.cos(self.q)
        
    def update(self, dt):
        a = lambda q: 2 / self.r * np.sin(q) * -9.81
        self.vel += RungeKutta_step(a, self.q, dt)
        self.vel -= ((self.vel * 0.47 * dt * np.pi)) * 0.1 / 10 # Air resistance decaleration with parenth coefficient times crosssection divided by mass 
        self.q += RungeKutta_step(lambda q: self.vel, self.q, dt)
            

def RungeKutta_step(d_e, y, step):
    s1 = d_e(y)
    y += step*s1/2
    s2 = d_e(y)
    y += step*s2/2 - step*s1/2
    s3 = d_e(y)
    y += s3*step - step*s2/2
    s4 = d_e(y)
    return step/6*(s1 + 2*(s2+s3) + s4)


        
animation_speed = 1
animation_acc = 1000 #calculations per simulated second
fps = 60 #frames per real second


fig = plt.figure()
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))

point, = ax.plot([], [], 'ro', lw=2)
line, = ax.plot([], [], 'r-', lw=2)
p = Particle([5, 8])
loc_time = time.time()
avg = []
# initialization function: plot the background of each frame. Repeats every second
def init():
    global loc_time
    global avg
    point.set_data([], [])
    line.set_data([], [])
    avg.append( fps / (time.time() - loc_time))
    print(f'fps: {(sum(avg[int(len(avg)/10):])/(len(avg)-int(len(avg)/10))).__round__(1)}')
    loc_time = time.time()
    return point, line,

# animation function.  This is called sequentially
def animate(i):
    for k in range(int(animation_acc/fps)):
        p.update(animation_speed/animation_acc)
    x, y = p.pos()
    point.set_data([x], [y])
    line.set_data([5,x], [8,y])
    return point, line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=fps, interval=int(1000/fps), blit=True)

plt.plot()