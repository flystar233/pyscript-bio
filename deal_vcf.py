from  collections import defaultdict
import re
import pandas as pd
import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.version_option(version='1.0.0')
@click.command('decode_vcf',help='Decode vcf file and order sample or change to genotype. Example: python vcf.py --vcf test.vcf --change_line T --select_line A141,L506')
@click.option("--vcf", type=click.Path(exists=True), help="vcf file")
@click.option("--change_line", type=click.Choice(['false','f','F','true','t','T']),default='false',help=" change the order of sample")	
@click.option("--select_line", type=str, default=False,help=" Sample name needed to be changed.(A141,L506) the first sample is the sample needed to be changed, the second sample will locate its next.")
@click.option("--vcf2genotype", type=click.Choice(['false','f','F','true','t','T']),default='false',help=" change the order of sample")
@click.option("-o","--outfile",default="out.txt",type=str,help="Output file (default 'out.txt')")
def decode_vcf(vcf,change_line,select_line,vcf2genotype,outfile):
	try:
		with open(vcf,'r') as IN,open('header.txt','w') as OUT:
			header = []
			raw_sample = ''
			bady = []
			bady_dict = defaultdict(list)

			for line in IN:  #extract header 
				if line.startswith('##'):
					header.append(line)
				elif line.startswith('#CHROM'):
					raw_sample += line
				else:
					bady.append(line)
			header = ''.join(header)
			all_sample = re.findall(r'FORMAT\t(.*)',raw_sample)[0].split() #extract sample name
			sample = raw_sample.split()

			for i in range(len(sample)): #extract sample variation
				for allsnp in bady:
					snp = allsnp.split()
					bady_dict[sample[i]].append(snp[i])
			data = pd.DataFrame(dict(bady_dict))
			######################################################################## fuction 1
			if change_line in ['true','t','T']: #change the order of sample
				col_need_change = select_line.split(',')[0]
				where_need_change =select_line.split(',')[1]
				data_need_change = data.loc[:,col_need_change]
				data=data.drop(col_need_change, axis=1)

				header_data = list(data.columns.values)
				loc = header_data.index(where_need_change)
	
				data.insert(loc, col_need_change,data_need_change)
				print("Received {} samples and {} snps...".format(data.shape[1]-9,data.shape[0]))

				OUT.write(header)
				data.to_csv(outfile,sep='\t',index=False)
			else:
				pass
			######################################################################### fuction 2
			if vcf2genotype in ['true','t','T']:
				pattern = {'GT':'K','AC':'M','AG':'R','CG':'S','CT':'Y','AT':'W','TG':'K','CA':'M','GA':'R','GC':'S','TC':'Y','TA':'W'}
				ann_data = data.iloc[:,[0,1,3]]
				df_change = pd.DataFrame() #crate all sample collector

				for i in range(len(all_sample)): #extract sample variation
					tmp = [] #crate per sample collector
					for allsnp in bady: #3:ref 4:alt 9:ann number
						snp = allsnp.split()
						if snp[i+9].split(':')[0] == '0/0':
							tmp.append(snp[3])
						elif snp[i+9].split(':')[0] == '0/1':
							locate = snp[3]+snp[4]
							tmp.append(pattern[locate])
						elif snp[i+9].split(':')[0] == '1/1':
							tmp.append(snp[4])
						elif snp[i+9].split(':')[0] == './.':
							tmp.append('-')
						else:
							pass
					df_change[all_sample[i]]=tmp

				vcf2genotype = ann_data.join(df_change)
				vcf2genotype.to_csv(outfile,sep='\t',index=False)
				print('Finish vcf2genotype!')
			else:
				pass
	except TypeError:
		print("Please input your option, or use --help")

if __name__ == "__main__":
	decode_vcf()	