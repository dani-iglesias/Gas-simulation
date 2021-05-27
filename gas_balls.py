import tkinter as tk
import random
import time
import numpy as np
from itertools import combinations


class Ball(object):   
    def __init__(self, canvas, *args, **kwargs):
        self.canvas = canvas 
        self.oval = canvas.create_oval(*args, **kwargs)               
        self.v = np.array((random.gauss(0,1), random.gauss(0,1)))
        
        x1, y1, x2, y2 = self.canvas.bbox(self.oval) # returns tuple with dimensions of rectangle enclosing Ball
        self.pos = np.array((x1 + (x2 - x1)/2, 
                         y1 + (y2 - y1)/2)) # center position of ball 

        
    def bounce_walls(self):
        
        x1, y1, x2, y2 = self.canvas.bbox(self.oval)
        self.pos = np.array((x1 + (x2 - x1)/2, y1 + (y2 - y1)/2)) # update ball position every iteration through animate
        
        # using abs values prevents ball from getting stuck at wall
        if x1 < 20:
            self.v[0] = abs(self.v[0])
        if y1 < 70:
            self.v[1] = abs(self.v[1])
        if x2 > App.frame_width+20:
            self.v[0] = -abs(self.v[0])
        if y2 > App.frame_height+70:
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
    N = 30 # number of balls
    frame_height = 500
    frame_width = 700
    b_size = 30
    def __init__(self, master, **kwargs):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=App.frame_width+40, height=App.frame_height+90) #dimensions of window  

        self.rectangle = self.canvas.create_rectangle(20, 70, App.frame_width+20, App.frame_height+70, outline='black')
        self.canvas.pack()                
        self.balls = []
        for j in range(App.N):
            
            self.place_x = (App.frame_width - App.b_size)*random.random()
            self.place_y = (App.frame_height - App.b_size)*random.random()
            
            self.balls.append(Ball(self.canvas,self.place_x+20, self.place_y+70,
                        self.place_x+20+App.b_size, self.place_y+70+App.b_size,
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
        
                        self.balls.append(Ball(self.canvas, self.place_x, self.place_y,
                           self.place_x+App.b_size, self.place_y+App.b_size,
                           outline='white', fill = 'red')) # creates N balls randomly placed
                       
        print(len(self.balls))
        self.master.after(0, self.animate)

        
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



    def animate(self):
        for ball in self.balls:
           ball.bounce_walls()
        self.collision()
        for ball in self.balls:
            ball.Movement()
        self.master.after(20, self.animate)    


root = tk.Tk()
root.title('Elastic collisions')
app = App(root)
root.mainloop()