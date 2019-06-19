#!/usr/bin/env python
# coding=utf-8

import os
import click
import re
'''
__author__ = 'xutengfei'
__author_email__ = 'xutengfei1@genomics.cn
Fuc: freebayes + bcftools snp calling piplines
Require python3+
'''

@click.command()
@click.option(
    "-r", "--reference", type=str, help="the file of reference genome"
    )
@click.option(
    "-l", "--listfile", type=str, help="Bam file list"
    )
@click.option(
    "-i","--imputation", default="false",type=click.Choice(['false','f','F','true','t','T'])
    )
@click.option(
    "-of", "--outfile_f", default="workf.sh", type=str, help="Output file (default 'workf.sh')")
@click.option(
    "-ob", "--outfile_b", default="workb.sh", type=str, help="Output file (default 'workb.sh')")

def command_line_runner(reference,listfile,outfile_f,outfile_b,imputation):

	try:
		with open(listfile,'r') as IN1, open(outfile_f,'w') as IN2, open(outfile_b,'w') as IN3:
			infile = IN1.readlines()
			chrom =re.findall(r'chr[0-9]+',infile[0])[0] # match chromosome of filename
			# freebayes piplines
			snpcalling_f = '/zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/freebayes/bin/freebayes '\
			'--use-best-n-alleles 4 -p 2 -f {} -L {} >freebayes.{}.vcf'.format(reference,listfile,chrom)
			out1file_f = 'freebayes.{}.vcf'.format(chrom)
			vcffilter_f = '/zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/freebayes/vcflib/bin/vcffilter '\
			'-f "TYPE = snp & QUAL >20  & DP > 10 & AC > 0 & SAF > 0 & SAR > 0 & RPL >0 & RPR >0" {} >filter.{}.vcf'.format(out1file_f,chrom)
			out2file_f = 'filter.{}.vcf'.format(chrom)
			vcftools_f = '/zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/vcftools_0.1.13/bin/vcftools  '\
			'--vcf {} --min-alleles 2.0 --max-alleles 2.0 --max-missing 0.95 --non-ref-af 0.05 --max-non-ref-af 0.95 --recode -c >finnal.{}.vcf'.format(out2file_f,chrom)
			out3file_f = 'finnal.{}.vcf'.format(chrom)
			change_spot_f = 'perl -pe "s/\\t.:/\\t.\/.:/g" {} >finnal2.{}.vcf'.format(out3file_f,chrom)
			out4file_f = 'finnal2.{}.vcf'.format(chrom)

			IN2.write(snpcalling_f+"\n")
			IN2.write(vcffilter_f+"\n")
			IN2.write(vcftools_f+"\n")
			IN2.write(change_spot_f+"\n")
			
			# bcftools piplines
			snpcalling_b = '/zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/miniconda/bin/bcftools mpileup -Ou --skip-indels -f {} -b {} '\
			'|/zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/miniconda/bin/bcftools call -P 1.1e-5 -Ob -mv -o bcftools.{}.bcf'.format(reference,listfile,chrom)
			out1file_b = 'bcftools.{}.bcf'.format(chrom)
			vcffilter_b = '/zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/miniconda/bin/bcftools filter -e "MQ < 40 || QUAL < 20 || DP <10 " -s LOWQUAL -Ou {} '\
			'|/zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/miniconda/bin/bcftools view -f PASS -Ov -o filter.{}.vcf'.format(out1file_b,chrom)
			out2file_b = 'filter.{}.vcf'.format(chrom)
			vcftools_b = '/zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/vcftools_0.1.13/bin/vcftools  --vcf {} '\
			'--min-alleles 2.0 --max-alleles 2.0 --max-missing 0.95 --non-ref-af 0.05 --max-non-ref-af 0.95 --recode -c >finnal.{}.vcf'.format(out2file_b,chrom)
			out3file_b = 'finnal.{}.vcf'.format(chrom)

			IN3.write(snpcalling_b+"\n")
			IN3.write(vcffilter_b+"\n")
			IN3.write(vcftools_b+"\n")
			
			if imputation in ['true','t','T']:
				impute_f = 'java -jar /zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/KIT/beagle.28Sep18.793.jar '\
				'gt={} out=imputation.{}.vcf'.format(out4file_f,chrom)
				impute_b = 'java -jar /zfssz3/NASCT_BACKUP/MS_PMO2017/xutengfei1/software/KIT/beagle.28Sep18.793.jar '\
				'gt={} out=imputation.{}.vcf'.format(out3file_b,chrom)
				IN2.write(impute_f+"\n")
				IN3.write(impute_b+"\n")
	except:
			print("Please input your option, or use --help")

if __name__ == "__main__":
        command_line_runner()
