#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

'''
__author__ = 'xutengfei'
__author_email__ = 'xutengfei1@genomics.cn
Function:Mergie two files according to the same column,the key column must be first colnum.
if not,you can use shell command --cut and paste to transform your files.
'''
import sys

def join_file(first_file,second_file,out_file):

	with open(first_file,'r') as IN1, open(second_file,'r') as IN2, open(out_file,'w') as OUT:

		f1 = { k1:v for k1,*v in [l1.split() for l1 in IN1 ]}
		f2 = { k2:v for k2,*v in [l2.split() for l2 in IN2 ]}
		joinf = {k2 : f1[k2]+f2[k2]  for k2 in f2 if k2 in f1 }
		for key,value in joinf.items():
			OUT.write(key+'\t'+'\t'.join(value)+'\n')

if (len(sys.argv)==4):
	join_file(sys.argv[1],sys.argv[2],sys.argv[3])
else:
	print("Usage: python first_file(min) second_file(max) out_file")
