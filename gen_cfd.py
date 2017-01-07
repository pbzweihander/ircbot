
from sentence_generator import calc_cfd
import pickle

doc = ""
cfd = []

with open("log.txt", 'r') as f:
    while True:
        line = f.readline()
        if not line: break
        doc += line

cfd = calc_cfd(doc)

with open("cfd.pkl", 'wb') as f:
    pickle.dump(cfd, f, -1)


