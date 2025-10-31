import numpy as np

A = np.array([[1.,1.],[4.,1.]])
b = np.array([4.],[2.])
A_inv = np.linalg.inv(A)
print(A_inv * b)