import tkinter as tk
import random
import time
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class Ball(object):   
    def __init__(self, canvas, *args, **kwargs):
        self.canvas = canvas 
        self.oval = canvas.create_oval(*args, **kwargs)
        
        x1, y1, x2, y2 = self.canvas.bbox(self.oval) # returns tuple with dimensions of rectangle enclosing Ball
        self.pos = np.array((x1 + (x2 - x1)/2, 
                         y1 + (y2 - y1)/2)) # center position of ball 
        
        self.v_mod = random.uniform(-1,1)
        self.v_ang = random.uniform(-np.pi/2, np.pi/2)               
        self.v = np.array((self.v_mod*np.cos(self.v_ang),
                          self.v_mod*np.sin(self.v_ang)))
        
        
    def bounce_walls(self):
            
        
        x1, y1, x2, y2 = self.canvas.bbox(self.oval)
        self.pos = np.array((x1 + (x2 - x1)/2, y1 + (y2 - y1)/2)) # update ball position every iteration through animate
        
        # using abs values prevents ball from getting stuck at wall
        if x1 < App.frame_gap:
            self.v[0] = abs(self.v[0])
        if y1 < App.frame_gap:
            self.v[1] = abs(self.v[1])
        if x2 > App.frame_width + App.frame_gap:
            self.v[0] = -abs(self.v[0])
        if y2 > App.frame_height + App.frame_gap:
            self.v[1] = -abs(self.v[1])        
              
    def remove(self, canvas):
        self.canvas.delete(self.oval)
        
    def overlap(self, other):
        
        d = ((self.pos[0] - other.pos[0])**2 +
            (self.pos[1] - other.pos[1])**2)**0.5
        
        if d < App.b_size:
            return True
        else:
            return False   
        
        
    def Movement(self):
        self.canvas.move(self.oval, self.v[0], self.v[1])


class App(object):
    N = 200 # number of balls
    b_size = 6
    
    frame_height = 500
    frame_width = 500
    frame_gap = 20
       
    
    def __init__(self, master, **kwargs):
        self.master = master

        self.canvas = tk.Canvas(self.master, width=App.frame_width+20, height=App.frame_height+40) #dimensions of window  

        self.rectangle = self.canvas.create_rectangle(App.frame_gap, App.frame_gap, App.frame_width+App.frame_gap, App.frame_height+App.frame_gap, outline='black')
        self.canvas.pack(side=tk.LEFT)                
        self.balls = []
        for j in range(App.N):
            
            self.place_x = (App.frame_width - App.b_size)*random.random()
            self.place_y = (App.frame_height - App.b_size)*random.random()
            
            self.balls.append(Ball(self.canvas,self.place_x+App.frame_gap, self.place_y+App.frame_gap,
            self.place_x+App.frame_gap+App.b_size, self.place_y+App.frame_gap+App.b_size,
            outline='white', fill = 'red')) # creates N balls randomly placed
            
            Free = False
            while Free == False: 
                Free = True
                for i in range(len(self.balls)-1):
                    if self.balls[-1].overlap(self.balls[i])==True: # delete ball if overlaps with other balls
                    
                    
                        Free = False
                        
                        self.canvas.delete(self.balls[-1].oval) # delete last ball from canvas                
                        del self.balls[-1] # delete last ball from list
                        
                        
                        self.place_x = (App.frame_width - App.b_size)*random.random()
                        self.place_y = (App.frame_height - App.b_size)*random.random()
        
                        self.balls.append(Ball(self.canvas,self.place_x+App.frame_gap, self.place_y+App.frame_gap,
                                               self.place_x+App.frame_gap+App.b_size, self.place_y+App.frame_gap+App.b_size,
                                               outline='white', fill = 'red')) # creates N balls randomly placed
                        
        self.master.after(0, self.animate)
    
    # Plot
      
        self.fig1 = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig1.add_subplot(1,1,1)
        self.ax.set_xlim(0, 2)
        self.ax.set_ylim(0, 30)
        self.ax.set_xlabel("velocity")
        self.ax.set_ylabel("count")
        velo = [(x.v[0]**2 + x.v[1]**2)**0.5 for x in self.balls]
        
        self.ax.hist(velo, bins=30)
        self.canvas_plot = FigureCanvasTkAgg(self.fig1, master = self.master)
        self.ax.grid(True)
        self.canvas_plot.draw()

        self.canvas_plot.get_tk_widget().pack(side=tk.RIGHT, expand=1)

        
    def collision(self):
        
        pairs = combinations(range(App.N), 2)
        for i,j in pairs:
            if self.balls[i].overlap(self.balls[j]) == True:

                    
                n = self.balls[i].v # previous velocity so that we don´t use the changed velocity
                m = self.balls[j].v
                
                # velocity change in elastic collisions
                self.balls[i].v = n - \
                np.dot(n - m, self.balls[i].pos - self.balls[j].pos) * \
                (self.balls[i].pos - self.balls[j].pos) / \
                np.linalg.norm(self.balls[i].pos - self.balls[j].pos)**2
                    
                self.balls[j].v = m - \
                np.dot(m - n, self.balls[j].pos - self.balls[i].pos) * \
                (self.balls[j].pos - self.balls[i].pos) / \
                np.linalg.norm(self.balls[j].pos - self.balls[i].pos)**2


    def histogram_update(self):
        
        
        self.ax.clear()

        self.ax.set_xlim(0, 2)
        self.ax.set_ylim(0, 30)
        self.ax.set_xlabel("velocity")
        self.ax.set_ylabel("count"
        velo = [(x.v[0]**2 + x.v[1]**2)**0.5 for x in self.balls]       
        self.ax.hist(velo, bins=30)

        self.ax.grid(True)
        self.canvas_plot.draw()



    def animate(self):
        for ball in self.balls:
           ball.bounce_walls()
        self.collision()
        for ball in self.balls:
            ball.Movement()
        self.histogram_update()
        self.master.after(100, self.animate)    


root = tk.Tk()
root.title('Elastic collisions')
app = App(root)
root.mainloop()