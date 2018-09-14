# Usage awk gff2gtf.sh gff.txt >gtf.txt
$3 == "mRNA" ||$3 == "CDS"{match($9,/ID=(.*);/,a);$9=a[1];
printf"%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\tgene_id \"%s\"; transcript_id \"\";\n",$1,$2,$3,$4,$5,$6,$7,$8,a[1]}
