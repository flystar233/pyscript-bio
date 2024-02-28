import argparse
import logging
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
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
handler = logging.FileHandler('error.log')
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_mRNA_list(gff_file):
    mRNA_list = {}
    with open(gff_file, 'r') as gff:
        for line in gff:
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
    # Sort the mRNA list
    for chromosome, mrnas in mRNA_list.items():
        mRNA_list[chromosome] = [sorted(mrna, key=lambda x: x[0]) for mrna in mrnas]
    return mRNA_list

                
def get_snp_location(snp_chromosome, snp_position, mRNA_list):
    if snp_chromosome not in mRNA_list:
        logger.error(f'Chromosome {snp_chromosome} not found in mRNA list.')
        return
    for mrna in mRNA_list[snp_chromosome]:
        if mrna[0][0] <= snp_position <= mrna[0][1]:
            for idx, pos in enumerate(mrna[1:], start=1):
                if pos[0] <= snp_position <= pos[1]:
                    print(f'{snp_chromosome}\t{snp_position}\texon ({idx})')
                    return
            print(f'{snp_chromosome}\t{snp_position}\tintron')
            return

    print(f'{snp_chromosome}\t{snp_position}\tintergenic')

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-p", "--pos", action="store", dest="pos", required=True,help="SNP position file,(chr    pos)")
    parser.add_argument("-g", "--gff", action="store", dest="gff",required=True,help="gff file,only need mRNA and CDS rows")
    args = parser.parse_args()
    
    # Load mRNA list
    mRNA_list=get_mRNA_list(args.gff)

    # Process SNP positions
    with open(args.pos, 'r') as pos_file:
        for line in pos_file:
            snp_chromosome, snp_position = line.strip().split()
            get_snp_location(snp_chromosome, int(snp_position), mRNA_list)


if __name__ == "__main__":
    main()
    # example： python find_position_in_gff.py -p pos.txt -g example.gff
    # output: 17510   exon    (3)
    #         17480   intron
    #         111111  intergenic
