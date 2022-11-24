import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from algorithms import swap, bubblesort, merge, mergesort, insertionsort, selectionsort, quicksort, heap_sort

def Sort(size, method):
    N = size
    method = method

    A = [x + 1 for x in range(N)]
    random.seed(time.time())
    random.shuffle(A)

    if method == "Bubble Sort":
        title = "Bubble sort"
        generator = bubblesort(A)
    elif method == "Insertion Sort":
        title = "Insertion sort"
        generator = insertionsort(A)
    elif method == "Merge Sort":
        title = "Merge sort"
        generator = mergesort(A, 0, N - 1)
    elif method == "Quicksort":
        title = "Quicksort"
        generator = quicksort(A, 0, N - 1)
    elif method == "Selection Sort":
        title = "Selection sort"
        generator = selectionsort(A)
    elif method == "Heap Sort":
        title = "Heap sort"
        generator = heap_sort(A)

    fig, ax = plt.subplots()
    ax.set_title(title)
    plt.style.use("fivethirtyeight")

    bar_rects = ax.bar(range(len(A)), A, align="edge")

    ax.set_xlim(0, N)
    ax.set_ylim(0, int(1.07 * N))

    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    iteration = [0]
    def update_fig(A, rects, iteration):
        for rect, val in zip(rects, A):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text(f'{iteration[0]} operations')

    anim = animation.FuncAnimation(fig, func=update_fig,
        fargs=(bar_rects, iteration), frames=generator, interval=5,
        repeat=False)

    plt.show()