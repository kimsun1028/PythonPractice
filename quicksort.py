import sys
sys.setrecursionlimit(2000000)
input = sys.stdin.readline

def partition(pivotarray, array, lidx, ridx):
    if lidx >= ridx:
        return
    
    mid = (lidx + ridx) // 2
    a, b, c = array[lidx], array[mid], array[ridx]
    if a <= b <= c or c <= b <= a:
        pivot, pidx = b, mid
    elif b <= a <= c or c <= a <= b:
        pivot, pidx = a, lidx
    else:
        pivot, pidx = c, ridx

    array[lidx], array[pidx] = array[pidx], array[lidx]
    pivotarray.append(pivot)

    low, high = lidx + 1, ridx
    while True:
        while low <= high and array[low] < pivot:
            low += 1
        while high >= low and array[high] > pivot:
            high -= 1
        if low >= high:
            break
        array[low], array[high] = array[high], array[low]
        low += 1
        high -= 1

    array[lidx], array[high] = array[high], array[lidx]

    partition(pivotarray, array, lidx, high - 1)
    partition(pivotarray, array, high + 1, ridx)

if __name__ == "__main__":
    n = int(input())
    array = list(map(int, input().split()))
    pivotarray = []
    partition(pivotarray, array, 0, n - 1)
    sys.stdout.write("_".join(map(str, pivotarray)) + "\n")
    sys.stdout.write("_".join(map(str, array)) + "\n")
