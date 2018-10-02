import glob
import numpy as np

fns=glob.glob("*.out.txt")

sum4nums=np.array([0,0,0,0])
for fn in fns:
	for line in open(fn).read().rstrip().split("\n"):
		a=line.split("\t")
		if len(a)>1:
			temp=a[-4:]
	sum4nums=sum4nums+[int(i) for i in temp]

print sum4nums