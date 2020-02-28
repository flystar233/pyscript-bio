import sys
from collections import Counter
import collections
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
Re_genetic_code = {'A':['GCT','GCC','GCA','GCG'],'R':['CGT','CGC','CGA','CGG','AGA','AGG'],'N':['AAT','AAC'],
            'D':['GAT','GAC'],'C':['TGT','TGC'],'Q':['CAA','CAG'],'E':['GAA','GAG'],'G':['GGT','GGC','GGA','GGG'],
            'H':['CAT','CAC'],'I':['ATT','ATC','ATA'],'L':['TTA','TTG','CTT','CTC','CTA','CTG'],'K':['AAA','AAG'],
            'M':['ATG'],'F':['TTT','TTC'],'P':['CCT','CCC','CCA','CCG'],'S':['TCT','TCC','TCA','TCG','AGT','AGC'],
            'T':['ACT','ACC','ACA','ACG'],'W':['TGG'],'Y':['TAT','TAC'],'V':['GTT','GTC','GTA','GTG'],'*':['TAA','TGA','TAG']}
Re_genetic_code2 = ['GCT','GCC','GCA','GCG','CGT','CGC','CGA','CGG','AGA','AGG','AAT','AAC','GAT','GAC','TGT','TGC',
 'CAA','CAG','GAA','GAG','GGT','GGC','GGA','GGG','CAT','CAC','ATT','ATC','ATA','TTA','TTG','CTT',
 'CTC','CTA','CTG','AAA','AAG','ATG','TTT','TTC','CCT','CCC','CCA','CCG','TCT','TCC','TCA','TCG',
 'AGT','AGC','ACT','ACC','ACA','ACG','TGG','TAT','TAC','GTT','GTC','GTA','GTG','TAA','TGA','TAG']


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

