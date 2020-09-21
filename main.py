'''
Bouncing Ball Simulation
This is an implementation of a bouncing ball simulation using mainly the Tkinter library in Python.
It includes physics and mechanics-related concepts such as gravity, air resistance, and collision.
Before the start of the simulation, the program prompts the user to enter a value for gravity and
air density. If you do not want to enter a value, please click on cancel or the window's exit button
and the default value is going to be applied (9.8 m/s^2 for gravity and 1.225 km/m^3 for air resistance).
If a vacuum setting is preferred, please enter 0 for both windows.

by Jing Han Sun
Updated September 21, 2020
'''

import tkinter as tk
from tkinter import simpledialog
import random
import math
import sys


class Visual(tk.Tk):
    '''This is the main class the will run the simulation'''

    #define width and height for window
    HEIGHT = 500
    WIDTH = 500

    #define a list of colors for the balls
    colors = ['#FF4325', '#E72020', #red
              '#FF9333',  #orange
              '#FEFA5F',  #yellow
              '#89F45E', '#9DFFA7', '#278A2A', #green
              '#6A8EFF', '#A8E5F9', '#1FFBF8', '#3253F4', '#2A438B', #blue
              '#67419E', '#C280FF', '#E12FE1', '#F1BFFC', #purple
              '#FCBFE9', '#FC22A0' #pink
              ]

    def __init__(self, argv):
        super().__init__()

        #create canvas
        self.canvas = tk.Canvas(self, width = self.WIDTH, height = self.HEIGHT, bg = 'white')
        self.canvas.pack()
        self.update()

        #window title
        self.title('Bouncing Balls')

        #add label
        self.label = tk.Label(self, text = 'Welcome!')
        self.label.pack()

        #add quit button
        self.button = tk.Button(self, text = "Quit", fg = 'red', command = self.quit())
        self.button.configure(width = 10, activebackground = "#33B5E5", relief = tk.FLAT)
        #self.button_window = self.canvas.create_window(10, 10, anchor = tk.NW , window = self.button)
        self.button.pack()
        self.update()

        #create dictionary to store info about circles (radius, dir_x, dir_y)
        self.circles_id = {}

        # ask the user to enter a value for gravity
        gravity = simpledialog.askfloat("Input", "Please enter a value for gravity (e.g.: 9.8)")
        if gravity is None:
            # use Earth's gravitational constant if no value is entered
            gravity = 9.8

        air_density = simpledialog.askfloat("Input", "Please enter a value for air density (e.g.: 1.225)")
        if air_density is None:
            # use the air density at STP if no value is entered
            air_density = 1.225

        for i in range(6):

            #set up a random radius
            radius = random.randint(20, 30)

            #set up a random initial center for each circle
            cx = random.randint(radius + 10, self.WIDTH - radius - 10)
            cy = random.randint(radius + 10, self.HEIGHT - radius - 10)

            #set up a random initial direction for each circle, from 1 to 360 degrees
            dir_x = random.randint(-10, 10)
            dir_y = random.randint(-10, 10)

            #create the circle
            ids = self.canvas.create_oval(cx - radius, cy - radius,
                                          cx + radius, cy + radius,
                                          fill = random.choice(self.colors), outline = 'black')

            #fill each list for each ball's characteristics
            #circles_id = {ids: [radius, dir_x, dir_y]}
            self.circles_id[ids] = [radius, dir_x, dir_y]

        #boolean that returns true if 2 balls overlap
        self.overlaps = False


        #actual animation
        while True:

            self.move_circles()

            #if it hits a wall
            self.bounce()

            self.collision()

            self.gravity(gravity)

            self.air_resistance(air_density)


    def center(self, circle):
        '''Get the center coordinates of a given ball'''

        x0, y0, x1, y1 = self.canvas.coords(circle)
        x = (x0 + x1) / 2
        y = (y0 + y1) / 2

        return x, y


    def distance(self, circle1, circle2):
        '''Get the distance between the center of 2 given balls'''

        x1, y1 = self.center(circle1)
        x2, y2 = self.center(circle2)

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


    def theta(self, x, y):
        '''Get the angle in radians (between 0 and 2pi) of a ball's movement using its x and y directions'''

        #first and fourth quadrant
        if x > 0:
            if y > 0:
                return math.atan(y / x)
            else:
                return math.atan(y / x) + 2 * math.pi
        #second and third quadrant
        elif x < 0:
            return math.atan(y / x) + math.pi
        # x = 0 is undefined for arctan
        else:
            if y > 0:
                return math.pi/2
            else:
                return 3 * math.pi/2


    def overlap(self):
        '''Return True if 2 balls overlap in the canvas'''

        for circle1 in self.circles_id:
            for circle2 in self.circles_id:
                if circle1 != circle2 and \
                        self.distance(circle1, circle2) <= \
                        (self.circles_id.get(circle1)[0] + self.circles_id.get(circle2)[0]):
                    self.overlaps = True
        return self.overlaps


    def move_circles(self):
        '''Movement of the balls in the frame using the generated direction for each ball'''

        for i in self.circles_id:
            dir_x = self.circles_id.get(i)[1]
            dir_y = self.circles_id.get(i)[2]
            self.canvas.move(i, dir_x, dir_y)
            self.canvas.update()


    def bounce(self):
        '''When a ball hits one of the 4 borders of the window, it bounces off according to their initial hit angle'''

        # x and y directions for a given ball
        for i in self.circles_id:
            dir_x = self.circles_id.get(i)[1]
            dir_y = self.circles_id.get(i)[2]

            #retrieve the initial coordinates of the ball
            x0, y0, x1, y1 = self.canvas.coords(i)

            #if it hits the left or right wall, reverse the x direction
            if x0 <= 10 or x1 >= self.WIDTH - 10:
                dir_x = -dir_x
                # update the x direction in the direction list to continue moving
                self.circles_id.get(i)[1] = dir_x
                #while x0 <= 0 or x1 >= self.SIZE:
                self.canvas.move(i, dir_x, dir_y)
                self.canvas.update()

            #if it hits the top or bottom wall, reverse the y direction
            if y0 <= 10 or y1 >= self.HEIGHT - 10:
                dir_y = -dir_y
                #update the y direction in the direction list to continue moving
                self.circles_id.get(i)[2] = dir_y
                #while y0 <= 0 or y1 >= self.SIZE:
                self.canvas.move(i, dir_x, dir_y)
                self.canvas.update()


    def collision(self):
        '''Check for collisions between 2 balls in the canvas. When 2 balls collide, they will bounce away as an elastic
        collision while conserving their momentum within the system involved'''

        for circle1 in self.circles_id:
            for circle2 in self.circles_id:

                #check if the distance between 2 distinct balls is smaller than the sum of their radius
                #if yes, it means collision
                #give a bit of space for collision to avoid bug when overlapping
                if -12 < self.distance(circle1, circle2) - \
                        (self.circles_id.get(circle1)[0] + self.circles_id.get(circle2)[0]) <= 0\
                        and circle1 != circle2:

                    #define initial x and y directions
                    x1 = self.circles_id.get(circle1)[1]
                    y1 = self.circles_id.get(circle1)[2]
                    x2 = self.circles_id.get(circle2)[1]
                    y2 = self.circles_id.get(circle2)[2]

                    #assume each ball weighs its radius squared with density pi^-1
                    m1 = (self.circles_id.get(circle1)[0]) ** 2
                    m2 = (self.circles_id.get(circle2)[0]) ** 2

                    #define initial speeds using the x and y directions
                    v1 = math.sqrt(x1 ** 2 + y1 ** 2)
                    v2 = math.sqrt(x2 ** 2 + y2 ** 2)

                    #define initial movement angles
                    theta1 = self.theta(x1, y1)
                    theta2 = self.theta(x2, y2)

                    #define the contact angle of the balls right before collision
                    phi = theta2 - theta1

                    # pi = pf (conservation of momentum)
                    #calculate the final x and y velocities after the collision
                    #source for the formula: https://en.wikipedia.org/wiki/Elastic_collision
                    x1 = ((v1 * math.cos(theta1 - phi) * (m1 - m2)) + 2 * m2 * v2 * math.cos(theta2 - phi)) \
                         * (math.cos(phi) / (m1 + m2)) + v1 * math.sin(theta1 - phi) * math.cos(phi + math.pi/2)
                    y1 = ((v1 * math.cos(theta1 - phi) * (m1 - m2)) + 2 * m2 * v2 * math.cos(theta2 - phi)) \
                         * (math.sin(phi) / (m1 + m2)) + v1 * math.sin(theta1 - phi) * math.sin(phi + math.pi/2)
                    x2 = ((v2 * math.cos(theta2 - phi) * (m2 - m1)) + 2 * m1 * v1 * math.cos(theta1 - phi)) \
                         * (math.cos(phi) / (m1 + m2)) + v2 * math.sin(theta2 - phi) * math.cos(phi + math.pi/2)
                    y2 = ((v2 * math.cos(theta2 - phi) * (m2 - m1)) + 2 * m1 * v1 * math.cos(theta1 - phi)) \
                         * (math.sin(phi) / (m1 + m2)) + v2 * math.sin(theta2 - phi) * math.sin(phi + math.pi/2)

                    #update the circles dictionary to make them continue moving after the collision
                    self.circles_id.get(circle1)[1] = x1
                    self.circles_id.get(circle1)[2] = y1
                    self.circles_id.get(circle2)[1] = x2
                    self.circles_id.get(circle2)[2] = y2

                    self.canvas.move(circle1, x1, y1)
                    self.canvas.move(circle2, x2, y2)
                    self.canvas.update()

                    #avoid pushing the ball out of the canvas when the collision happens near the canvas border
                    self.bounce()


    def gravity(self, a):
        '''Adds some gravity to the balls which attracts them to the ground'''

        for i in self.circles_id:
            vy = self.circles_id.get(i)[2]
            #kinematic equation: (vf = vi + a * t) to apply the acceleration to the velocity
            vy = vy + a / 5

            #update the y velocity after applying gravity
            self.circles_id.get(i)[2] = vy

            # avoid pushing the ball out of the canvas when the collision happens near the canvas border
            self.bounce()


    def air_resistance(self, air_density):
        '''Adds some air resistance to the balls which attracts them to the ground'''

        for i in self.circles_id:
            vx = self.circles_id.get(i)[1]
            vy = self.circles_id.get(i)[2]
            m = (self.circles_id.get(i)[0]) ** 2 / 1000
            cd = 1.05 #drag coefficient of a cube
            area = (self.circles_id.get(i)[0] / 1000) ** 2 * math.pi

            #calculate the air resistance
            #source for the formula: https://www.softschools.com/formulas/physics/air_resistance_formula/85/
            fx = (air_density * cd * area * vx ** 2) / 2
            fy = (air_density * cd * area * vy ** 2) / 2

            #calculate the acceleration
            ax = fx / m
            ay = fy / m

            # kinematic equation: (vf = vi + a * t) to apply the acceleration to the velocity
            vx = vx + ax / 5
            vy = vy + ay / 5

            # update the y velocity after applying gravity
            self.circles_id.get(i)[1] = vx
            self.circles_id.get(i)[2] = vy

            # avoid pushing the ball out of the canvas when the collision happens near the canvas border
            self.bounce()


    def drag(self):
        self.canvas.bind('<B1-Motion>', self.move_circles())


if __name__ == '__main__':
    Visual(sys.argv[1:]).mainloop()
