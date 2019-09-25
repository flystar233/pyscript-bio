import os
import sys

def splitfile(filepath,linesize=10):
    filedir,name = os.path.split(filepath)
    name,ext = os.path.splitext(name)
    filedir = os.path.join(filedir,name)
    if not os.path.exists(filedir):
        os.mkdir(filedir)
         
    partnum = 0
    with open(filepath,'r', encoding='utf-8') as stream:
        while True:
            partfilename = os.path.join(filedir,name + '_' + str(partnum) + ext)
            print('Write data into %s' % partfilename)
            part_stream = open(partfilename,'w', encoding='utf-8')
 
            read_count = 0
            while read_count < int(linesize):
                read_content = stream.readline()
                if read_content:
                    part_stream.write(read_content)
                else:
                    break
                read_count += 1
          
            part_stream.close()
            if(read_count < int(linesize)) :
                break
            partnum += 1
 
        print('Split file done')
 
if (len(sys.argv)==3):
        splitfile(sys.argv[1],sys.argv[2])
else:
        print("Usage: python split.py split_file split_lines")