def prediction_p2d(train_seq,test_seq):
    train = parseFasta(train_seq)
    train_value = list(train.values())[0]
    train_value = [train_value[i:i+3] for i in range(0, len(train_value), 3)]
    counter = dict(Counter(train_value))
    new_counter = collections.defaultdict(int)
    for key,value in counter.items():
        new_counter[key]= value/len(train_value)
    freq = []
    for i in Re_genetic_code2: #sort by Re_genetic_code2
        freq.append((i,new_counter[i]))

    new_genetic_code = collections.defaultdict(int) #build a genetic code from the most frequent codons

    new_counter_A = {'GCT':new_counter['GCT'],'GCC':new_counter['GCC'],'GCA':new_counter['GCA'],'GCG':new_counter['GCG']}
    new_counter_A_tmp = []
    for key,value in new_counter_A.items():
        new_counter_A_tmp.append((key,value))
    new_counter_A_tmp = sorted(new_counter_A_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['A'] = new_counter_A_tmp[0][0]

    new_counter_R = {'CGT':new_counter['CGT'],'CGC':new_counter['CGC'],'CGA':new_counter['CGA'],
                    'CGG':new_counter['CGG'],'AGA':new_counter['AGA'],'AGG':new_counter['AGG']}
    new_counter_R_tmp = []
    for key,value in new_counter_R.items():
        new_counter_R_tmp.append((key,value))
    new_counter_R_tmp = sorted(new_counter_R_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['R'] = new_counter_R_tmp[0][0]

    new_counter_N = {'AAT':new_counter['AAT'],'AAC':new_counter['AAC']}
    new_counter_N_tmp = []
    for key,value in new_counter_N.items():
        new_counter_N_tmp.append((key,value))
    new_counter_N_tmp = sorted(new_counter_N_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['N'] = new_counter_N_tmp[0][0]

    new_counter_D = {'GAT':new_counter['GAT'],'GAC':new_counter['GAC']}
    new_counter_D_tmp = []
    for key,value in new_counter_D.items():
        new_counter_D_tmp.append((key,value))
    new_counter_D_tmp = sorted(new_counter_D_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['D'] = new_counter_D_tmp[0][0]

    new_counter_C = {'TGT':new_counter['TGT'],'TGC':new_counter['TGC']}
    new_counter_C_tmp = []
    for key,value in new_counter_C.items():
        new_counter_C_tmp.append((key,value))
    new_counter_C_tmp = sorted(new_counter_C_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['C'] = new_counter_C_tmp[0][0]

    new_counter_Q = {'CAA':new_counter['CAA'],'CAG':new_counter['CAG']}
    new_counter_Q_tmp = []
    for key,value in new_counter_Q.items():
        new_counter_Q_tmp.append((key,value))
    new_counter_Q_tmp = sorted(new_counter_Q_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['Q'] = new_counter_Q_tmp[0][0]

    new_counter_E = {'GAA':new_counter['GAA'],'GAG':new_counter['GAG']}
    new_counter_E_tmp = []
    for key,value in new_counter_E.items():
        new_counter_E_tmp.append((key,value))
    new_counter_E_tmp = sorted(new_counter_E_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['E'] = new_counter_E_tmp[0][0]

    new_counter_G = {'GGT':new_counter['GGT'],'GGC':new_counter['GGC'],'GGA':new_counter['GGA'],'GGG':new_counter['GGG']}
    new_counter_G_tmp = []
    for key,value in new_counter_G.items():
        new_counter_G_tmp.append((key,value))
    new_counter_G_tmp = sorted(new_counter_G_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['G'] = new_counter_G_tmp[0][0]

    new_counter_H = {'CAT':new_counter['CAT'],'CAC':new_counter['CAC']}
    new_counter_H_tmp = []
    for key,value in new_counter_H.items():
        new_counter_H_tmp.append((key,value))
    new_counter_H_tmp = sorted(new_counter_H_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['H'] = new_counter_H_tmp[0][0]

    new_counter_I = {'ATT':new_counter['ATT'],'ATC':new_counter['ATC'],'ATA':new_counter['ATA']}
    new_counter_I_tmp = []
    for key,value in new_counter_I.items():
        new_counter_I_tmp.append((key,value))
    new_counter_I_tmp = sorted(new_counter_I_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['I'] = new_counter_I_tmp[0][0]

    new_counter_L = {'TTA':new_counter['TTA'],'TTG':new_counter['TTG'],'CTT':new_counter['CTT'],
                    'CTC':new_counter['CTC'],'CTA':new_counter['CTA'],'CTG':new_counter['CTG']}
    new_counter_L_tmp = []
    for key,value in new_counter_L.items():
        new_counter_L_tmp.append((key,value))
    new_counter_L_tmp = sorted(new_counter_L_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['L'] = new_counter_L_tmp[0][0]

    new_counter_K = {'AAA':new_counter['AAA'],'AAG':new_counter['AAG']}
    new_counter_K_tmp = []
    for key,value in new_counter_K.items():
        new_counter_K_tmp.append((key,value))
    new_counter_K_tmp = sorted(new_counter_K_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['K'] = new_counter_K_tmp[0][0]

    new_counter_M = {'ATG':new_counter['ATG']}
    new_counter_M_tmp = []
    for key,value in new_counter_M.items():
        new_counter_M_tmp.append((key,value))
    new_counter_M_tmp = sorted(new_counter_M_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['M'] = new_counter_M_tmp[0][0]

    new_counter_F = {'TTT':new_counter['TTT'],'TTC':new_counter['TTC']}
    new_counter_F_tmp = []
    for key,value in new_counter_F.items():
        new_counter_F_tmp.append((key,value))
    new_counter_F_tmp = sorted(new_counter_F_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['F'] = new_counter_F_tmp[0][0]

    new_counter_P = {'CCT':new_counter['CCT'],'CCC':new_counter['CCC'],'CCA':new_counter['CCA'],'CCG':new_counter['CCG']}
    new_counter_P_tmp = []
    for key,value in new_counter_P.items():
        new_counter_P_tmp.append((key,value))
    new_counter_P_tmp = sorted(new_counter_P_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['P'] = new_counter_P_tmp[0][0]

    new_counter_S = {'TCT':new_counter['TCT'],'TCC':new_counter['TCC'],'TCA':new_counter['TCA'],
                    'TCG':new_counter['TCG'],'AGT':new_counter['AGT'],'AGC':new_counter['AGC']}
    new_counter_S_tmp = []
    for key,value in new_counter_S.items():
        new_counter_S_tmp.append((key,value))
    new_counter_S_tmp = sorted(new_counter_S_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['S'] = new_counter_S_tmp[0][0]

    new_counter_T = {'ACT':new_counter['ACT'],'ACC':new_counter['ACC'],'ACA':new_counter['ACA'],'ACG':new_counter['ACG']}
    new_counter_T_tmp = []
    for key,value in new_counter_T.items():
        new_counter_T_tmp.append((key,value))
    new_counter_T_tmp = sorted(new_counter_T_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['T'] = new_counter_T_tmp[0][0]

    new_counter_W = {'TGG':new_counter['TGG']}
    new_counter_W_tmp = []
    for key,value in new_counter_W.items():
        new_counter_W_tmp.append((key,value))
    new_counter_W_tmp = sorted(new_counter_W_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['W'] = new_counter_W_tmp[0][0]

    new_counter_Y = {'TAT':new_counter['TAT'],'TAC':new_counter['TAC']}
    new_counter_Y_tmp = []
    for key,value in new_counter_Y.items():
        new_counter_Y_tmp.append((key,value))
    new_counter_Y_tmp = sorted(new_counter_Y_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['Y'] = new_counter_Y_tmp[0][0]

    new_counter_V = {'GTT':new_counter['GTT'],'GTC':new_counter['GTC'],'GTA':new_counter['GTA'],'GTG':new_counter['GTG']}
    new_counter_V_tmp = []
    for key,value in new_counter_V.items():
        new_counter_V_tmp.append((key,value))
    new_counter_V_tmp = sorted(new_counter_V_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['V'] = new_counter_V_tmp[0][0]

    new_counter_end = {'TAA':new_counter['TAA'],'TGA':new_counter['TGA'],'TAG':new_counter['TAG']}
    new_counter_end_tmp = []
    for key,value in new_counter_end.items():
        new_counter_end_tmp.append((key,value))
    new_counter_end_tmp = sorted(new_counter_end_tmp, key=lambda code: code[1], reverse=True)
    new_genetic_code['*'] = new_counter_end_tmp[0][0]

    test = parseFasta(test_seq)
    mykey = list(test.keys())
    for value in test.values(): #Loop through each sequence
        new_value = '' #init new seq
        for i in value:
            new_value += new_genetic_code[i.upper()]
        result_seq.append(new_value)
    result = zip(mykey,result_seq)
    return freq,new_genetic_code,result

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
elif(len(sys.argv)==4 and 'pp2d' in sys.argv):
    frequency,code,result = prediction_p2d(sys.argv[2],sys.argv[3])
    with open('frequency_result.txt','w') as OUT1:
        for i in frequency:
            OUT1.write(i[0]+"\t"+str(i[1])+"\n")
    with open('code_result.txt','w') as OUT2:
        for key,value in code.items():
            OUT2.write(key+" : "+value+"\n")
    with open('pp2d_result.txt','w') as OUT:
        for i in result:
            OUT.write(i[0])
            OUT.write("\n")
            OUT.write(i[1])
            OUT.write("\n")
else:
    print("Usage: python transcode.py p2d protein.fa specie(fish,plant,human,bacterial). \
          \npython transcode.py d2p dna.fa\npython transcode.py pp2d train.fa protein.fa")