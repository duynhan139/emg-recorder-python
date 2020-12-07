import PySimpleGUI as sg      
from serial.tools import list_ports

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
    
        [sg.Text('Select port'), sg.InputCombo(com_ports, size=(7, 1), default_value='COM1'), sg.Text('Baud rate'), sg.InputCombo((9600, 500000), size=(10, 1))]],            
        title='Options',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],      
   
    [       
        sg.Listbox(values=['Select gesture'], enable_events=True, size=(30,17), key="-FILE LIST-", default_values='Select gesture'),
        sg.Image(r"300x300.png", key="-IMAGE-"),
        sg.Canvas(size=(500,300), background_color='white', key='-CANVAS-')
    ],
    [sg.Text('_'  * 80)],    
   
    [sg.Text('Save to', size=(15, 1), auto_size_text=False, justification='right'),      
        sg.InputText('./'), sg.FolderBrowse()],      

        [sg.Button('Record'), sg.Button('Stop')],

]      



window = sg.Window('Everything bagel', layout, default_element_size=(40, 1), grab_anywhere=False, element_justification='c')      

event, values = window.read()      

window.close()    

sg.popup('Title',      
            'The results of the window.',      
            'The button clicked was "{}"'.format(event),      
            'The values are', values)      