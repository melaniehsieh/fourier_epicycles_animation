import math

from matplotlib.patches import Circle
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class CircleWave:
    def  __init__(self, center, wave, point_on_wave = 0, parent = None):
        if parent == None:
            self.center = center
        else:
            self.center = [parent.x + parent.r, parent.y + parent.x]
        self.r = wave.amp
        self.x, self.y = self.center[0], self.center[1]
        self.wave = wave
        self.wv_point = point_on_wave
    
        self.circle_patch = Circle(self.center, radius = self.r, color = (1,0,0,0.3))
        self.child = None

    def update_pos(self):
        self.x = self.center[0]
        self.y = self.center[1]
        self.circle_patch.center = self.center

    def plot_circle(self, ax):
        ax.add_patch(self.circle_patch)
        
    def  plot_vector(self, ax, theta):
        ax.plot([self.x, self.x + self.r*math.cos(theta)], \
                [self.y, self.y + self.r*math.sin(theta)], '--', color = "black")

        ax.plot(self.x +  self.r*math.cos(theta), self.y + self.r*math.sin(theta), 'o', color = (0,0,1,0.5))
        
        point = [self.x +  self.r*math.cos(theta), self.y + self.r*math.sin(theta)]

        if self.child != None:
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

    def  plot_wave(self, ax, x_values, t):
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

    def  plot(self, ax, x_values, t):
        for circle in self.circles:
            circle.plot_circle(ax)
            theta = circle.wave.omg*(circle.wv_point - circle.wave.c*t)
            point = circle.plot_vector(ax,theta)

        for wave in self.waves:
            wave.plot_wave(ax, x_values, t)

        wave_sum = [sum([wave.func(x, t) for wave in self.waves]) for x in x_values]
        ax.plot(x_values, wave_sum, '-', lw = 2, color = 'black')

        wave_sum_yp = sum([wave.func(0, t) for wave in self.waves])
        ax.plot([point[0], 0], [point[1], wave_sum_yp], '--', color = (0.2, 0.2, 0.2, 0.5))

        return point

fig, ax = plt.subplots()

time_points = [0 + 100*i/10000 for i in range(10001)]
n_time = len(time_points)

wave = SineWave(3, 5, 1, color = (0,0.1,0.3))
wave_2 = SineWave(2, 5.5, 5, color = (0.1,0,0.3))
waves = [wave, wave_2]

x = [0 + 10*math.pi*i/1000 for i in range(1001)]

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

    ax.plot(draw_points_x, draw_points_y, '-', color = 'purple')

    ax.set_xlim([-20, 20])
    ax.set_ylim([-10, 10])
    
animation = FuncAnimation(fig, animate, frames = range(n_time), repeat = False, interval = 50)
