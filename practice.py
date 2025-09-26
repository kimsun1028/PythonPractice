import random

n = int(input("반복할 수를 입력하세요 : "))
b = 0
for i in range(n):
    a = random.randint(1,10)
    if a == 1:
        b+=1

print(f"{n} 번의 반복 중 {b} 번 성공 / 확률 : {b/n*100:.2f}%")