import gzip
import sys
def selectSNP(infile,outfile):
	with gzip.open(infile,'rt') as f ,gzip.open(outfile,'wt') as OUT:
		f1 = [l1.split() for l1 in f ]
		for info in f1:
			if(float(info[4]) >= 20 and (float(info[13])<=300 and float(info[13]) >=3) and float(info[14]) >= 0.05 and float(info[15]) <= 1.5 and info[2] != info[3]):
				OUT.write('\t'.join(info)+'\n')
			else:
				pass

if (len(sys.argv)==3):
	selectSNP(sys.argv[1],sys.argv[2])
else:
	print("Usage: python3 infile outfile")
