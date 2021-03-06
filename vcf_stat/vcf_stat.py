import csv
import re
import click
import gzip
from  collections import defaultdict

pattern = {'GT':'K','AC':'M','AG':'R','CG':'S','CT':'Y','AT':'W','TG':'K','CA':'M','GA':'R','GC':'S','TC':'Y','TA':'W'}
def decomment(csvfile):
    for row in csvfile:
        raw = row.split('##')[0].strip()
        if raw: yield raw

@click.command()
@click.option(
    "-f", "--vcf", type=click.Path(exists=True), help="vcf file"
    )
@click.option(
    "-s", "--select", default="a", type=str, help="The number of alleles is one(a) or two(other)", show_default=True)
@click.option(
    "-p", "--pdf", default="True", type=str, help="make plot ", show_default=True)
@click.option(
    "-v", "--outfile1", default="out.vcf",type=str, help="streamlined vcf file",show_default=True)
@click.option(
    "-g", "--outfile2", default="out.geno", type=str, help="genotype file ", show_default=True)
@click.option(
    "--sample_name", default="False", type=str, help="The sample order of heatmap")
@click.option(
    "--start", default=0, type=int, help="the position of start")
@click.option(
    "--end", default=1, type=int, help="the position of end")
def vcf_stat(vcf,outfile1,outfile2,sample_name,select,pdf,start,end):
	try:
		if vcf.endswith('gz'):
			opener = gzip.open
		else:
			opener = open
		with opener(vcf,'rt') as IN,open(outfile1,'w') as OUT1,open(outfile2,'w') as OUT2,open('stat.txt','w') as OUT3:
			f_csv = csv.reader(decomment(IN),delimiter='\t') # skip annoation(##)
			header = next(f_csv) # skip annoation(#)
			CHR = header[0]
			POS = header[1]
			RFF = header[3]
			ALT = header[4]
			SAMPLE_list = header[9:]
			SAMPLE = '\t'.join(SAMPLE_list)
			OUT1.write(CHR+'\t'+POS+'\t'+RFF+'\t'+ALT+'\t'+SAMPLE+'\n')
			OUT2.write(CHR+'\t'+POS+'\t'+RFF+'\t'+ALT+'\t'+SAMPLE+'\n')
			snp_count = defaultdict(int)
			snp_count2 = defaultdict(list)
			snp_count3 = defaultdict(int)
			position = []
			snp_list = []
			for i in f_csv:
				sample = ' '.join(i[9:])
				sample_tmp = re.findall(r'(./.)',sample)
				snp_list.append(sample_tmp)
				position.append(int(i[1]))
				locate = i[3]+i[4]
				snp_count[locate] += 1 # count genotype

				snp_count2[locate].append(sample_tmp.count('0/0')) # count genotype in every sample
				snp_count2[locate].append(sample_tmp.count('0/1'))
				snp_count2[locate].append(sample_tmp.count('1/1'))

				for subscript,sam in enumerate(sample_tmp):
					if sam=='0/1':
						snp_count3[SAMPLE_list[subscript]]+=1
				########################################################
				geno = []
				if select == 'a': #simple
					for ii in sample_tmp:
						if ii == '0/0':
							geno.append(i[3])
						elif ii == '0/1':
							geno.append(pattern[locate])
						elif ii == '1/1':
							geno.append(i[4])
						elif ii == './.':
							geno.append('-')
						else:
							pass
				else: #double
					for ii in sample_tmp:
						if ii == '0/0':
							geno.append(i[3]+i[3])
						elif ii == '0/1':
							geno.append(i[3]+i[4])
						elif ii == '1/1':
							geno.append(i[4]+i[4])
						elif ii == './.':
							geno.append('--')
						else:
							pass
				sample_vcf = '\t'.join(sample_tmp)
				sample_geno = '\t'.join(geno)
				subject_vcf = i[0]+'\t'+i[1]+'\t'+i[3]+'\t'+i[4]+'\t'+sample_vcf+'\n'
				subject_geno = i[0]+'\t'+i[1]+'\t'+i[3]+'\t'+i[4]+'\t'+sample_geno+'\n'
				OUT1.write(subject_vcf)
				OUT2.write(subject_geno)
			#############################################################
			final_dict = {}
			for key,value in snp_count2.items():
				number_aa = 0
				number_Aa = 0
				number_AA = 0
				for count in range(0,len(value),3): # add aa Aa AA
					number_aa += value[count]
				for count in range(0,len(value),3):
					number_Aa += value[count+1]
				for count in range(0,len(value),3):
					number_AA += value[count+2]
				final_dict[key[0]+' --> '+key[1]]=[number_aa,number_Aa,number_AA]

			snp_type = snp_count.keys()
			snp_type = [i[0]+' --> '+i[1] for i in snp_type]
			snp_number = snp_count.values()
			snp_tuple = []
			for i in zip(snp_type,snp_number):
				snp_tuple.append(i)
			snp_tuple = sorted(snp_tuple, key=lambda x: x[1]) #sort by snp number
			snp_type = [i[0] for i in snp_tuple]
			snp_number = [i[1] for i in snp_tuple]
			heatmap_list = []
			for i in snp_type[::-1]:
				heatmap_list.append(final_dict[i])

			OUT3.write(f'The number of samples: {len(SAMPLE_list)}\n')
			OUT3.write(f'The number of SNP: {sum(snp_count.values())}\n')
			OUT3.write('Heterozygosity rate per sample:\n')
			for sample,heter in snp_count3.items():
				OUT3.write(f'    {sample}: {heter/sum(snp_count.values())*100:0.2f}%\n')
			OUT3.write('The number of variation type:\n')
			for result in zip(snp_type,snp_number):
				OUT3.write(f'    {result[0]}: {result[1]}\n')
			############################################################# heatmap
			if end > 1:
				import pandas as pd
				import matplotlib.pyplot as plt
				assert end > start,"Start should't less than end"
				for i in range(0,1000000,1):
					if start not in position:
						start +=1
					else:
						start_subscript = position.index(start)
						break
				for i in range(0,1000000,1):
					if end not in position:
						end -=1
					else:
						end_subscript = position.index(end)
						break
				snp_list = snp_list[start_subscript:end_subscript+1]
				tran_snp_list = []
				for site in snp_list:
					tmp = []
					for snp in site: # transform
						if snp =='./.':
							snp=0
						elif snp =='0/0':
							snp=1
						elif snp =='0/1':
							snp=2
						elif snp =='1/1':
							snp=1
						tmp.append(snp)
					tran_snp_list.append(tmp)
				df = pd.DataFrame(tran_snp_list,columns=SAMPLE_list).T
				if sample_name!='False':
					sample_order = open(sample_name)
					sample_list = [i.strip() for i in sample_order.readlines()]
					df = df.reindex(index=sample_list[::-1]) # Custom sample order
				else:
					df = df.reindex(index=SAMPLE_list[::-1])
				fig = plt.figure(figsize=(15,5))
				ax = fig.add_subplot(1,1,1)
				plt.pcolormesh(df,cmap=plt.cm.binary)
				ax.yaxis.set_ticks([])
				ax.spines['top'].set_visible(False)
				ax.spines['right'].set_visible(False)
				ax.spines['left'].set_visible(False)
				plt.savefig('haplotype.pdf')
			####################################### make pdf
			if pdf =='True':
				import matplotlib.pyplot as plt
				fig = plt.figure(figsize=(10,10))
				plt.style.use('ggplot')
				plt.subplots_adjust(wspace =0)
				ax = fig.add_subplot(1,2,2)
				plt.barh(range(len(snp_type)),snp_number,tick_label=list(snp_type),color=['royalblue'])
				plt.xlabel('snp number',{'family' : 'Arial','weight' : 'normal','size' : 12})
				ax.xaxis.get_major_formatter().set_powerlimits((0,1)) #kexuejishu
				ax.yaxis.set_ticks_position('right') 
				plt.tick_params(labelsize=12)

				plt.subplot(1,2,1)
				ax2 = fig.add_subplot(1,2,1)
				im = plt.imshow(heatmap_list, cmap=plt.cm.hot_r,interpolation='none')
				cbaxes = fig.add_axes([0.08, 0.75, 0.02, 0.2]) #set colorbar position
				xx = plt.colorbar(im,cbaxes)
				#plt.xticks(range(3), ['aa','Aa','AA'])
				plt.tick_params(labelsize=12)
				ax2.yaxis.set_ticks([])
				ax2.xaxis.set_ticks([])
				plt.tight_layout()
				plt.savefig("snp_count.pdf")
			else:
				pass
	except FileNotFoundError:
		print("The file you inputed was not found")
	except:
		print("Please input your option, or use --help")
if __name__ == "__main__":
	vcf_stat()
