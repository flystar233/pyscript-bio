#!/usr/bin/env python
# coding=utf-8
import re
import gzip
import bz2
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS) # turn on subcommand options
@click.version_option(version='1.0.0')
def entrance(): # defind the entrance of method
    pass

@click.command("fq2fa", help="fq 2 fa")
@click.option(
    "-i", "--fqname", type=click.Path(exists=True), help="the file of fq" )
@click.option(
    "-o", "--faname", type=str,default="result.fa.gz", help="the file of fa" , show_default=True)	
@click.option(
    "-t", "--seq_type", default="default", type=click.Choice(["gz","bz2","default"]), help="seq_type", show_default=True)
@click.option(
    "-l", "--level", type=int,default=5, help="compresslevel", show_default=True )

def fq2fa(fqname,faname,seq_type,level=5):
	if seq_type == "gz":
		with gzip.open(fqname, 'rt') as IN, gzip.open(faname,'wt',compresslevel=level) as OUT:
			for i, line in enumerate(IN):
                                if i % 4 == 0 or i % 4 == 1:
                                        line_change = re.sub(r'@', ">", line)
                                        OUT.write(line_change)
	elif seq_type == "bz2":
		with bz2.open(fqname, 'rt') as IN, gzip.open(faname,'wt',compresslevel=level) as OUT:
                        for i, line in enumerate(IN):
                                if i % 4 == 0 or i % 4 == 1:
                                        line_change = re.sub(r'@', ">", line)
                                        OUT.write(line_change)
	else:
		with open(fqname, 'rt') as IN, gzip.open(faname,'wt') as OUT:
			for i, line in enumerate(IN):
				if i % 4 == 0 or i % 4 == 1:
					line_change = re.sub(r'@', ">", line)
					OUT.write(line_change)

@click.command("length_fa", help="Calculate length of fa")
@click.option(
    "-i", "--faname", type=click.Path(exists=True), help="the file of fa")
@click.option(
    "-o", "--out", type=str,default="fa_stat.txt", help="result", show_default=True)
def length_fa(faname,out):
	with gzip.open(faname,'rt') as IN, open(out,'wt') as OUT:
		Dict = {}
		result=[]
		for line in IN:
			if line[0] == '>':
				key = line[1:-1]
				Dict[key] = []
			else:
				Dict[key].append(line.strip("\n"))
		for key, value in Dict.items():
			Dict[key] = ''.join(value)
		
		for key, value in Dict.items():			
			tmp_result = key+"\t"+str(len(value))
			result.append(tmp_result)
		result = "\n".join(result)
		OUT.write(result)

@click.command("length2_fa", help="Calculate length of fa,reduce memory usage")
@click.option(
    "-i", "--faname", type=click.Path(exists=True), help="the file of fa")
@click.option(
    "-o", "--out", type=str,default="fa_stat.txt", help="result")
def length2_fa(faname,out):
	with gzip.open(faname,'rt') as IN, open(out,'wt') as OUT:
		for line in IN:
			if line[0] == '>':
				keys=line[1:-1]
				OUT.write(keys)
			else:
				values=line.strip("\n")
				OUT.write("\t"+str(len(values))+"\n")
			
entrance.add_command(fq2fa)
entrance.add_command(length_fa)
entrance.add_command(length2_fa)

if __name__ == "__main__":
        entrance()
