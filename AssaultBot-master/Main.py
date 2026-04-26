from Utils import *
import keyboard
import tkinter as tk
from threading import Thread
import win32gui, time

# Variabili di stato
aim_on, esp_on, lines_on, god_on, ammo_on = False, False, False, False, False
draw_list = []

def cheat_loop():
    global aim_on, esp_on, lines_on, god_on, ammo_on, draw_list
    print("\n" + "="*40)
    print("      ASSAULTBOT 1.3.0.2 - READY")
    print("="*40)
    print("[Q] Aimbot         [L] ESP Boxes")
    print("[O] ESP Lines      [T] God Mode")
    print("[Y] Inf. Ammo      [C] Teleport to Enemy")
    print("[K] Mass Kill      [DEL] Exit")
    print("="*40 + "\n")

    while True:
        try:
            if keyboard.is_pressed('q'):
                aim_on = not aim_on
                print(f">> Aimbot: {'ON' if aim_on else 'OFF'}")
                time.sleep(0.3)
            if keyboard.is_pressed('l'):
                esp_on = not esp_on
                print(f">> ESP Box: {'ON' if esp_on else 'OFF'}")
                time.sleep(0.3)
            if keyboard.is_pressed('o'):
                lines_on = not lines_on
                print(f">> Lines: {'ON' if lines_on else 'OFF'}")
                time.sleep(0.3)
            if keyboard.is_pressed('t'):
                god_on = not god_on
                print(f">> God Mode: {'ON' if god_on else 'OFF'}")
                time.sleep(0.3)
            if keyboard.is_pressed('y'):
                ammo_on = not ammo_on
                print(f">> Ammo: {'ON' if ammo_on else 'OFF'}")
                time.sleep(0.3)
            if keyboard.is_pressed('k'):
                print(">> EXTERMINATING...")
                mass_kill_score()
                time.sleep(0.3)
            if keyboard.is_pressed('c'):
                print(">> TELEPORTING...")
                teleport_to_closest()
                time.sleep(0.3)

            # Esecuzione funzioni
            if aim_on: silent_aim()
            if god_on: procID.write_int(entity_base_address + entity.health_offset, 999999)
            if ammo_on: procID.write_int(entity_base_address + entity.ammo_offset, 999)

            if esp_on or lines_on:
                hwnd = win32gui.FindWindow(None, "AssaultCube")
                if hwnd:
                    r = win32gui.GetWindowRect(hwnd)
                    draw_list = get_esp_data(r[2]-r[0], r[3]-r[1])
            else: draw_list = []
            
            if keyboard.is_pressed('delete'): break
            time.sleep(0.01)
        except: continue

def overlay():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True, "-transparentcolor", "black")
    root.config(bg="black")
    canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    def draw():
        canvas.delete("all")
        hwnd = win32gui.FindWindow(None, "AssaultCube")
        if hwnd:
            r = win32gui.GetWindowRect(hwnd)
            w, h = r[2]-r[0], r[3]-r[1]
            root.geometry(f"{w}x{h}+{r[0]}+{r[1]}")
            for p in draw_list:
                if 0 < p['x'] < w and 0 < p['y'] < h:
                    if esp_on: canvas.create_rectangle(p['x']-15, p['y']-15, p['x']+15, p['y']+15, outline="red", width=2)
                    if lines_on: canvas.create_line(w/2, h, p['x'], p['y'], fill="red", width=1)
        root.after(10, draw)
    draw()
    root.mainloop()

if __name__ == '__main__':
    Thread(target=cheat_loop, daemon=True).start()
    overlay()