try:
    import keyboard
    import pygetwindow as pw
    import pyautogui
    import os
    import time
    import ctypes
    import sys
    import subprocess
except (ImportError, ImportWarning) as imeimw:
    print(imeimw)
    quit()

def screenshot(file_name: str, app_title: str, path):
    path = path.strip()

    if path == None:
        print("what is your path?????")
        quit("jump.")

    if path.__contains__(r"\ ".strip()):
        path = path.replace(r"\ ".strip(), "/")

    tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, a,b,c = time.gmtime()
    timestamp = f"{tm_year}{tm_mon:02}{tm_day:02}-{tm_hour:02}{tm_min:02}{tm_sec:02}"

    def unique_path(filepath: str) -> str:
        if not os.path.exists(filepath):
            return filepath
        base, ext = os.path.splitext(filepath)
        counter = 1
        while os.path.exists(f"{base} ({counter}){ext}"):
            counter += 1
        return f"{base} ({counter}){ext}"

    def _screenshot(fname):
        file_name = unique_path(f"{path}/{fname}")

        try:
            win = pw.getWindowsWithTitle(app_title)[0]
            os.makedirs(path, exist_ok=True)
            screenshot = pyautogui.screenshot(region=(win.left, win.top, win.width, win.height))
            screenshot.save(file_name, "png")
            return win, file_name
        except Exception as exce:
            print("exception(_screenshot): ", exce, "\nif list index is out of range this means the application is not running (mostlikely)")
            try:
                app_title.lower()
                win = pw.getWindowsWithTitle(app_title)[0]
                os.makedirs(path, exist_ok=True)
                screenshot = pyautogui.screenshot(region=(win.left, win.top, win.width, win.height))
                screenshot.save(file_name, "png")
                return win
            except:
                print("| not even lower case worked. . .")
                time.sleep(3)
                quit()
    
    base = file_name[:-4] if file_name.endswith(".png") else file_name 
    final = f"{base}_{timestamp}.png"
    w, fn = _screenshot(final)
    return fn

def check_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def run_if_admin():
    if check_admin():
        return True
    else:
        if "--elevated" in sys.argv:
            print("did not get admin")
            time.sleep(2)
            sys.exit(1)
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            " ".join([sys.argv[0]] + sys.argv[1:] + ["--elevated"]),
            None,
            1
        )
        sys.exit(0)

amount = 0
if __name__ == "__main__":
    running = True
    if run_if_admin():
        name = input("Input a file name >>> ")
        app_name = input("Input the app name (look in task manager if needed) >>> ")
        file = input("Input a file path where the images will save >>> ")

        if name == "":
            name = "_NIL"
        if app_name == "" or file == "":
            print("one of the inputs is empty. . . retry")
            time.sleep(1.5)
            quit(1)
        
        print("\npress period '.' to take a screenshot \n| press ctrl + comma to stop running without closing the application\n")

        while running:
            if keyboard.is_pressed("."):                                         # to take a screenshot
                amount += 1
                f = screenshot(name.strip(), app_name.strip(), fr"{file}")
                print(f"screenshot !   I|I   times: {amount}   I|I   file: {f}")
            if keyboard.is_pressed('ctrl+comma'):                                # to stop
                print("stopped (pressed keybind)")
                time.sleep(1.345)
                running = False

            time.sleep(0.03432567890014144404)
