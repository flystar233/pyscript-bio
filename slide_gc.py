import argparse
import sys
def parseFasta(filename): #seq_api
    fas = {}
    idlis = []
    id = None
    with open(filename, 'r') as fh:
        for line in fh:
            if line[0] == '>':
                header = line[0:].rstrip()
                id = header.split()[0]
                idlis.append(id)
                fas[id] = []
            else:
                fas[id].append(line.rstrip())
        for id, seq in fas.items():
            fas[id] = ''.join(seq)
    return fas

def gc_slide():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-f", "--fasta", action="store", dest="fasta_name", required=True)
    parser.add_argument("-s", "--step", action="store", type = int,dest="step", default =20000)
    parser.add_argument("-w", "--window", dest="window_size",type = int,default =100000)
    args = parser.parse_args()
    fasta_name = args.fasta_name
    step = args.step
    window_size = args.window_size
    if step >window_size:
        print("ERROR! step can't be bigger than window.")
        sys.exit()
    genome_fa = parseFasta(fasta_name)
    print("chr start end gc_count")
    for CHR,SEQ in genome_fa.items():
        i=0
        while i<len(SEQ):
            x = SEQ[i:i+window_size]
            if len(SEQ)-i>=window_size:
                print(CHR.strip('>'),i+1,i+window_size,(x.upper().count('G')+x.upper().count('C'))/len(x))
            i=i+step
if __name__ == "__main__":
    gc_slide()