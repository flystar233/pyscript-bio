import csv
import sys
import argparse
def turn(arr):
	row = len(arr)
	col = len(arr[0])
	B = []
	for j in range(col):
		A = []
		list2 = [i for i in range(row)]
		for i in list2[::-1]:
			A.append(arr[i][j])
		B.append(A)
	return B
def stat():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("-i", "--input", action="store", dest="filename", required=True,help="Name of file")
	parser.add_argument("-c", "--caculate",  type =str, dest = "caculate",help = "statistical method",required=True)
	parser.add_argument("-f", "--form", action="store", dest="form",default = 'col', choices=['col', 'row'],help="col or row")
	parser.add_argument("-H", "--header",  type =str, dest = "Header",help = "Header or not",default ='False',choices=['False','True'])
	args = parser.parse_args()
	filename = args.filename
	form = args.form
	Header = args.Header
	stat = args.caculate
	with open(filename) as IN:
		myfile = csv.reader(IN,delimiter='\t')
		count = 0
		if Header=='True':
			next(myfile)
		if form =='row':
			if stat=='sum':
				for num in myfile:
					count+=1
					print(count,":",sum([int(i) for i in num if i.isdigit()]))
			elif stat=='mean':
				for num in myfile:
					count+=1
					print(count,":",sum([int(i) for i in num if i.isdigit()])/len(num))
			elif stat=='min':
				for num in myfile:
					count+=1
					print(count,":",min([int(i) for i in num if i.isdigit()]))
			elif stat=='max':
				for num in myfile:
					count+=1
					print(count,":",max([int(i) for i in num if i.isdigit()]))
			print("So there are {} rows".format(count))
		elif form =='col':
			tmp = []
			for num in myfile:
				tmp.append(num)
			reault_col = turn(tmp)
			if stat=='sum':
				for index,col in enumerate(reault_col,start=1):
					mydata = [int(i) for i in col if i.isdigit()]
					if mydata !=[]:
						print(index,":",sum(mydata))
					else:
						print(index,":",'NA')
			elif stat=='mean':
				for index,col in enumerate(reault_col,start=1):
					mydata = [int(i) for i in col if i.isdigit()]
					mylen = len(mydata)
					mysum = sum(mydata)
					try:
						print(index,":",mysum/mylen)
					except ZeroDivisionError:
						print(index,":",'NA')
			elif stat=='min':
				for index,col in enumerate(reault_col,start=1):
					tmp = [int(i) for i in col if i.isdigit()]
					try:
						print(index,":",min(tmp))
					except ValueError:
						print(index,":",'NA')
			elif stat=='max':
				for index,col in enumerate(reault_col,start=1):
					tmp = [int(i) for i in col if i.isdigit()]
					try:
						print(index,":",max(tmp))
					except ValueError:
						print(index,":",'NA')
			print("So there are {} cols".format(len(reault_col)))


if __name__=="__main__":
	stat()
