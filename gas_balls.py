import tkinter as tk
import random
import time
import numpy as np
from itertools import combinations


class Ball(object):   
    def __init__(self, canvas, *args, **kwargs):
        self.canvas = canvas # The canvas is defined inside other class
        self.oval = canvas.create_oval(*args, **kwargs)        
        #self.step_x = random.gauss(0,1) # step size which the ball is moving every iteration
        #self.step_y = random.gauss(0,1)
        
        self.v = np.array((random.gauss(0,1), random.gauss(0,1))) 
        
       
    def bounce_walls(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.oval) # returns tuple with dimensions of rectangle enclosing Ball
        if x1 < 0:
            self.v[0] = -self.v[0]
        if y1 < 0:
            self.v[1] = -self.v[1]
        if x2 > 500:
            self.v[0] = -self.v[0]
        if y2 > 500:
            self.v[1] = -self.v[1]
        #self.canvas.move(self.oval, self.v[0], self.v[1])
        
        self.pos = np.array((x1 + (x2 - x1)/2, 
                         y1 + (y2 - y1)/2)) # center position of ball       


class App(object):
    N = 5 # number of balls
    frame_size = 500
    b_size = 60
    def __init__(self, master, **kwargs):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=500, height=500) #dimensions of window  
        self.canvas.pack()
        

        self.place_x = [(App.frame_size - App.b_size)*random.random() for i in range(App.N)]
        self.place_y = [(App.frame_size - App.b_size)*random.random() for i in range(App.N)]
        
        self.balls = [Ball(self.canvas, self.place_x[i], self.place_y[i],
                           self.place_x[i]+App.b_size, self.place_y[i]+App.b_size,
                           outline='white', fill = 'red') for i in range(App.N)] # creates N balls randomly placed

        self.master.after(0, self.animate)
        '''    
    def overlap(self, other):
        
        d = ((self.pos[0] - other.pos[0])**2 +
            (self.pos[1] - other.pos[1])**2)**0.
        
        if d < App.b_size:
            return True
        else:
            return False
        '''        
    def collision(self):
        
        pairs = combinations(range(App.N), 2)
        for i,j in pairs:


            d = ((self.balls[i].pos[0] - self.balls[j].pos[0])**2 +
            (self.balls[i].pos[1] - self.balls[j].pos[1])**2)**0.5
            
            if d < App.b_size:
                
                    
                n = self.balls[i].v # previous velocity so that we don´t use the changed velocity
                m = self.balls[j].v
                    
                self.balls[i].v = n - \
                np.dot(n - m, self.balls[i].pos - self.balls[j].pos) * \
                (self.balls[i].pos - self.balls[j].pos) / \
                np.linalg.norm(self.balls[i].pos - self.balls[j].pos)**2
                    
                self.balls[j].v = m - \
                np.dot(m - n, self.balls[j].pos - self.balls[i].pos) * \
                (self.balls[j].pos - self.balls[i].pos) / \
                np.linalg.norm(self.balls[j].pos - self.balls[i].pos)**2


        for x in self.balls:
            x.canvas.move(x.oval, x.v[0], x.v[1])



    def animate(self):
        for ball in self.balls:
           ball.bounce_walls()
        self.collision()
        self.master.after(5, self.animate)    


root = tk.Tk()
app = App(root)
root.mainloop()
