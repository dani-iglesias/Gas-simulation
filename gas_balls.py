import tkinter as tk
import random
import time
import numpy as np


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
        self.canvas.move(self.oval, self.v[0], self.v[1])
        
        self.pos = np.array((x1 + (x2 - x1)/2, 
                         y1 + (y2 - y1)/2)) # center position of ball       


class App(object):
    N = 2 # number of balls
    frame_size = 500
    b_size = 150
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
    def collision(self):
        d = []
        for i in range(App.N):
            
            d.append([((self.balls[i].pos[0] - self.balls[j].pos[0])**2 +
            (self.balls[i].pos[1] - self.balls[j].pos[1])**2)**0.5
                 for j in range(App.N) if j>i]) # distances between a ball and the others

        del d[-1] #remove last position from list since it is empty
        
        for x, val in enumerate(d):
            for y, val1 in enumerate(val):
                if val1 < App.b_size: # if a distance smaller than balls diameter
                    
                    print(x)
                    print(y+x+1)
                    print(self.balls[x].pos)
                    print(self.balls[x+y+1].pos)
                    
                    n = self.balls[x].v # previous velocity so that we don´t use the changed velocity
                    m = self.balls[y+x+1].v
                    
                    self.balls[x].v = n - \
                    np.dot(n - m, self.balls[x].pos - self.balls[y+x+1].pos) * \
                    (self.balls[x].pos - self.balls[y+x+1].pos) / \
                    d[x][y]
                    #np.linalg.norm(self.balls[x].pos - self.balls[y+x+1].pos)**2
                    
                    self.balls[y+x+1].v = m - \
                    np.dot(m - n, self.balls[y+x+1].pos - self.balls[x].pos) * \
                    (self.balls[y+x+1].pos - self.balls[x].pos) / \
                    d[x][y]
                    #np.linalg.norm(self.balls[y+x+1].pos - self.balls[x].pos)**2
                    
                    
                    self.balls[x].step_x = -self.balls[x].step_x
                    self.balls[x].step_y = -self.balls[x].step_y
                    self.balls[y].step_x = -self.balls[y].step_x
                    self.balls[y].step_y = -self.balls[y].step_y
                    
        print('hai')                                
        for x, value in enumerate(self.balls):            
            print(self.balls[x].v)
            self.balls[x].canvas.move(self.balls[x].oval, self.balls[x].v[0], self.balls[x].v[1])
        #self.balls[y].canvas.move(self.balls[y].oval, self.balls[y].v[0], self.balls[y].v[1])
        '''            
                  
    def animate(self):
        for ball in self.balls:
           ball.bounce_walls()
        #self.collision()
        self.master.after(5, self.animate)    


root = tk.Tk()
app = App(root)
root.mainloop()
