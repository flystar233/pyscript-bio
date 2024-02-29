import argparse

def parseFasta(filename):
    fas = {}
    with open(filename, 'r') as fh:
        for line in fh:
            if line[0] == '>':
                header = line[1:].rstrip()
                id = header.split()[0]
                fas[id] = []
            else:
                fas[id].append(line.rstrip())
        for id, seq in fas.items():
            fas[id] = ''.join(seq)
    return fas

def calc_N_value(lengths, ratio):
    total_len = sum(lengths)
    target = total_len * ratio
    value_sum = 0
    for value in lengths:
        value_sum += value
        if target <= float(value_sum):
            return value
    return 0

def dealN50(fasta,cutoff=1):
    print("Including contigs/scaffolds with at least {} bp".format(cutoff))
    lengths, mydict = [], parseFasta(fasta)
    G_count = C_count = 0
    for id, seq in mydict.items():
        len_seq = len(seq)
        if len_seq > cutoff:
            lengths.append(len_seq)
            G_count += seq.upper().count('G')
            C_count += seq.upper().count('C')
    lengths.sort(reverse=True)
    allsum = sum(lengths)
    GC_content = round((G_count + C_count) / allsum, 4)  # round to 4 decimal places
    return calc_N_value(lengths, 0.5), calc_N_value(lengths, 0.9), allsum, lengths[0], GC_content

def main():
    parser = argparse.ArgumentParser(description="Calculate genome size and N50,N90,GC content.")
    parser.add_argument("fasta", help="Input fasta file.")
    parser.add_argument("cutoff", type=int, default=1, help="Cutoff for sequence length.")
    args = parser.parse_args()

    result = dealN50(args.fasta, args.cutoff)
    print("The genome size is {} bp".format(result[2]))
    print("The max length is {} bp".format(result[3]))
    print("The N50 is {} bp".format(result[0]))
    print("The N90 is {} bp".format(result[1]))
    print("The GC content is {}".format(result[4]))

if __name__ == "__main__":
    main()
