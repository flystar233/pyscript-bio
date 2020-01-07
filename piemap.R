if (!require("getopt")) install.packages("getopt")
spec <- matrix(c(
        'input', 'i', 1, 'character',
        'output', 'o', 1, 'character',
        'help', 'h', 0, 'logical'
        ), byrow = TRUE, ncol = 4)
opt <- getopt(spec)

print_usage <- function(spec = NULL) {
        getopt(spec, usage = TRUE)
        cat('
Example:
1) Rscript map.R -i [map.data] -o [output_file_name]
2) Rscript amp.R --input [map.data] --output [output_file_name]
The format of input file:
Latitude	Longitude	sample1	sample2	sample3
-38.416097	-63.616672      1       0       4
-35.675147	-71.542969      0       0       0
-32.522779	-55.765835      1       0       2
\n')
        q('no')
}
if (!is.null(opt$help)) print_usage(spec)
library (rworldmap)
library(rworldxtra)

pdf(paste(opt$output, 'pdf', sep = '.'),height=10, width=20)
color_list <-c('gray3','plum1','peru','olivedrab2','firebrick1','grey70','dodgerblue','gold1','hotpink2','orchid','cornsilk')
mapdata <- read.table(opt$input, head=T,sep='\t',)
mapdata  <- as.data.frame(mapdata)
class <- names(mapdata)[-1][-1] #delete "Longitude" and  "Latitude"
random_col <- sample(color_list,size=length(class)) #select color

mapPies(mapdata,nameX="Longitude",nameY="Latitude",nameZs=class,mapRegion='world',symbolSize=1.3,barOrient='vert',oceanCol="grey",landCol="white",addCatLegend=F,zColours =random_col)
dev.off()
