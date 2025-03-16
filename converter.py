import tkinter as tk
from tkinter import ttk

# Gauge lookup table (AWG to mm)
gauge_to_mm = {
    10: 2.59, 11: 2.30, 12: 2.05, 13: 1.83, 14: 1.63, 15: 1.45,
    16: 1.29, 17: 1.15, 18: 1.02, 19: 0.91, 20: 0.81, 21: 0.72,
    22: 0.64, 23: 0.57, 24: 0.51, 25: 0.46, 26: 0.41, 27: 0.36,
}

def mm_to_gauge(mm):
    """Finds the closest AWG gauge for a given wire diameter in mm."""
    return min(gauge_to_mm, key=lambda g: abs(gauge_to_mm[g] - mm))

def set_mode(mode):
    """Enable/Disable fields based on selected conversion mode."""
    entry_wire.config(state=tk.NORMAL if mode == "wire_outer_to_inner_gauge" else tk.DISABLED)
    entry_outer.config(state=tk.NORMAL if mode == "wire_outer_to_inner_gauge" else tk.DISABLED)
    entry_inner.config(state=tk.NORMAL if mode == "inner_gauge_to_wire_outer" else tk.DISABLED)
    entry_gauge.config(state=tk.NORMAL if mode == "inner_gauge_to_wire_outer" else tk.DISABLED)

    # Clear fields when switching modes
    clear_all()

    global conversion_mode
    conversion_mode = mode

def convert():
    """Handles conversions when the user clicks the button."""
    try:
        if conversion_mode == "wire_outer_to_inner_gauge":
            wire_dia = float(entry_wire.get())
            outer_dia = float(entry_outer.get())

            inner_dia = outer_dia - 2 * wire_dia
            gauge = mm_to_gauge(wire_dia)

            result_inner.config(text=f"{inner_dia:.2f} mm")
            result_gauge.config(text=f"{gauge} AWG")

        elif conversion_mode == "inner_gauge_to_wire_outer":
            inner_dia = float(entry_inner.get())
            gauge = int(entry_gauge.get())

            if gauge in gauge_to_mm:
                wire_dia = gauge_to_mm[gauge]
                outer_dia = inner_dia + 2 * wire_dia

                result_wire.config(text=f"{wire_dia:.2f} mm")
                result_outer.config(text=f"{outer_dia:.2f} mm")
            else:
                result_wire.config(text="Invalid AWG")
                result_outer.config(text="Invalid AWG")

    except ValueError:
        result_inner.config(text="Invalid Input")
        result_gauge.config(text="Invalid Input")
        result_wire.config(text="Invalid Input")
        result_outer.config(text="Invalid Input")

def clear_all():
    """Clears all input fields and result labels."""
    entry_wire.delete(0, tk.END)
    entry_outer.delete(0, tk.END)
    entry_inner.delete(0, tk.END)
    entry_gauge.delete(0, tk.END)
    result_inner.config(text="---")
    result_gauge.config(text="---")
    result_wire.config(text="---")
    result_outer.config(text="---")

# GUI Setup
root = tk.Tk()
root.title("Jump Ring Converter")
root.geometry("550x400")
root.configure(bg="#f4f4f4")

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TLabel", font=("Arial", 11), background="#f4f4f4")

# Default conversion mode
conversion_mode = "wire_outer_to_inner_gauge"

# Mode Selection
mode_frame = ttk.Frame(root, padding=10)
mode_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

ttk.Label(mode_frame, text="Select Conversion Mode:", font=("Arial", 12, "bold")).pack()

mode1_btn = ttk.Button(mode_frame, text="Wire + Outer → Inner + Gauge", command=lambda: set_mode("wire_outer_to_inner_gauge"))
mode1_btn.pack(pady=5, fill="x")

mode2_btn = ttk.Button(mode_frame, text="Inner + Gauge → Wire + Outer", command=lambda: set_mode("inner_gauge_to_wire_outer"))
mode2_btn.pack(pady=5, fill="x")

# Main Input Frame
frame = ttk.Frame(root, padding=10)
frame.grid(row=1, column=0, sticky="nsew")

ttk.Label(frame, text="Wire Diameter (mm):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_wire = ttk.Entry(frame, state=tk.NORMAL)
entry_wire.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Outer Diameter (mm):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_outer = ttk.Entry(frame, state=tk.NORMAL)
entry_outer.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame, text="Inner Diameter (mm):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_inner = ttk.Entry(frame, state=tk.DISABLED)
entry_inner.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame, text="Gauge (AWG):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
entry_gauge = ttk.Entry(frame, state=tk.DISABLED)
entry_gauge.grid(row=3, column=1, padx=5, pady=5)

# Convert & Clear Buttons
buttons_frame = ttk.Frame(frame)
buttons_frame.grid(row=4, column=0, columnspan=2, pady=10)
convert_btn = ttk.Button(buttons_frame, text="Convert", command=convert)
convert_btn.pack(side=tk.LEFT, padx=10)
clear_btn = ttk.Button(buttons_frame, text="Clear All", command=clear_all)
clear_btn.pack(side=tk.RIGHT, padx=10)

# Results Section
ttk.Label(frame, text="Inner Diameter:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
result_inner = ttk.Label(frame, text="---", font=("Arial", 11, "bold"))
result_inner.grid(row=5, column=1, padx=5, pady=5)

ttk.Label(frame, text="Gauge (AWG):").grid(row=6, column=0, sticky="w", padx=5, pady=5)
result_gauge = ttk.Label(frame, text="---", font=("Arial", 11, "bold"))
result_gauge.grid(row=6, column=1, padx=5, pady=5)

ttk.Label(frame, text="Wire Diameter:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
result_wire = ttk.Label(frame, text="---", font=("Arial", 11, "bold"))
result_wire.grid(row=7, column=1, padx=5, pady=5)

ttk.Label(frame, text="Outer Diameter:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
result_outer = ttk.Label(frame, text="---", font=("Arial", 11, "bold"))
result_outer.grid(row=8, column=1, padx=5, pady=5)

# Gauge Table on the Right
gauge_table = ttk.Treeview(root, columns=("AWG", "MM"), show="headings", height=10)
gauge_table.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

gauge_table.heading("AWG", text="Gauge (AWG)")
gauge_table.heading("MM", text="Diameter (mm)")

for gauge, mm in gauge_to_mm.items():
    gauge_table.insert("", "end", values=(gauge, mm))

# Set default mode
set_mode(conversion_mode)

# Run GUI
root.mainloop()
