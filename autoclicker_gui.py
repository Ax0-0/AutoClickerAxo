import customtkinter as ctk
import pyautogui
import threading
import time
import keyboard

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

clicking = False
click_button = 'left'
click_type = 'single'
delay = 0.1
keybind = 'f6'
keybind_ref = None
repeat_clicks = False
click_count = 1

# Fonction pour gérer les clics
def click_loop():
    global clicking
    apply_delay()
    if repeat_clicks:
        for _ in range(click_count):
            if not clicking:
                break
            pyautogui.click(button=click_button, clicks=1 if click_type == 'single' else 2)
            time.sleep(delay)
    else:
        while clicking:
            pyautogui.click(button=click_button, clicks=1 if click_type == 'single' else 2)
            time.sleep(delay)

def toggle_click():
    global clicking
    clicking = not clicking
    if clicking:
        threading.Thread(target=click_loop, daemon=True).start()

def start_click():
    global clicking
    if not clicking:
        clicking = True
        threading.Thread(target=click_loop, daemon=True).start()

def stop_click():
    global clicking
    clicking = False

def apply_delay():
    global delay
    try:
        hours = float(entry_hr.get()) * 3600
        mins = float(entry_min.get()) * 60
        secs = float(entry_sec.get())
        ms = float(entry_ms.get()) / 1000
        delay = hours + mins + secs + ms
    except ValueError:
        delay = 0.1

def set_left_click():
    global click_button
    click_button = 'left'
    left_btn.configure(fg_color="#3aa6ff")
    right_btn.configure(fg_color="#2d2d44")

def set_right_click():
    global click_button
    click_button = 'right'
    right_btn.configure(fg_color="#3aa6ff")
    left_btn.configure(fg_color="#2d2d44")

def set_click_type(choice):
    global click_type
    click_type = click_type_combo.get().lower()

def update_repeat_mode():
    global repeat_clicks
    repeat_clicks = repeat_mode.get() == 1

def update_click_count():
    global click_count
    try:
        click_count = int(entry_count.get())
    except ValueError:
        click_count = 1

def set_keybind():
    def capture_key(event):
        global keybind, keybind_ref
        keybind = event.name
        keybind_display.configure(text=keybind.upper())
        keybind_window.destroy()
        if keybind_ref:
            keyboard.remove_hotkey(keybind_ref)
        keybind_ref = keyboard.add_hotkey(keybind, toggle_click)

    keybind_window = ctk.CTkToplevel(app)
    keybind_window.title("Définir une touche")
    keybind_window.geometry("300x100")
    label = ctk.CTkLabel(keybind_window, text="Appuie sur une touche...", font=("Segoe UI", 14))
    label.pack(expand=True)
    keyboard.on_press(capture_key, suppress=True)

# Interface principale
app = ctk.CTk()
app.title("AutoClickerAxo")
app.geometry("530x480")
app.resizable(False, False)
import os
import sys
if hasattr(sys, '_MEIPASS'):
    icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
else:
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
app.iconbitmap(default=icon_path)

# Titre principal
ctk.CTkLabel(app, text="AutoClickerAxo", font=("Segoe UI", 24, "bold")).pack(pady=(15, 5))

# Cadre principal pour alignement vertical
main_frame = ctk.CTkFrame(app)
main_frame.pack(pady=5)

# Entrées délai
entry_frame = ctk.CTkFrame(main_frame)
entry_frame.pack(pady=10)

entry_hr = ctk.CTkEntry(entry_frame, width=80, height=35, font=("Segoe UI", 14), justify="center")
entry_min = ctk.CTkEntry(entry_frame, width=80, height=35, font=("Segoe UI", 14), justify="center")
entry_sec = ctk.CTkEntry(entry_frame, width=80, height=35, font=("Segoe UI", 14), justify="center")
entry_ms = ctk.CTkEntry(entry_frame, width=100, height=35, font=("Segoe UI", 14), justify="center")

