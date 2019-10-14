#!/usr/bin/env python
# coding=utf-8

import os
from datatable import Frame,fread
import click
from collections import defaultdict

'''
__author__ = 'xutengfei'
__author_email__ = 'xutengfei1@genomics.cn
Fuc: According to the results of GWAS, the genes of upstream and downstream 1M of SNP locus were selected.
'''

@click.command()
@click.option(
    "-g", "--gff", type=str, help="gff file (It can only contain one chromosome.)"
    )
@click.option(
    "-p", "--position", type=str, help="chromosome name and snp position file(chr1  123456789)"
    )
@click.option(
    "-w", "--width", default=1000000, type=int, help="Total length of upstream and downstream of SNP locus (default 1M)"
)
@click.option(
    "-o",
    "--out",
    default="out.txt",
    type=str,
    help="Output file (default 'out.txt')")

def command_line_runner(gff,position,width,out):
	_VERSION = "1.0.0"
	try:
		print("--------------------------------------------\nLooking for genes...\nThe gene and iterative position will be saved in {}".format(out))
		mydcit = defaultdict(list)
		df  = fread(gff,sep='\t',header=False)
		pos = fread(position,sep='\t',header=False)
		outfile = open(out,'w')
		df3=df[:,3].to_list()[0]
		df4=df[:,4].to_list()[0]
		df8=df[:,8].to_list()[0]
		df_all = zip(df3,df4,df8) #crate a zip include df3 df4 df8
		posnow = pos[:,1].to_list()[0]
		df_all2 = zip(df3,df4,df8)

		for z in df_all2:
			for a in posnow:
				snp = int(a)
				if z[0] <= snp < z[1]:
					print("\nsnp {} in {}".format(snp,z[2]))
				else:
					pass
		for z in df_all:
			for a in posnow:
				snp = int(a)
				snpdown = snp - width/2 #set downstream
				for i in range(0,width+1,100): #step=100,related with the gap of genes
					snpnow = snpdown +i
					if z[0] <= snpnow < z[1]:
						mydcit[z[2]].append(snpnow)
#		outfile.write("gene\tposition\n")
		for key in mydcit.keys():
			outfile.write("{}\t{}\n".format(key,mydcit[key]))
		number = len(mydcit.keys())
		print("Work done,there are {} gene in file {}".format(number,out))
	except:
		print("Please input your option, or use --help")
	
if __name__ == "__main__":
	command_line_runner()

