import sys
import numpy as np
#import scipy
from scipy.sparse import csr_matrix, lil_matrix
import random
from random import randint
import pickle
import time


DAMP = 0.85
DANGLING_RANDOM_NBORS = 20
EPS = 0.0001

inp_dict = {}
n_nbors  = {}

with open(sys.argv[1]) as f:
    for line in f:
        line = line.split()
        assert(len(line) == 2)
        s, t = int(line[0]), int(line[1])
        try:
            inp_dict[s].append(t)
        except KeyError:
            inp_dict[s] = [t]

ITER = int(sys.argv[2])

keys = list(inp_dict.keys())
keys.sort()
assert(keys[0] == 0)
n = max([k for k in keys] + [e for lst_ in [lst for lst in inp_dict.values()] for e in lst_]) + 1

missing = []

for i in range(n):
    if i not in inp_dict:
        inp_dict[i] = []
        missing += [i]
        n_nbors[i] = 0
    n_nbors[i] = len(inp_dict[i])

print("create empty matrix")

matrix = lil_matrix((n, n))
print("m shape", matrix.shape)

print("fill matrix")
for u in inp_dict:
    nbors = inp_dict[u]
    for v in nbors:
        matrix[v, u] = 1. / n_nbors[u]

non_dangling = [i for i in range(n) if i not in missing]
for i in missing:
    for j in [random.sample(non_dangling, k=min(n, DANGLING_RANDOM_NBORS))]:
        matrix[j, i] = 1/(min(DANGLING_RANDOM_NBORS, n))

if n < 1000:
    print(matrix)

matrix = csr_matrix(matrix)

vec = np.matrix([1./n for _ in range(n)]).T
vec_saved = vec
print("start solving")
b = time.time()
for i in range(ITER):
    vec = matrix * vec * DAMP + ((1 - DAMP) / n)
    vec_saved = vec
    a = time.time()
    print("finish iter i", i+1, "in", a - b)
    b = a

print("iterations", i)
if n < 1000:
    print("output", vec)
print("this should be 1", sum(vec))

with open("test.pickle", "wb") as f:
    pickle.dump(vec, f)