entry_hr.insert(0, "0")
entry_min.insert(0, "0")
entry_sec.insert(0, "0")
entry_ms.insert(0, "100")

entry_hr.grid(row=0, column=0, padx=5)
entry_min.grid(row=0, column=1, padx=5)
entry_sec.grid(row=0, column=2, padx=5)
entry_ms.grid(row=0, column=3, padx=5)

labels = ["heures", "minutes", "secondes", "millisecondes"]
for i, txt in enumerate(labels):
    ctk.CTkLabel(entry_frame, text=txt).grid(row=1, column=i)

# Clic boutons horizontal
btn_click_frame = ctk.CTkFrame(main_frame)
btn_click_frame.pack(pady=5)

left_btn = ctk.CTkButton(btn_click_frame, text="Clic Gauche", command=set_left_click, corner_radius=20, width=160, height=40, font=("Segoe UI", 13, "bold"))
right_btn = ctk.CTkButton(btn_click_frame, text="Clic Droit", command=set_right_click, corner_radius=20, width=160, height=40, font=("Segoe UI", 13, "bold"))
left_btn.grid(row=0, column=0, padx=5)
right_btn.grid(row=0, column=1, padx=5)

click_type_combo = ctk.CTkComboBox(main_frame, values=["Single", "Double"], command=set_click_type, width=200, height=35, font=("Segoe UI", 12))
click_type_combo.set("Single")
click_type_combo.pack(pady=5)

# Répétition
repeat_frame = ctk.CTkFrame(main_frame)
repeat_frame.pack(pady=5)

repeat_mode = ctk.IntVar(value=0)
radio1 = ctk.CTkRadioButton(repeat_frame, text="Répéter x fois", variable=repeat_mode, value=1, command=update_repeat_mode)
entry_count = ctk.CTkEntry(repeat_frame, width=50, justify="center")
entry_count.insert(0, "1")
radio2 = ctk.CTkRadioButton(repeat_frame, text="Répéter jusqu'à arrêt", variable=repeat_mode, value=0, command=update_repeat_mode)

radio1.grid(row=0, column=0, padx=5)
entry_count.grid(row=0, column=1, padx=5)
radio2.grid(row=1, column=0, columnspan=2, pady=5)

# Keybind aligné horizontalement
keybind_frame = ctk.CTkFrame(main_frame)
keybind_frame.pack(pady=5)

btn_set_keybind = ctk.CTkButton(keybind_frame, text="Définir la touche", command=set_keybind, width=200, height=40, corner_radius=15, font=("Segoe UI", 12, "bold"))
keybind_display = ctk.CTkLabel(keybind_frame, text=keybind.upper(), font=("Segoe UI", 14), width=50, anchor="center")
btn_set_keybind.grid(row=0, column=0, padx=10)
keybind_display.grid(row=0, column=1)

# Start / Stop aligné horizontalement
startstop_frame = ctk.CTkFrame(main_frame)
startstop_frame.pack(pady=10)

start_btn = ctk.CTkButton(startstop_frame, text="Démarrer", fg_color="#3cb371", corner_radius=20, width=180, height=45, font=("Segoe UI", 13, "bold"), command=lambda:[update_click_count(), apply_delay(), start_click()])
stop_btn = ctk.CTkButton(startstop_frame, text="Arrêter", fg_color="#ff5f5f", corner_radius=20, width=180, height=45, font=("Segoe UI", 13, "bold"), command=stop_click)

start_btn.grid(row=0, column=0, padx=10)
stop_btn.grid(row=0, column=1, padx=10)

# Activation clavier
def register_hotkey():
    global keybind_ref
    if keybind_ref:
        keyboard.remove_hotkey(keybind_ref)
    keybind_ref = keyboard.add_hotkey(keybind, toggle_click)

register_hotkey()

# Affichage de la version en bas à droite
version_label = ctk.CTkLabel(app, text="v1.0", font=("Segoe UI", 10))
version_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

app.mainloop()
