from tkinter import *
from tkinter import ttk
from sorts import Sort

def Start():
    size = sizeEntry.get()
    method = selected_algorithm.get()
    return Sort(size, method)

root = Tk()
root.title('Vis-Sort')
root.maxsize(1000, 800)
root.config(bg='black')

selected_algorithm = StringVar()
data = []

UI_frame = Frame(root, width= 900, height=600, bg='grey')
UI_frame.grid(row=0, padx=10, pady=5)

Label(UI_frame, text="Algorithm: ", bg='grey').grid(row=0, column=0, padx=5, pady=5, sticky=W)
algMenu = ttk.Combobox(UI_frame, textvariable=selected_algorithm, values=['Bubble Sort', 'Merge Sort', 'Insertion Sort', 'Selection Sort', 'Quicksort', 'Heap Sort'])
algMenu.grid(row=0, column=1, padx=5, pady=5)
algMenu.current(0)
Button(UI_frame, text="Start", command=Start, bg='red').grid(row=1, column=0, padx=5, pady=5)

sizeEntry = Scale(UI_frame, from_=25, to=100, resolution=3, orient=HORIZONTAL, label="Data Size")
sizeEntry.grid(row=1, column=1, padx=5, pady=5)

root.mainloop()