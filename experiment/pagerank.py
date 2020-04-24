import sys
import numpy as np
#import scipy
from scipy.sparse import csr_matrix

ITER = 13
DAMP = 0.85

inp_dict = {}

with open(sys.argv[1]) as f:
    for line in f:
        line = line.split()
        assert(len(line) == 2)
        s, t = int(line[0]), int(line[1])
        try:
            inp_dict[s].append(t)
        except KeyError:
            inp_dict[s] = [t]

keys = list(inp_dict.keys())
keys.sort()
assert(keys[0] == 0)
n = max([k for k in keys]) + 1

for i in range(n):
    if i not in inp_dict:
        inp_dict[i] = []

print("create empty matrix")

matrix = csr_matrix((n, n))
print("m shape", matrix.shape)

print("fill matrix")
#wrong, only iterate over existing elements
for u in range(n):
    for v in range(n):
        if u in inp_dict[v]:
            matrix[u, v] = 1. / sum([1 for w in inp_dict[v]])
            matrix[u, v] = matrix[u, v] * DAMP + ((1 - DAMP) / n)

vec = np.matrix([1./n for _ in range(n)]).T
vec_saved = vec
print("start solving")
for i in range(ITER):
    vec = matrix * vec
    vec_saved = vec

print("iterations", i)
print("output", vec)
print("this should be 1", sum(vec))
