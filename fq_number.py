import os
from multiprocessing import Pool
import gzip
import sys
import time
def process_wrapper(filename,chunkStart, chunkSize):
    row_num = 0
    base_num =0
    if filename.endswith('gz'):
        myopen = gzip.open
    else:
        myopen = open
    with myopen(filename,'rb') as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        row_num +=len(lines)
        for i in lines:
            if i.startswith(b'@') or i.strip()==b'+':
                pass
            else:
                base_num+=len(i.strip())
    return row_num,base_num

def chunkify(fname,size):
    if fname.endswith('gz'):
        fileEnd = int(os.popen(f"pigz -dc {fname}|wc -c").read())
        myopen = gzip.open
    else:
        fileEnd = int(os.path.getsize(fname))
        myopen = open
    with myopen(fname,'rb') as f:
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size,1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd >= fileEnd:
                break

if "__main__" == __name__:
    if (len(sys.argv)==3):
        start = time.time()
        cpu_core = int(sys.argv[2])
        myfile = sys.argv[1]
        if myfile.endswith('gz'):
            chunk_size_set = int(int(os.popen(f"pigz -dc {myfile}|wc -c").read())/20)
        else:
            chunk_size_set = int(os.path.getsize(myfile)/20)
        pool = Pool(cpu_core)
        jobs = []
        for chunkStart, chunkSize in chunkify(myfile,chunk_size_set):
            jobs.append(pool.apply_async(process_wrapper, (myfile,chunkStart,chunkSize)))
        res = []
        for job in jobs:
            res.append(job.get())
        all_row_num = 0
        all_base_num = 0
        for i in res:
            all_row_num+=i[0]
            all_base_num+=i[1]
        print("num_seqs: ",f"{int(all_row_num/4):,d}"," sum_len: ",f"{int(all_base_num/2):,d}")
        end = time.time()
        t = end - start
        print("The total running time is {:.2f}s.".format(t))
    else:
        print("Usage: python fqfile cpu_number")
