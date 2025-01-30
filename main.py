import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import quad
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Button
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Parse signal parameters.')
    parser.add_argument('--sampling_rate', type=int, default=1000, help='Sampling rate of the signal (default: 1000)')
    parser.add_argument('--frequencies', type=str, default="2, 5, 8", help='Comma-separated list of frequencies')
    parser.add_argument('--shiftes', type=str, default="0, 0, 0", help='Comma-separated list of phase shifts in radians')
    
    args = parser.parse_args()
    
    if (args.frequencies is None) != (args.shiftes is None):
        parser.error("Both --frequencies and --shiftes must be provided together.")
    
    frequencies = list(map(float, args.frequencies.split(','))) if args.frequencies else []
    shiftes = list(map(lambda x: np.pi * float(x) / 180, args.shiftes.split(','))) if args.shiftes else []
    
    return args.sampling_rate, frequencies, shiftes


sampling_rate, frequencies, shiftes = parse_args()


time_points = np.linspace(0, 5, sampling_rate, endpoint=False)

signal_func = lambda t: np.sum([np.sin(2 * np.pi * f * t + s) for f, s in zip(frequencies, shiftes)], axis=0)

signal_points = np.sum([np.sin(2 * np.pi * f * time_points + s) for f, s in zip(frequencies, shiftes)], axis=0)

def wire_func(t, signal_func, winding_frequency):
    radius = signal_func(t)
    angle = 2 * np.pi * t * winding_frequency
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    return (x, y)

def compute_center_of_mass(signal_func, winding_frequency):
    x_cm, _ = quad(lambda t: signal_func(t) * np.cos(2 * np.pi * t * winding_frequency), 0, 1)
    y_cm, _ = quad(lambda t: signal_func(t) * np.sin(2 * np.pi * t * winding_frequency), 0, 1)
    return x_cm, y_cm

fig = plt.figure(figsize=(18, 10))

gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

ax3 = fig.add_subplot(gs[1, :])

ax1.plot(time_points, signal_points)
ax1.set_title('Исходный сигнал')
ax1.set_xlabel('Время (с)')
ax1.set_ylabel('Амплитуда')
ax1.grid(True)

line, = ax2.plot([], [], lw=2)
ax2.set_xlim(-5, 5)
ax2.set_ylim(-5, 5)
ax2.set_aspect('equal')
ax2.set_title('Намотанный сигнал')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.grid(True)

text = ax2.text(0.02, 0.95, '', transform=ax2.transAxes, fontsize=12, color='red')
cm_point, = ax2.plot([], [], 'bo', markersize=8)

vlines = [ax1.axvline(0, color='red', linestyle='--', lw=2) for _ in range(5)]

x_cm_values, y_cm_values = [], []
frame_values = []

line_x_cm, = ax3.plot([], [], 'b-', label='$x_{cm}$')
line_y_cm, = ax3.plot([], [], 'r-', label='$y_{cm}$')
line_x_sum_y_cm, = ax3.plot([], [], 'g-', label='$(x+y)_{cm}$')

ax3.set_xlim(0, 10)
ax3.set_ylim(-1, 1)
ax3.set_title('Координаты центра масс')
ax3.set_xlabel('Частота намотки (Гц)')
ax3.set_ylabel('Значение')
ax3.legend()
ax3.grid(True)

def init():
    global frame_values, x_cm_values, y_cm_values
    frame_values = []
    x_cm_values = []
    y_cm_values = []
    line.set_data([], [])
    text.set_text('')
    for vline in vlines:
        vline.set_xdata(0)
    cm_point.set_data(0, 0)
    line_x_cm.set_data([], [])
    line_y_cm.set_data([], [])
    line_x_sum_y_cm.set_data([], [])
    return line, text, cm_point, line_x_cm, line_y_cm, line_x_sum_y_cm, *vlines

def update(frame):
    winding_frequency = frame
    wire_mass_point = [wire_func(t, signal_func, winding_frequency) for t in time_points]
    wire_mass_point_x, wire_mass_point_y = zip(*wire_mass_point)
    
    line.set_data(wire_mass_point_x, wire_mass_point_y)
    
    x_cm, y_cm = compute_center_of_mass(signal_func, winding_frequency)
    cm_point.set_data(x_cm, y_cm)

    frame_values.append(winding_frequency)
    x_cm_values.append(x_cm)
    y_cm_values.append(y_cm)
    
    line_x_cm.set_data(frame_values, x_cm_values)
    line_y_cm.set_data(frame_values, y_cm_values)
    line_x_sum_y_cm.set_data(frame_values, np.array(x_cm_values) + np.array(y_cm_values))

    text.set_text(f'winding_frequency = {winding_frequency:.2f} Гц')
    
    if winding_frequency > 0:
        for i, vline in enumerate(vlines):
            vline.set_xdata(1 / winding_frequency * (i + 1))
    
    ax2.set_title(f'Намотанный сигнал (частота намотки: {winding_frequency:.2f} Гц)')
    return line, text, cm_point, line_x_cm, line_y_cm, line_x_sum_y_cm, *vlines

def restart(event):
    global ani
    ani.event_source.stop()

    ani = FuncAnimation(fig, update, frames=np.linspace(0, 10, 200), init_func=init, blit=True, interval=50, repeat=False)

    plt.draw()

ani = FuncAnimation(fig, update, frames=np.linspace(0, 10, 200), init_func=init, blit=True, interval=50, repeat=False)

ax_restart = fig.add_axes([0.9, 0.01, 0.08, 0.05])
button = Button(ax_restart, 'Restart')
button.on_clicked(restart)

plt.show()
