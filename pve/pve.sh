#!/bin/bash

(($# == 2)) || { echo -e "\nUsage: $0 <plink.raw> <trait.txt>\n"; exit; }

infile="$1"
trait_file="$2"
cut -f 1,2,3,4,5,6 --complement $infile  -d " " > tmp.raw
sh split_col.sh tmp.raw 100000
rm tmp.raw
i=0
ls tmp.raw*|while read line
do
paste $trait_file $line -d " " >pve_in.raw.$i
rm $line
echo "Rscript pve_c.R pve_in.raw.$i result_pve.txt$i" > work_pve.sh$i
((i++))
done