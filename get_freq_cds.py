import sys
import argparse
from collections import defaultdict
from collections import Counter

codon_table = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
}
protein_to_codon = defaultdict(list)
for codon, protein in codon_table.items():
    protein_to_codon[protein].append(codon)
codon_table=dict(protein_to_codon)

def parseFasta(filename):
    fas = {}
    idlis = []
    id = None
    with open(filename, 'r') as fh:
        for line in fh:
            if line[0] == '>':
                header = line[1:].rstrip()
                id = header.split()[0]
                idlis.append(id)
                fas[id] = []
            else:
                fas[id].append(line.rstrip())
        for id, seq in fas.items():
            fas[id] = ''.join(seq)
    return fas

def getFrequency(codon_table,fasta):
    split_strings =[]
    for sequence  in fasta.values():
        split_strings += [sequence[i:i+3] for i in range(0, len(sequence), 3)]
    frequency = Counter(split_strings)

    codon_freq = {}
    for amino_acid, codons in codon_table.items():
        total_freq = sum(frequency[codon] for codon in codons)
        for codon in codons:
            codon_freq[codon] = round(frequency[codon] / total_freq,4)
    return codon_freq


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--in", action="store", dest="cds", required=True,help="cds file from genomic")
    args = parser.parse_args()
    cds = args.cds

    fasta = parseFasta(cds)
    codon_freq = getFrequency(codon_table,fasta)

    for codon, freq in codon_freq.items():
        print(f'Codon {codon} frequency: {freq}')

if __name__ == "__main__":
    main()