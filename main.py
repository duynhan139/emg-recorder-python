import PySimpleGUI as sg      
import matplotlib
matplotlib.use('TkAgg')
from serial.tools import list_ports
from python_serial_read import read_com
from datetime import datetime
import threading
import time
import os

from signal_plot import plot_signal

sg.theme('Dark Grey 9')      

# ------ Menu Definition ------ #      
menu_def = [['File', ['Open', 'Save', 'Exit', 'Properties']],                       
            ['Help', 'About...'], ]      

# ------ Column Definition ------ #      
column1 = [[sg.Text('Column 1', background_color='#F7F3EC', justification='center', size=(10, 1))],      
            [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],      
            [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],      
            [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]      

ports = list_ports.comports()
com_ports = []
for port, desc, hwid in sorted(ports):
    # print("{}: {} [{}]".format(port, desc, hwid))
    if 'COM' in port:
        com_ports.append(port)

#('COM1', 'COM2')

layout = [      
    [sg.Menu(menu_def, tearoff=True)],      
    [sg.Text('Demo - EMG signal recording', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],    
  
    [sg.Frame(layout=[      
    
        [sg.Text('Select port'), sg.InputCombo(com_ports, size=(7, 1), enable_events=True, key='-COM-', default_value='COM11'), 
        sg.Text('Baud rate'), sg.InputCombo([9600, 500000], enable_events=True, key='-BAUD-', size=(10, 1), default_value=500000)]],            
        title='Options',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],      
   
    [       
        sg.Listbox(values=['Select gesture'], enable_events=True, size=(30,17), key="-FILE LIST-", default_values='Select gesture'),
        sg.Image(r"300x300.png", key="-IMAGE-"),
        sg.Canvas(size=(500,300), background_color='white', key='-CANVAS-')
    ],
    [sg.Text('_'  * 80)],    
   
    [sg.Text('Save to', size=(15, 1), auto_size_text=False, justification='right'),      
        sg.InputText('./', key='-PATHTEXT-'), sg.FolderBrowse(key='-PATH-')],      

        [sg.Button('Record', enable_events=True, key='-RECORD-'), 
        sg.Button('Stop', enable_events=True, key='-STOP-')],

]      



window = sg.Window('Everything bagel', layout, default_element_size=(40, 1), grab_anywhere=False, element_justification='c')      
p1 = 1
stop_event= threading.Event()
fig_canvas_agg = None
while True:
    event, values = window.read()      

    if event == '-COM-':
        print (values["-COM-"])
    elif event == '-PATH-':
        window['-PATHTEXT-'].update(values['-PATH-'])
    elif event == '-RECORD-':
        timeout = False
        if (values["-COM-"]) != "" and (values["-BAUD-"]) != "":           
            now = datetime.now()
            FILENAME = "recording_{}_{}_{}_{}_{}_{}.csv".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
            FILENAME = os.path.join(values['-PATHTEXT-'], FILENAME)
            stop_event.clear()
            t1 = threading.Thread(target=read_com, args=(values["-COM-"], int(values["-BAUD-"]), FILENAME,stop_event,), daemon=True)
            t1.start()
            # p1 = multiprocessing.Process(target=read_com, args=(values["-COM-"], int(values["-BAUD-"]), FILENAME,))
            # p1.start()
            # read_com(values["-COM-"], int(values["-BAUD-"]), FILENAME)
            start_time = time.time()
            while not os.path.exists(FILENAME) and (time.time()-start_time<5):
                pass
            if time.time() - start_time >= 5 and (not os.path.exists(FILENAME)):
                timeout=True
            time.sleep(1)
            if fig_canvas_agg is not None:               
                fig_canvas_agg.get_tk_widget().pack_forget()
            if not timeout:
                fig_canvas_agg = plot_signal(window['-CANVAS-'].TKCanvas, FILENAME)               
        else:
            sg.popup('Please specifiy port and baud rate!')
    elif event == '-STOP-':
        print (stop_event.is_set())
        stop_event.set()
        print (stop_event.is_set())
        if fig_canvas_agg is not None:
            fig_canvas_agg.get_tk_widget().pack_forget()     
    elif event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()    

  