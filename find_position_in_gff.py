import argparse
def get_mRNA_list(gff_file):
    with open(gff_file, 'r') as file:
        CDS_list=[]
        all_mRNA_list=[]
        for line in file:
            if not line.startswith('#'):
                data = line.strip().split()
                seqid = data[0]
                feature = data[2]
                pos = [int(data[3]),int(data[4])]
                if feature=='mRNA':
                    CDS_list.sort(key=lambda x: x[0])
                    all_mRNA_list.append(CDS_list)
                    CDS_list=[]
                CDS_list.append(pos)
        all_mRNA_list.pop(0)
        return all_mRNA_list
                
def get_snp_location(snp,mRNA_list):
    for mrna_index,mRNA in enumerate(mRNA_list):
        mRNA_quantity=len(mRNA_list)
        if mRNA[0][0]<=snp<=mRNA[0][1]:
            mRNA.pop(0)
            CDS_quantity=len(mRNA)
            for cds_index,pos in enumerate(mRNA):
                if pos[0]<=snp<=pos[1]:
                    print(f'{snp}\texon\t({cds_index+1})')
                    break
                else:
                    if cds_index+1 < CDS_quantity:
                        pass
                    else:
                        print(f'{snp}\tintron')
                        break
            break
        else:
            if mrna_index+1 < mRNA_quantity:
                pass
            else:
                print(f'{snp}\tintergenic')
                break

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-p", "--pos", action="store", dest="pos", required=True,help="SNP position file,only one row is needed")
    parser.add_argument("-g", "--gff", action="store", dest="gff",required=True,help="gff file,only need mRNA and CDS rows,and only one chromosome is supported")
    args = parser.parse_args()
    pos = args.pos
    gff = args.gff
    mRNA_list=get_mRNA_list(gff)
    with open(pos, 'r') as IN1:
        all_pos= IN1.readlines()
        for pos in all_pos:
            get_snp_location(int(pos),mRNA_list)


if __name__ == "__main__":
    main()
    # example： python find_position_in_gff.py -p pos.txt -g example.gff
    # output: 17510   exon    (3)
    #         17480   intron
    #         111111  intergenic
