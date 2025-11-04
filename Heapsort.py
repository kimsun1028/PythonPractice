def Heapsort(array):
    n = len(array) -1
    
    for i in range(n // 2, 0, -1):
        Downheap(array, n,i) 

    heapsize = n
    for i in range(1,n):
        array[1],array[heapsize] = array[heapsize],array[1]
        printing(array)
        heapsize -= 1
        Downheap(array,heapsize,1)

def Downheap(array,heapsize,i):
    rootidx = i
    n = heapsize

    while True:
        left = 2*rootidx
        right = 2*rootidx + 1

        
        hasleft =  left <= n
        hasright = right <= n

        
        if hasleft and hasright:
            childm =  max([(array[left],left), (array[right],right)], key = lambda x: x[0])
            if childm[0] > array[rootidx]:
                array[rootidx],array[childm[1]] = array[childm[1]],array[rootidx]
                rootidx = childm[1]
                
            else:
                break
        elif hasleft and not hasright:
            childm = (array[left],left)
            if childm[0] > array[rootidx]:
                array[rootidx],array[childm[1]] = array[childm[1]],array[rootidx]
                rootidx = childm[1]
                
            else:
                break
        else:
            break
            

def printing(array):
    n = len(array)
    string = ""
    for m in range(1,n):
        string += str(array[m])
        if m != n-1:
            string += "_"	
    print(string)





n = int(input())
array1 = list(map(int, input().split()))
array1.insert(0, None)
Heapsort(array1)