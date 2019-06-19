#!/usr/bin/env python
# coding=utf-8
import sys
import re
def fq2fa(fqname,faname):
	with open(fqname, 'r') as IN, open(faname,'w') as OUT:
		for i, line in enumerate(IN):
			if i % 4 == 0 or i % 4 == 1:
				line_change = re.sub(r'@', ">", line)
				OUT.write(line_change)
if (len(sys.argv)==3):
        fq2fa(sys.argv[1],sys.argv[2])
else:
        print("Usage: python3 fqname faname")
