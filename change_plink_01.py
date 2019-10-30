import sys

def change_plink_01(infile):
	pattern = {'11':'-1', '22':'1','12':'0'}
	with open(infile,'r') as IN,open('result_01.txt','w') as OUT:
		for i in IN:
			tmp=[]
			i_len = len(i.strip())
			for aa in range(0,i_len,4):
				ii = i[aa]+i[aa+2]
				tmp.append(ii)
			rep = [pattern[x] if x in pattern else x for x in tmp]
			result = '\t'.join(rep)
			OUT.write(result)
			OUT.write('\n')
if (len(sys.argv)==2):
	change_plink_01(sys.argv[1])
else:
	print("Usage: python change_plink_01.py test.ped")