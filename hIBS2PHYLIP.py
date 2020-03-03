import sys
import numpy as np
if (len(sys.argv)==2):
	with open(sys.argv[1],'r') as IN, open("PHYLIP_need.txt",'w') as OUT:
		f_np = np.loadtxt(IN,delimiter='\t')
		result = abs((f_np-1)) #减一取绝对值
		np.savetxt(OUT,result,fmt="%.6f",delimiter="\t")
		print("Done!")
else:
	print("Usage: python hIBS2PHYLIP.py test.hIBS.kinf")