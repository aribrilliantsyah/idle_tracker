import time, schedule, pywinauto
from localStoragePy import localStoragePy
from ctypes import Structure,windll,c_uint,sizeof,byref

localStorage = localStoragePy('idle-windows', 'json')
def idletime():
    class LASTINPUTINFO(Structure):
        _fields_ = [('cbSize', c_uint), ('dwTime', c_uint)]
    
    def get_idle_duration():
        lastinputinfo = LASTINPUTINFO()
        lastinputinfo.cbSize = sizeof(lastinputinfo)
        
        windll.user32.GetLastInputInfo(byref(lastinputinfo)) 
        timediff = windll.kernel32.GetTickCount() - lastinputinfo.dwTime
        idle = timediff/1000
        b_total_idle = localStorage.getItem("total_idle")
        
        if b_total_idle is None:
            b_total_idle = 0

        print(f"Before: {b_total_idle}")

        total_idle = float(b_total_idle) + idle;
        localStorage.setItem("total_idle", total_idle)

        d = dict()
        d["cuur_idle"] = idle
        d["total_idle"] = total_idle
        return d

    objidle = get_idle_duration()
    total_idle = objidle.get("total_idle")
    curr_idle = objidle.get("cuur_idle")
    
    print(f"Current idle in seconds: {curr_idle}")
    print(f"Total idle in seconds: {total_idle}")

    if curr_idle > 20.0:
        pywinauto.mouse.move(coords=(100, 10))
        pywinauto.mouse.move(coords=(100, 40))
        pywinauto.mouse.move(coords=(100, 10))

def listen(): 
    idletime()
    

schedule.every(10).seconds.do(listen) 

while 1:
    schedule.run_pending()
    time.sleep(1)