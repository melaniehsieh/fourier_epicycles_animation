import math

from matplotlib.patches import Circle
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt 

class CircleWave:
    def __init__(self, center, wave, point_on_wave = 0, parent = None):
        if parent == None:
            self.center = center
        else:
            self.center = [parent.x + parent.r, parent.y + parent.r]
        self.r = wave.amp
        self.x, self.y = self.center[0], self.center[1]
        self.wave = wave
        self.wv_point = point_on_wave

        self.circle_patch = Circle(self.center, radius = self.r, color = (1,0,0,0.2))
        self.child = None

    def update_pos(self):
        self.x = self.center[0]
        self.y = self.center[1]
        self.circle_patch.center = self.center

    def plot_circle(self, ax):
        ax.add_patch(self.circle_patch)

    def plot_vector(self, ax, theta):
        ax.plot([self.x, self.x + self.r*math.cos(theta)], \
                [self.y, self.y + self.r*math.sin(theta)], '--', color = 'black')

        ax.plot(self.x + self.r*math.cos(theta), self.y + self.r*math.sin(theta), 'o', color = 'black')

        point = [self.x + self.r*math.cos(theta),  self.y + self.r*math.sin(theta)]

        if (self.child != None):
            self.child.center = point
            self.child.update_pos()
        
        return point

class SineWave:
    def __init__(self, amp, omega, velocity, color):
        self.amp = amp
        self.omg = omega
        self.c = velocity
        self.color = color

        self.func = lambda x, t: self.amp*math.sin(self.omg*(x - self.c*t))
        
    def plot_wave(self, ax, x_values, t):
        y = [self.func(x, t) for x in x_values]
        ax.plot(x_values, y, '-', color = self.color)

class CosineWave:
    def __init__(self, amp, omega, velocity, color):
        self.amp = amp
        self.omg = omega
        self.c = velocity
        self.color = color

        self.func = lambda x, t: self.amp*math.cos(self.omg*(x - self.c*t))
        
    def plot_wave(self, ax, x_values, t):
        y = [self.func(x, t) for x in x_values]
        ax.plot(x_values, y, '-', color = self.color)

class TanWave:
    def __init__(self, amp, omega, velocity, color):
        self.amp = amp
        self.omg = omega
        self.c = velocity
        self.color = color

        self.func = lambda x, t: self.amp*math.tan(self.omg*(x - self.c*t))
        
    def plot_wave(self, ax, x_values, t):
        y = [self.func(x, t) for x in x_values]
        ax.plot(x_values, y, '-', color = self.color)

class FourierSeriesWave:
    def __init__(self, waves, bigcircle_x = -10, point_on_wave = 0):
        self.waves = sorted(waves, key = lambda x: x.amp, reverse=True)  

        self.circles = [CircleWave([bigcircle_x,0], self.waves[0], point_on_wave)]
        for wave in self.waves[1:]:
            circle = CircleWave([0,0], wave, point_on_wave, parent = self.circles[-1])
            self.circles[-1].child = circle
            self.circles.append(circle)

    def plot(self, ax, x_values, t):
        for circle in self.circles:
            circle.plot_circle(ax)
            theta = circle.wave.omg*(circle.wv_point - circle.wave.c*t)
            point = circle.plot_vector(ax, theta) 

        for wave in self.waves:
            wave.plot_wave(ax, x_values, t)

        wave_sum = [sum([wave.func(x, t) for wave in self.waves]) for x in x_values]
        ax.plot(x_values, wave_sum, '-', lw = 1.5, color = 'black')

        wave_sum_yp = sum([wave.func(0, t) for wave in self.waves]) 
        ax.plot([point[0], 0], [point[1], wave_sum_yp], '--', color = (0.2, 0.2, 0.2, 0.5))
            
        return point

fig, ax = plt.subplots()

time_points = [0 + 500*i/100000 for i in range(100001)] 
n_time = len(time_points)

#multiple waves
wave = SineWave(2, 8, 7, color = (0,0,1,0.3))
wave_2 = CosineWave(1, 2, 10, color = (0,1,0,0.3))
wave_3 = TanWave(3, 2, 1, color = (1,0,0,0.3))
wave_4 = SineWave(0.5, 3, 7.5, color = (0,1,1,0.3))
waves = [wave, wave_2, wave_3]

# square wave
# waves = [CosineWave(1.2*(10/((i)*math.pi)), i, 15, color = (0,0,1,0.2)) for i in range(1, 10, 2)]

# sawtooth wave
# waves = [CosineWave(3*(3/((i)*math.pi)), i, 20, color = (0,1,0,0.3)) for i in range(1, 9)]

x = [0 + 10*math.pi*i/5000 for i in range(5001)]

fourier_series = FourierSeriesWave(waves)

draw_points_x = []
draw_points_y = []

def animate(frame):
    ax.cla()
    ax.axis('equal')

    t = time_points[frame]

    point = fourier_series.plot(ax, x, t)
    draw_points_x.append(point[0])
    draw_points_y.append(point[1])

    ax.plot(draw_points_x, draw_points_y, '-', color = (0,0,1,0.8))
    equation_title = "2sin(8x - 7t) + cos(2x - 10t) + 3tan(2x - t) + 0.5sin(3x - 7.5t)"
    ax.set_title(equation_title, color = 'black')

    ax.set_xlim([-20, 20])
    ax.set_ylim([-10, 10])
    
plt.pause(3)
animation = FuncAnimation(fig, animate, frames = range(n_time), repeat = False, interval = 50)

plt.show()

