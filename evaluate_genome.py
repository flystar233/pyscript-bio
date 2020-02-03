import sys
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
def dealN50(fasta,cutoff=1):
    print("Including contigs/scaffolds with at least {} bp".format(cutoff))
    BaseSum,N50,N90 = 0,0,0
    Length = []
    G_count,C_count = 0,0
    mydict = parseFasta(fasta)
    for id, seq in mydict.items():
        Length.append(len(seq))
        G_count += seq.upper().count('G')
        C_count += seq.upper().count('C')
    Length = sorted(Length, reverse=True)
    Allsum = sum(Length) # caculate GC concent ,so defind Allsum
    GC_content = (G_count + C_count) / Allsum
    Length = [i for i in Length if i > cutoff]
    BaseSum = sum(Length)
    Max_len = Length[0]
    N50_pos = float(BaseSum / 2.0)
    N90_pos = float(BaseSum / 1.111111)
    ValueSum = 0
    for value in Length:
        ValueSum += value
        if N50_pos <= float(ValueSum):
           N50 = value
           break
    ValueSum = 0
    for value in Length:
        ValueSum += value
        if N90_pos <= float(ValueSum):
           N90 = value
           break
    return N50,N90,BaseSum,Max_len,GC_content
if (len(sys.argv)==3):
    result = dealN50(sys.argv[1],int(sys.argv[2]))
    print("The genome size is {} bp".format(result[2]))
    print("The max length is {} bp".format(result[3]))
    print("The N50 is {} bp".format(result[0]))
    print("The N90 is {} bp".format(result[1]))
    print("The GC content is {}".format(result[4]))
else:
    print("Calculate genome size and N50,N90,GC content.\nUsage: python test.fa cutoff")
