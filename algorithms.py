from heapq import heappop, heappush
import time

def swap(v, i, j):
    if i != j:
        v[i], v[j] = v[j], v[i]

def bubblesort(v):
    swapped = True
    for i in range(len(v) - 1):
        if not swapped:
            break
        swapped = False
        for j in range(len(v) - 1 - i):
            if v[j] > v[j + 1]:
                swap(v, j, j + 1)
                swapped = True
            yield v

def insertionsort(v):
    for i in range(1, len(v)):
        j = i
        while j > 0 and v[j] < v[j - 1]:
            swap(v, j, j - 1)
            j -= 1
            yield v

def heap_sort(v):
    heap = []
    for x in v:
        heappush(heap, x)
        yield heap
        time.sleep(0.03)

    ordered = []

    # While we have elements left in the heap
    while heap:
        ordered.append(heappop(heap))
        yield ordered
        time.sleep(0.05)

    yield ordered

def mergesort(v, start, end):
    if end <= start:
        return

    mid = start + ((end - start + 1) // 2) - 1
    yield from mergesort(v, start, mid)
    yield from mergesort(v, mid + 1, end)
    yield from merge(v, start, mid, end)
    yield v

def merge(v, start, mid, end):
    merged = []
    leftIdx = start
    rightIdx = mid + 1

    while leftIdx <= mid and rightIdx <= end:
        if v[leftIdx] < v[rightIdx]:
            merged.append(v[leftIdx])
            leftIdx += 1
        else:
            merged.append(v[rightIdx])
            rightIdx += 1

    while leftIdx <= mid:
        merged.append(v[leftIdx])
        leftIdx += 1

    while rightIdx <= end:
        merged.append(v[rightIdx])
        rightIdx += 1

    for i, sorted_val in enumerate(merged):
        v[start + i] = sorted_val
        yield v

def quicksort(v, start, end):
    if start >= end:
        return

    pivot = v[end]
    pivot_index = start

    for i in range(start, end):
        if v[i] < pivot:
            swap(v, i, pivot_index)
            pivot_index += 1
        yield v
    swap(v, end, pivot_index)
    yield v

    yield from quicksort(v, start, pivot_index - 1)
    yield from quicksort(v, pivot_index + 1, end)

def selectionsort(v):
    if len(v) == 1:
        return

    for i in range(len(v)):
        minVal = v[i]
        minIdx = i
        for j in range(i, len(v)):
            if v[j] < minVal:
                minVal = v[j]
                minIdx = j
            yield v
        swap(v, i, minIdx)
        yield v