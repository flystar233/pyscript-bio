#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
__author__ = 'xutengfei'
__author_email__ = 'xutengfei1@genomics.cn
Fuc: Compute the character with the highest frequency in the string.
'''

import sys
def max_word(in_file,out_file):

        with open(in_file,'r') as IN1, open(out_file,'w') as OUT:
                data = IN1.readlines()
                for i in data:
                        text = i.upper()
                        OUT.write(max(text, key=text.count)+"\t"+str(text.count(max(text, key=text.count))/(len(text)-1))+"\n")
if (len(sys.argv)==3):
        max_word(sys.argv[1],sys.argv[2])
else:
        print("Usage: python in_file  out_file")
