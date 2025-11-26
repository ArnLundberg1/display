import tkinter as tk
from tkinter import messagebox
import json

# -----------------------------
# Ladda config-filer
# -----------------------------
with open("lines_config.json", "r", encoding="utf-8") as f:
    lines_data = json.load(f)

with open("keybinds_config.json", "r", encoding="utf-8") as f:
    keybinds_data = json.load(f)

with open("stopbutton_config.json", "r", encoding="utf-8") as f:
    stopbutton_data = json.load(f)

# -----------------------------
# Huvudapplikation
# -----------------------------
class BusDisplayApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SL Buss Display")
        self.configure(bg="#0b1a2b")  # mörkblå bakgrund
        self.attributes("-fullscreen", True)

        self.current_line = None
        self.current_station_index = 0
        self.stopping = False

        self.create_home_screen()
    
    # -------------------------
    # Hemskärm med linjeval
    # -------------------------
    def create_home_screen(self):
        self.clear_screen()
        tk.Label(self, text="Välj linje", font=("Arial", 48, "bold"), bg="#0b1a2b", fg="yellow").pack(pady=50)
        for line in lines_data:
            btn = tk.Button(self, text=f"{line['number']} → {line['destination']}", 
                            font=("Arial", 36), width=20, 
                            command=lambda l=line: self.start_line(l))
            btn.pack(pady=10)
    
    # -------------------------
    # Starta vald linje
    # -------------------------
    def start_line(self, line):
        self.current_line = line
        self.current_station_index = 0
        self.stopping = False
        self.create_display_screen()
    
    # -------------------------
    # Display för linjen
    # -------------------------
    def create_display_screen(self):
        self.clear_screen()
        
        # Panel för linje/destination
        self.line_label_shadow = tk.Label(self, text=f"{self.current_line['number']} → {self.current_line['destination']}",
                                         font=("Arial Black", 64, "bold"), bg="#0b1a2b", fg="black")
        self.line_label_shadow.place(relx=0.5, y=80, anchor="center")
        self.line_label = tk.Label(self, text=f"{self.current_line['number']} → {self.current_line['destination']}",
                                   font=("Arial Black", 64, "bold"), bg="#0b1a2b", fg="yellow")
        self.line_label.place(relx=0.5, y=78, anchor="center")  # offset för shadow-effect
        
        # Nästa hållplats
        self.station_label = tk.Label(self, text=self.current_line['stations'][self.current_station_index],
                                      font=("Courier New", 60, "bold"), bg="#0b1a2b", fg="white")
        self.station_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Knappar
        btn_frame = tk.Frame(self, bg="#0b1a2b")
        btn_frame.pack(side="bottom", pady=20)
        
        # Vanliga knappar
        for idx, btn in enumerate(keybinds_data):
            action = btn["action"]
            if action == "prev_station":
                command = self.prev_station
            elif action == "next_station":
                command = self.next_station
            elif action == "home":
                command = self.create_home_screen
            else:
                command = lambda: None
            b = tk.Button(btn_frame, text=btn["label"], font=("Arial", 24), width=12, command=command)
            b.grid(row=0, column=idx, padx=10)
        
        # Stoppknappar
        for idx, btn in enumerate(stopbutton_data):
            action = btn["action"]
            if action == "stop_pressed":
                command = self.stop_pressed
            else:
                command = lambda: None
            b = tk.Button(btn_frame, text=btn["label"], font=("Arial", 24), width=12, bg="red", fg="white", command=command)
            b.grid(row=0, column=len(keybinds_data)+idx, padx=10)
    
    # -------------------------
    # Byt till nästa station med slide upp
    # -------------------------
    def next_station(self):
        if not self.stopping and self.current_station_index < len(self.current_line['stations']) - 1:
            self.current_station_index += 1
            self.slide_station_up(self.current_line['stations'][self.current_station_index])
    
    def prev_station(self):
        if not self.stopping and self.current_station_index > 0:
            self.current_station_index -= 1
            self.slide_station_up(self.current_line['stations'][self.current_station_index], reverse=True)
    
    # -------------------------
    # Slide upp-animation
    # -------------------------
    def slide_station_up(self, text, reverse=False):
        # Skapa ny label ovanför/bakom
        new_label = tk.Label(self, text=text, font=("Courier New", 60, "bold"), bg="#0b1a2b", fg="white")
        start_y = 600 if reverse else -100  # start utanför skärmen
        new_label.place(relx=0.5, y=start_y, anchor="center")
        
        self.animate_slide_up(new_label, target_y=self.winfo_height()/2)
    
    def animate_slide_up(self, label, target_y):
        current_y = label.winfo_y()
        step = -20 if current_y > target_y else 20
        if abs(current_y - target_y) > 5:
            label.place(y=current_y + step)
            self.after(20, lambda: self.animate_slide_up(label, target_y))
        else:
            label.place(y=target_y)
            self.station_label.destroy()
            self.station_label = label
    
    # -------------------------
    # Stoppknapp (STANNAR visas statiskt)
    # -------------------------
    def stop_pressed(self):
        self.stopping = True
        self.station_label.config(text="STANNAR")
    
    # -------------------------
    # Rensa skärmen
    # -------------------------
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = BusDisplayApp()
    app.mainloop()
