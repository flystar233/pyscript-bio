import sys

Danio_rerio = {'A':'GCT','R':'AGA','N':'AAC','D':'GAC','C':'TGT','Q':'CAG','E':'GAG',
            'G':'GGA','H':'CAC','I':'ATC','L':'CTG','K':'AAG','M':'ATG','F':'TTC',
            'P':'CCT','S':'AGC','T':'ACA','W':'TGG','Y':'TAC','V':'GTG','*':'TGA'}
Arabidopsis_thaliana = {'A':'GCT','R':'AGA','N':'AAT','D':'GAT','C':'TGT','Q':'CAA','E':'GAA',
            'G':'GGA','H':'CAT','I':'ATT','L':'CTT','K':'AAG','M':'ATG','F':'TTT',
            'P':'CCT','S':'TCT','T':'ACT','W':'TGG','Y':'TAT','V':'GTT','*':'TGA'}
Homo_sapiens = {'A':'GCC','R':'AGA','N':'AAC','D':'GAC','C':'TGC','Q':'CAG','E':'GAG',
            'G':'GGC','H':'CAC','I':'ATC','L':'CTG','K':'AAG','M':'ATG','F':'TTC',
            'P':'CCC','S':'AGC','T':'ACC','W':'TGG','Y':'TAC','V':'GTG','*':'TGA'}
Escherichia_coli = {'A':'GCG','R':'CGC','N':'AAC','D':'GAT','C':'TGC','Q':'CAG','E':'GAA',
            'G':'GGC','H':'CAT','I':'ATT','L':'CTG','K':'AAA','M':'ATG','F':'TTT',
            'P':'CCG','S':'AGC','T':'ACC','W':'TGG','Y':'TAT','V':'GTG','*':'TAA'}
Genetic_code = {'TTT':'F','TTC':'F','TTA':'L','TTG':'L','CTT':'L','CTC':'L','CTA':'L','CTG':'L','ATT':'I','ATC':'I','ATA':'I',
            'ATG':'M','GTT':'V','GTC':'V','GTA':'V','GTG':'V','TCT':'S','TCC':'S','TCA':'S','TCG':'S','CCT':'P','CCC':'P','CCA':'P',
            'CCG':'P','ACT':'T','ACC':'T','ACA':'T','ACG':'T','GCT':'A','GCC':'A','GCA':'A','GCG':'A','TAT':'Y','TAC':'Y','TAA':'*',
            'TAG':'*','CAT':'H','CAC':'H','CAA':'Q','CAG':'Q','AAT':'N','AAC':'N','AAA':'K','AAG':'K','GAT':'D','GAC':'D','GAA':'E',
            'GAG':'E','TGT':'C','TGC':'C','TGA':'*','TGG':'W','CGT':'R','CGC':'R','CGA':'R','CGG':'R','AGT':'S','AGC':'S','AGA':'R',
            'AGG':'R','GGT':'G','GGC':'G','GGA':'G','GGG':'G',}

result_seq = []
result_protein = []
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

def p2d(fasta,specie):
    mydict = parseFasta(fasta)
    mykey = list(mydict.keys())
    for value in mydict.values(): #Loop through each sequence
        new_value = '' #init new seq
        if specie in ['FISH','fish']: #select specie
            for i in value:
                new_value += Danio_rerio[i.upper()]
            result_seq.append(new_value) #collect all sequences
        elif specie in ['plant','PLANT']:
            for i in value:
                new_value += Arabidopsis_thaliana[i.upper()]
            result_seq.append(new_value)
        elif specie in ['human','HUMAN']:
            for i in value:
                new_value += Homo_sapiens[i.upper()]
            result_seq.append(new_value)
        elif specie in ['bacterial','BACTERIAL']:
            for i in value:
                new_value += Escherichia_coli[i.upper()]
            result_seq.append(new_value)
        else:
            print("Error! The species you entered is not found in the library\n(fish,plant,human,bacterial).")
            break
    result = zip(mykey,result_seq) #package file
    return result

def d2p(fasta):
    mydict = parseFasta(fasta)
    mykey = list(mydict.keys())
    for index,value in enumerate(mydict.values()): #Loop through each sequence
        new_value = ''
        value = [value[i:i+3] for i in range(0, len(value), 3)]
        if len(value[-1]) < 3: #delete base that's less than 3
            print("The length of {} is not a multiple of 3,delete the last 1 or 2 base.".format(mykey[index][1:])) #print seq name without >
            value.pop()
        for i in value:
            new_value += Genetic_code[i.upper()]
        result_protein.append(new_value)
    result = zip(mykey,result_protein)
    return result

if (len(sys.argv)==3 and 'd2p' in sys.argv): #the mode d2p
    result = d2p(sys.argv[2])
    with open('d2p_result.txt','w') as OUT:
        for i in result:
            OUT.write(i[0])
            OUT.write("\n")
            OUT.write(i[1])
            OUT.write("\n")
elif(len(sys.argv)==4 and 'p2d' in sys.argv): #the mode p2d
    result = p2d(sys.argv[2],sys.argv[3])
    with open('p2d_result.txt','w') as OUT:
        for i in result:
            OUT.write(i[0])
            OUT.write("\n")
            OUT.write(i[1])
            OUT.write("\n")
else:
    print("Usage: python transcode.py p2d protein.fa specie(fish,plant,human,bacterial). or\npython transcode.py d2p dna.fa")