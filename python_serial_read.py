import serial
import time
from datetime import datetime
import threading

now = datetime.now()
#FILENAME = "recording_{}_{}_{}_{}_{}_{}.csv".format(now.year, now.month, now.day, now.hour, now.minute, now.second)

def threadFunc():
   for i in range(5):
       print ('Hello from new Thread {}'.format(i))
       time.sleep(1)

def threadFunc2(timelst,lst,FILENAME):  
    # FILENAME = "recording_{}_{}_{}_{}_{}_{}.csv".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    with open(FILENAME, 'a+') as f:
        for i in range(len(lst)):
            f.write("{},{}\n".format(timelst[i],lst[i]))

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

def read_com(com_port,baudrate,FILENAME,stop_event):   
    ser = serial.Serial(com_port, baudrate)
    timelst = []
    lst = []
    
    rl = ReadLine(ser)
    cyl=0
    i_t=0
    start_time = time.time()
    while cyl<3600*24 and (not stop_event.is_set()):           
        rcv = rl.readline().strip()
        # print (rcv)
        rcv = rcv.decode('utf-8', errors='ignore')
        if 'Hello' not in rcv:
            # print (rcv)
            try:
                num = int(rcv)
            except:
                break
            # timelst.append(int(round(time.time() * 1000)))
            timelst.append(i_t)
            i_t+=1
            lst.append(num)
            # print (time.time(), num)
            if len(lst) > 999:                
                cyl += 1
                print (stop_event.is_set(), cyl)
                # x = threading.Thread(target=threadFunc2, args=(timelst,lst,FILENAME,))
                # x.start()
                with open(FILENAME, 'a') as f:
                    for i in range(len(lst)):
                        f.write("{},{}\n".format(timelst[i],lst[i]))
                lst = []
                timelst = []
    
    ser.close()
    print ("Port closed")
                # print (num)
        

    # print(rl.readline())
if __name__ == "__main__":
    # x = threading.Thread(target=threadFunc)
    # x.start()
    FILENAME = "recording_{}_{}_{}_{}_{}_{}.csv".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    read_com('COM14',FILENAME)