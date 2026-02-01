import tkinter as tk
import re

def on_click(value):
    current = display.get()
    if current == "0":
        display.delete(0, tk.END)
        display.insert(0, value)
    else:
            # Otherwise, just append like normal
            display.insert(tk.END, value)

def calculate():
    try:
        result = eval(display.get())
        display.delete(0, tk.END)
        display.insert(0, str(result))
    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Error")

def clear():
    display.delete(0, tk.END)
    display.insert(0, "0")

# def backspace():
#     # Get the index of the very last character
#     last_char_index = len(display.get()) - 1
    
#     # Delete ONLY that one character
#     if last_char_index >= 0:
#         display.delete(last_char_index)

def backspace():
    current = display.get()
    display.delete(0, tk.END)
    
    # Slice the string
    new_value = current[:-1]
    
    # If the string is now empty or was "0", reset to "0"
    if new_value == "":
        display.insert(0, "0")
    else:
        display.insert(0, new_value)

# def percent():
#     try:
#         value = float(display.get())
#         display.delete(0, tk.END)
#         display.insert(0, value / 100)
#     except ValueError:
#         pass

def percent():
    expr = display.get()

    match = re.search(r'(.+)([+\-*/])(\d+\.?\d*)$', expr)
    if not match:
        # fallback: simple percent
        try:
            display.delete(0, tk.END)
            display.insert(0, float(expr) / 100)
        except ValueError:
            pass
        return

    left, op, right = match.groups()
    left_val = float(left)
    right_val = float(right)

    if op in "+-":
        result = left_val * (right_val / 100)
        final = left_val + result if op == "+" else left_val - result
    elif op == "*":
        final = left_val * (right_val / 100)
    elif op == "/":
        final = left_val / (right_val / 100)

    display.delete(0, tk.END)
    display.insert(0, str(final))

# Create window
root = tk.Tk()
root.configure(bg="darkgrey")
root.title("Calculator")
root.geometry("400x400")

# Display
display = tk.Entry(root, font=("Arial", 18), bg="white", fg="black", insertbackground="yellow", justify="right")
display.insert(0, "0")
display.pack(fill="x", padx=10, pady=10, ipady=10, expand=True)

# Buttons
buttons = [
    (None, "%", "C", "⌫"),
    ("7", "8", "9", "/"),
    ("4", "5", "6", "*"),
    ("1", "2", "3", "-"),
    ("0", ".", "=", "+"),
]

for row in buttons:
    frame = tk.Frame(root)
    frame.pack(expand=True, fill="both")
    for btn in row:
        if btn == "":
            tk.Label(frame, bg="black").pack(side="left", expand=True, fill="both")
            continue
        elif btn == "C":
            b = tk.Button(frame, text=btn, command=clear)
        elif btn == "⌫":
            b = tk.Button(frame, text=btn, command=backspace)
        elif btn == "%":
            b = tk.Button(frame, text=btn, command=percent)
        elif btn == "=":
            b = tk.Button(frame, text=btn, command=calculate)
        else:
            b = tk.Button(frame, text=btn, command=lambda v=btn: on_click(v))
        b.config(bg="grey", fg="yellow", activebackground="#544B4B")
        b.pack(side="left", expand=True, fill="both")

root.mainloop()
