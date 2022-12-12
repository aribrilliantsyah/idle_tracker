import time, schedule, pywinauto, pyautogui
from localStoragePy import localStoragePy
from sys import platform
from idle_time import IdleMonitor

localStorage = localStoragePy('idle-windows', 'sqlite')
def idletime():

    if platform == "win32":
        from ctypes import Structure,c_uint,sizeof,byref
        class LASTINPUTINFO(Structure):
            _fields_ = [('cbSize', c_uint), ('dwTime', c_uint)]
    
    def for_win():
        from ctypes import windll
        print(f"WINDOWS")

        lastinputinfo = LASTINPUTINFO()
        lastinputinfo.cbSize = sizeof(lastinputinfo)
        
        windll.user32.GetLastInputInfo(byref(lastinputinfo)) 
        timediff = windll.kernel32.GetTickCount() - lastinputinfo.dwTime
        idle = timediff/1000
        b_total_idle = localStorage.getItem("total_idle")
        
        if b_total_idle is None:
            b_total_idle = 0

        print(f"Before: {b_total_idle}")

        total_idle = float(b_total_idle) + idle
        localStorage.setItem("total_idle", total_idle)

        d = dict()
        d["cuur_idle"] = idle
        d["total_idle"] = total_idle
        return d
    
    def for_osx():
        d = dict()
        d["cuur_idle"] = 0
        d["total_idle"] = 0
        return d

    def for_linux():
        print(f"LINUX")

        monitor = IdleMonitor.get_monitor()
        idle = monitor.get_idle_time()
        curr_idle = idle
        b_total_idle = localStorage.getItem("total_idle")
        
        if b_total_idle is None:
            b_total_idle = 0

        print(f"Before: {b_total_idle}")

        total_idle = float(b_total_idle) + idle
        localStorage.setItem("total_idle", total_idle)
        
        d = dict()
        d["cuur_idle"] = curr_idle
        d["total_idle"] = total_idle
        return d

    if platform == "linux" or platform == "linux2":
        objidle = for_linux()
    elif platform == "darwin":
        objidle = for_osx()
    elif platform == "win32":
        objidle = for_win()
    else:
        objidle = None

    if objidle is not None: 
        total_idle = objidle.get("total_idle")
        curr_idle = objidle.get("cuur_idle")
        
        print(f"Current idle in seconds: {curr_idle}")
        print(f"Total idle in seconds: {total_idle}")

        if curr_idle > 20.0:
            if platform == "win32":
                print("WIN - Move Cursor")
                pywinauto.mouse.move(coords=(100, 10))
                pywinauto.mouse.move(coords=(100, 40))
                pywinauto.mouse.move(coords=(100, 10))
            elif platform == "linux" or platform == "linux2":
                print("LINUX - Move Cursor")
                pyautogui.moveTo(100, 500)
                pyautogui.moveTo(100, 100)
                pyautogui.moveTo(100, 500)

def listen(): 
    idletime()
    

schedule.every(10).seconds.do(listen) 

while 1:
    schedule.run_pending()
    time.sleep(1)