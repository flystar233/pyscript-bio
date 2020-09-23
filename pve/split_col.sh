#!/bin/bash

(($# == 2)) || { echo -e "\nUsage: $0 <file to split> <# columns in each split>\n\n"; exit; }

infile="$1"

inc=$2
ncol=$(awk 'NR==1{print NF}' "$infile")

((inc < ncol)) || { echo -e "\nSplit size >= number of columns\n\n"; exit; }

for((i=0, start=1, end=$inc; i < ncol/inc + 1; i++, start+=inc, end+=inc)); do
  cut -f$start-$end "$infile" -d " "> "${infile}.$i"
done
