#!/usr/bin/env python
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.animation import FuncAnimation
import pandas as pd
import tailer as tl
import io
import random
from itertools import count


def plot_signal(canvas, filename):
    fig, ax = plt.subplots(1,1)
    fig.set_size_inches(5,3)
    fig.set_dpi(100)

    def animate(i):  
        with open(filename, 'r') as f:
            for i, l in enumerate(f):
                pass
        
        data = pd.read_csv(filename, skiprows=max(0,i-1000), names=['x_value', 'total_1'])
        
        x = data['x_value']
        y1 = data['total_1']
      
    
        ax.cla()
        ax.plot(x, y1, label='Channel 1')
      
        ax.legend(loc='upper left')
        fig.tight_layout()
        

    ani = FuncAnimation(fig, animate, interval=1000) 

    # ------------------------------- END OF YOUR MATPLOTLIB CODE -------------------------------

    # ------------------------------- Beginning of Matplotlib helper code -----------------------

    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        ani = FuncAnimation(figure, animate, interval=1000)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    return draw_figure(canvas, fig)
    

# ------------------------------- Beginning of GUI CODE -------------------------------

# # define the window layout
# layout = [[sg.Text('Plot test')],
#           [sg.Canvas(key='-CANVAS-')],
#           [sg.Button('Ok')],
#           [sg.Button('Clear')]]

# # create the form and show it without the plot
# window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True, element_justification='center', font='Helvetica 18')

# # add the plot to the window
# # fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
# fig_canvas_agg = None
# while True:
#     event, values = window.read()
#     if event=='Ok':
#         if fig_canvas_agg is not None:
#             fig_canvas_agg.get_tk_widget().pack_forget()
#         fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
#     elif event=='Clear':
#         fig_canvas_agg.get_tk_widget().pack_forget()
       
#     elif event==sg.WIN_CLOSED:
#         break




# window.close()
