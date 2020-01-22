#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 12:15:41 2020

@author: thausmann
"""


import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation


class Particle():
    pos = []
    vel = []
    walls = []
    def __init__(self, position, walls):
        self.pos = np.array(position, 'float64')
        self.vel = np.array([0 for cord in self.pos], 'float64')
        self.walls = walls
        
    def update(self, dt):
        a = np.array([0,-9.81])
        self.vel += a*dt
        self.vel -= ((self.vel * 0.47 * dt * np.linalg.norm(self.vel) * np.pi)) * 0.1 / 10 # Air resistance decaleration with parenth coefficient times crosssection divided by mass 
        self.pos += self.vel*dt
        coll = self.collide()
        if coll!=None:
            if coll == 'inf':
                vec_m = np.array([0,1], 'float64')
            else:
                vec_m = np.multiply(np.array([1,coll], 'float64'), 1/np.sqrt(1+coll**2))
            vec_along = np.dot(vec_m, self.vel) * vec_m
            self.vel = (2 * vec_along - self.vel)
            
    
    def collide(self):
        for wall in self.walls:
            x_range, y_range = wall.line()
            s = (self.pos[0] - x_range[0])  
            if s>0 and s<(x_range[1] - x_range[0])+0.01:
                if  x_range[0] != x_range[1]:
                    m = (y_range[1]-y_range[0]) / (x_range[1] - x_range[0])
                    if self.pos[1]-0.15 < y_range[0] + m * s:
                        return m
                else:
                    return 'inf'
        return None
                    
    
class Wall():
    pos = []
    def __init__(self, position):
        self.pos = np.array(position, 'float64')
        
    def line(self):
        return self.pos[0], self.pos[1]
        

        
animation_speed = 1
animation_acc = 10000 #calculations per simulated second
fps = 30 #frames per real second


fig = plt.figure()
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
ws = [Wall([[0,10],[0,0]]), Wall([[4,10],[0,3]]), Wall([[0,1.4],[3,0]]), Wall([[0,0],[10,0]]), Wall([[10,10],[10,0]])]
for w in ws:
    x_range, y_range = w.line()
    plt.plot(x_range, y_range)
point, = ax.plot([], [], 'ro', lw=2)
p = Particle([8, 9],ws)
# initialization function: plot the background of each frame. Repeats every second
def init():
    point.set_data([], [])
    return point,

# animation function.  This is called sequentially
def animate(i):
    for k in range(int(animation_acc/fps)):
        p.update(animation_speed/animation_acc)
    x, y = p.pos
    point.set_data([x], [y])
    return point,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=fps, interval=int(1000/fps), blit=True)

plt.plot()