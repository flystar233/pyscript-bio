#!/usr/bin/env python
# coding=utf-8

import os
import csv
import click
import collections

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
	"""
	According to the results of GWAS, the genes of upstream and downstream 1M of SNP locus were selected.
	"""
	_VERSION = "1.1.1"
	try:
		print("--------------------------------------------\nLooking for genes...\nThe gene and iterative position will be saved in {}".format(out))
		mydcit = collections.defaultdict(list)
		posnow =[]
		iloc3 =[]
		iloc4 =[]
		iloc8 =[]
		with open(gff) as f,open(position) as pos:
			f_csv = csv.reader(f,delimiter='\t')
			for i in f_csv:
				iloc3.append(float(i[3])) #select position and gene
				iloc4.append(float(i[4]))
				iloc8.append(i[8])
			df_all = zip(iloc3,iloc4,iloc8)
			pos_csv = csv.reader(pos,delimiter='\t')
			for i in pos_csv:
				posnow.append(float(i[1]))
		
		outfile = open(out,'w')
		for z in df_all:
			for a in posnow:
				snp = int(a)
				snpdown = snp - width/2 #set downstream
				for i in range(0,width+1,1000):
					snpnow = snpdown +i
					if z[0] <= snpnow < z[1]:
						mydcit[z[2]].append(snpnow)
		outfile.write("gene\tposition\n")
		for key in mydcit.keys():
			outfile.write("{}\t{}\n".format(key,mydcit[key]))
		number = len(mydcit.keys())
		print("There are {} gene in {}".format(number,out))
	except FileNotFoundError:
		print("The file you inputed was not found")
	except:
		print("Please input your option, or use --help")
	
if __name__ == "__main__":
	command_line_runner()