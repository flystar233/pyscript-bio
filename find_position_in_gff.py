import argparse
import copy
def get_mRNA_list(gff_file):
    mRNA_list = {}
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
    return mRNA_list
                
def get_snp_location(snp_chromosome,snp_position,mRNA_list):
    tmp_mRNA_list = copy.deepcopy(mRNA_list)
    if snp_chromosome in tmp_mRNA_list:
        specified_chromosome_data=tmp_mRNA_list[snp_chromosome]
        for mrna_index,mRNA in enumerate(specified_chromosome_data):
            mRNA_quantity=len(tmp_mRNA_list)
            if mRNA[0][0]<=snp_position<=mRNA[0][1]:
                mRNA.pop(0)
                CDS_quantity=len(mRNA)
                for cds_index,pos in enumerate(mRNA):
                    if pos[0]<=snp_position<=pos[1]:
                        print(f'{snp_chromosome}\t{snp_position}\texon\t({cds_index+1})')
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
    # output: 17510   exon    (3)
    #         17480   intron
    #         111111  intergenic
