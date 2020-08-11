import csv
from pathlib import Path
import sys
def features_draw(gff_list,out_script):
	with open(gff_list) as IN,open(out_script,'w') as OUT:
		OUT.write("from dna_features_viewer import GraphicFeature, GraphicRecord\n\n")
		filenames = IN.readlines()
		for name in filenames:
			name = name.strip()
			features_name =Path(name).stem
			OUT.write("features_"+features_name+"=[\n")
			with open(name) as GFFFILE:
				gff = csv.reader(GFFFILE,delimiter='\t')
				start,end = [],[]
				strand = ""
				for gfftext in gff:
					strand = gfftext[6]
					if gfftext[2] in ["CDS","exon"]:
						start.append(int(gfftext[3]))
						end.append(int(gfftext[4]))
				start.sort()
				end.sort()
				tmp_number = start[0] #init
				start = [i-tmp_number for i in start] #init
				end = [i-tmp_number for i in end] #init
				for double_pos in zip(start,end):
					feature = "GraphicFeature(start={}, end={}, strand={}1, color='#ccccff'),".format(double_pos[0],double_pos[1],strand)
					OUT.write("\t"+feature+"\n")
			OUT.write("]\n")
			OUT.write("record = GraphicRecord(sequence='',sequence_length={},features=features_{})\n".format(end[-1]+1,features_name))
			OUT.write("ax, _ = record.plot(figure_width=15)\nrecord.plot_sequence(ax)\n")
			OUT.write("ax.figure.savefig('{}.pdf', bbox_inches='tight')\n".format(features_name))

if (len(sys.argv)==3):
	features_draw(sys.argv[1],sys.argv[2])
else:
	print("Usage: python gff.list features_draw.py")
