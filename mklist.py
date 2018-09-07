import sys
import os
import gzip
def mklist(path,flist):
	with open(flist,'wt') as OUT:
		files= os.listdir(path)
		OUT.write("#Chr"+"\t"+"Loci"+"\n")
		for file in files: 
			if not os.path.isdir(file):
				f = gzip.open(path+"/"+file,'rt')
				iter_f = iter(f)
				allf1 = [line.split() for line in iter_f]
				dic = {(k,int(v)):'value' for k,v,*z in allf1}
				for keys,values in sorted(dic.items()):
					OUT.write(keys[0]+"\t"+str(keys[1])+"\n")

if (len(sys.argv)==3):
	mklist(sys.argv[1],sys.argv[2])
else:
	print("Usage: python3 path out_file")
