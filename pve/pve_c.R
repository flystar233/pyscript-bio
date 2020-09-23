Args <- commandArgs(T)
if(length(Args)!=2){
cat("Rscript work_pve.R pve_in.raw result_pve.txt...\n")
quit("no")}
infile=Args[1]
outfile=Args[2]
library(data.table)
data<-fread(infile,header = T,nThread=8)
cat(paste("Read file done!","\n"))
varlist<-names(data)[2:ncol(data)]
models <- lapply(varlist, function(x) {
  tmp<-lm(substitute(trait ~ i, list(i = as.name(x))), data = data)
  cat(paste("Deal with ",x,"\n"))
  af<-anova(tmp)
  afss <- af$"Sum Sq"
  cbind(af,PctExp=afss/sum(afss)*100)
})
write.table('SITE\tPVE',file = outfile,row.names = F,col.names = F,quote =FALSE)
for (i in 1:length(models)){
  write.table(paste(rownames(models[[i]]), models[[i]]$PctExp),sep = "\n",file = outfile,row.names = F,col.names = F,quote =FALSE,append=T)
}