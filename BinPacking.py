def count_bin(lst, C):
    return sum(1 for e in lst if e != C)

def find_best_idx(array, k, C):
    best = None
    best_space = C + 1
    for i in range(len(array)):
        remain = array[i] - k
        if remain >= 0 and remain < best_space:
            best_space = remain
            best = i
    return best

def first_fit(C, w):
    bins = [C] * len(w)
    used = 0

    for item in w:
        placed = False
        for i in range(used + 1):
            if bins[i] >= item:
                bins[i] -= item
                placed = True
                break
        if not placed:
            used += 1
            bins[used] -= item

    return count_bin(bins, C)

def best_fit(C, w):
    bins = [C] * len(w)
    used = 0

    for item in w:
        idx = find_best_idx(bins, item, C)
        if idx is not None and idx <= used:
            bins[idx] -= item
        else:
            used += 1
            bins[used] -= item

    return count_bin(bins, C)

def next_fit(C, w):
    bins = [C] * len(w)
    used = 0

    for item in w:
        if bins[used] >= item:
            bins[used] -= item
        else:
            used += 1
            bins[used] -= item

    return count_bin(bins, C)

n, C = map(int, input().split())
w = list(map(int, input().split()))

f = first_fit(C,w)
b = best_fit(C,w)
n = next_fit(C,w)
print(f,b,n)