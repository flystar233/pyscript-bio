import argparse
"""
Data Structure:
The chromosome name is the key, and all mRNAs under a single chromosome are the values and stored in a list, 
each individual mRNA is nested in the list, each individual mRNA is taken as the first value by the mRNA line in the gff file,
and its cds are sorted sequentially.

Exameple:
{'NC_000001.11': 
    [[[17300, 17700], [17369, 17436], [17450, 17472], [17510, 17600]], 
    [[18300, 18700], [18369, 18436], [18450, 18472], [18510, 18600]]], 
'NC_000001.22': 
    [[[17300, 17700], [17369, 17436], [17450, 17472], [17510, 17600]],
    [[18300, 18700], [18369, 18436], [18450, 18472], [18510, 18600]]]}
"""
def get_mRNA_list(gff_file):
    mRNA_list = {}
    sort_mRNA_list={}
    with open(gff_file, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                line = line.strip().split()
                chromosome = line[0]
                feature = line[2]
                start = int(line[3])
                end = int(line[4])
                if chromosome not in mRNA_list:
                    mRNA_list[chromosome] = []
                if feature == "mRNA":
                    mRNA_list[chromosome].append([])
                mRNA_list[chromosome][-1].extend([[start, end]])
    
    for key,value in mRNA_list.items(): #sort mRNA list to pinpoint the order of exons
        sort_list=[]
        for single_mRNA in value:
            sort_single_mRNA = sorted(single_mRNA,key=lambda x: x[0])
            sort_list.append(sort_single_mRNA)
        sort_mRNA_list[key] = sort_list
    return sort_mRNA_list

                
def get_snp_location(snp_chromosome,snp_position,mRNA_list):
    if snp_chromosome in mRNA_list:
        specified_chromosome_data=mRNA_list[snp_chromosome]
        for mrna_index,mRNA in enumerate(specified_chromosome_data):
            mRNA_quantity=len(specified_chromosome_data)
            if mRNA[0][0]<=snp_position<=mRNA[0][1]:
                CDS_quantity=len(mRNA)-1 # Count the number of CDS
                for cds_index,pos in enumerate(mRNA[1:]):
                    if pos[0]<=snp_position<=pos[1]:
                        print(f'{snp_chromosome}\t{snp_position}\texon ({cds_index+1})')
                        break
                    else:
                        if cds_index+1 < CDS_quantity:
                            pass
                        else:
                            print(f'{snp_chromosome}\t{snp_position}\tintron')
                            break
                break
            else:
                if mrna_index+1 < mRNA_quantity:
                    pass
                else:
                    print(f'{snp_chromosome}\t{snp_position}\tintergenic')
                    break
    else:
        pass

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-p", "--pos", action="store", dest="pos", required=True,help="SNP position file,(chr    pos)")
    parser.add_argument("-g", "--gff", action="store", dest="gff",required=True,help="gff file,only need mRNA and CDS rows")
    args = parser.parse_args()
    pos = args.pos
    gff = args.gff
    mRNA_list=get_mRNA_list(gff)
    with open(pos, 'r') as IN1:
        all_pos= IN1.readlines()
        for pos in all_pos:
            pos=pos.strip().split()
            snp_chromosome=pos[0]
            snp_position=pos[1]
            get_snp_location(snp_chromosome,int(snp_position),mRNA_list)


if __name__ == "__main__":
    main()
    # example： python find_position_in_gff.py -p pos.txt -g example.gff
    # output: NC_000001.11    17510   exon    (3)
    #         NC_000001.11    17480   intron
    #         NC_000001.22    17510   exon    (3)
    #         NC_000001.22    17480   intron
    #         NC_000001.22    11111111        intergenic
