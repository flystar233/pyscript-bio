from  collections import defaultdict
import argparse
def vcf_slide():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-f", "--vcf", action="store", dest="vcf_name", required=True)
    parser.add_argument("-g", "--genome", action="store", dest="genome_name", required=True)
    parser.add_argument("-w", "--window", dest="window_size",type = int,default =100000)
    args = parser.parse_args()
    vcf_name = args.vcf_name
    genome_name = args.genome_name
    window_size = args.window_size

    with open(vcf_name) as IN1,open(genome_name) as IN2:
        len_dict = {}
        for i in IN2:
            tmp = i.split()
            len_dict[tmp[0]]=tmp[1]

        location = []
        for CHR,LENGTH in len_dict.items():
            for i in range(0,int(LENGTH)+1,window_size):
                if i+window_size < int(len_dict[CHR]):
                    location.append((CHR,i,i+window_size-1))
                else:
                    location.append((CHR,i,int(len_dict[CHR])))
        vcf_loc = defaultdict(list)
        for i in IN1:
            tmp = i.split() 
            vcf_loc[tmp[0]].append(tmp[1])
        for i in location:
            num = 0
            for y in vcf_loc[i[0]]:
                if int(i[1])<=int(y)<=int(i[2]):
                    num+=1
            print(i[0],i[1],i[2],num)

if __name__ == "__main__":
    vcf_slide()
