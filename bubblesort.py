def BubbleSort(array):
	sort = 0
	n = len(array)
	for i in range(n-1):
		issort = False
		for j in range(n-i-1):
			if array[j] > array[j+1]:
				issort = True
				sort+=1
				array[j],array[j+1] = array[j+1],array[j]
				string = ""
				for m in range(n):
					string += str(array[m])
					if m != n-1:
						string += "_"	
				print(string)
		if i == 0 and not issort:
			print("x")
	print(str(sort))


n = int(input())
array = list(map(int, input().split()))
BubbleSort(array)