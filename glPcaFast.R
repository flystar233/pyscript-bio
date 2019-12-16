glPcaFast <- function(x,
 center=TRUE,
 scale=FALSE,
 nf=NULL,
 loadings=TRUE,
 alleleAsUnit=FALSE,
 returnDotProd=FALSE){

 if(!inherits(x, "genlight")) stop("x is not a genlight object")
 # keep the original mean / var code, as it's used further down
 # and has some NA checks..
 if(center) {
 vecMeans <- glMean(x, alleleAsUnit=alleleAsUnit)
 if(any(is.na(vecMeans))) stop("NAs detected in the vector of means")
 }
 if(scale){
 vecVar <- glVar(x, alleleAsUnit=alleleAsUnit)
 if(any(is.na(vecVar))) stop("NAs detected in the vector of variances")
 }
 # convert to full data, try to keep the NA handling as similar
 # to the original as possible
 # - dividing by ploidy keeps the NAs
 mx <- t(sapply(x$gen, as.integer)) / ploidy(x)
 # handle NAs
 NAidx <- which(is.na(mx), arr.ind = T)
 if (center) {
 mx[NAidx] <- vecMeans[NAidx[,2]]
 } else {
 mx[NAidx] <- 0
 }
 # center and scale
 mx <- scale(mx,
 center = if (center) vecMeans else F,
 scale = if (scale) vecVar else F)
 # all dot products at once using underlying BLAS
 # to support thousands of samples, this could be
 # replaced by 'Truncated SVD', but it would require more changes
 # in the code around
 allProd <- tcrossprod(mx) / nInd(x) # assume uniform weights
 ## PERFORM THE ANALYSIS ##
 ## eigenanalysis
 eigRes <- eigen(allProd, symmetric=TRUE, only.values=FALSE)
 rank <- sum(eigRes$values > 1e-12)
 eigRes$values <- eigRes$values[1:rank]
 eigRes$vectors <- eigRes$vectors[, 1:rank, drop=FALSE]
 ## scan nb of axes retained
 if(is.null(nf)){
 barplot(eigRes$values, main="Eigenvalues", col=heat.colors(rank))
 cat("Select the number of axes: ")
 nf <- as.integer(readLines(n = 1))
 }
 ## rescale PCs 
 res <- list()
 res$eig <- eigRes$values
 nf <- min(nf, sum(res$eig>1e-10))
 ##res$matprod <- allProd # for debugging
 ## use: li = XQU = V\Lambda^(1/2)
 eigRes$vectors <- eigRes$vectors * sqrt(nInd(x)) # D-normalize vectors
 res$scores <- sweep(eigRes$vectors[, 1:nf, drop=FALSE],2,
sqrt(eigRes$values[1:nf]), FUN="*")
 ## GET LOADINGS ##
 ## need to decompose X^TDV into a sum of n matrices of dim p*r
 ## but only two such matrices are represented at a time
 if(loadings){
 if(scale) {
 vecSd <- sqrt(vecVar)
 }
 res$loadings <- matrix(0, nrow=nLoc(x), ncol=nf) # create empty matrix
 ## use: c1 = X^TDV
 ## and X^TV = A_1 + ... + A_n
 ## with A_k = X_[k-]^T v[k-]
 myPloidy <- ploidy(x)
 for(k in 1:nInd(x)){
 temp <- as.integer(x@gen[[k]]) / myPloidy[k]
 if(center) {
 temp[is.na(temp)] <- vecMeans[is.na(temp)]
 temp <- temp - vecMeans
 } else {
 temp[is.na(temp)] <- 0
 }
 if(scale){
 temp <- temp/vecSd
 }
 res$loadings <- res$loadings + matrix(temp) %*% eigRes$vectors[k,
1:nf, drop=FALSE]
 }
 res$loadings <- res$loadings / nInd(x) # don't forget the /n of X_tDV
 res$loadings <- sweep(res$loadings, 2, sqrt(eigRes$values[1:nf]),
FUN="/")
 }
 ## FORMAT OUTPUT ##
 colnames(res$scores) <- paste("PC", 1:nf, sep="")
 if(!is.null(indNames(x))){
 rownames(res$scores) <- indNames(x)
 } else {
 rownames(res$scores) <- 1:nInd(x)
 }
 if(!is.null(res$loadings)){
 colnames(res$loadings) <- paste("Axis", 1:nf, sep="")
 if(!is.null(locNames(x)) & !is.null(alleles(x))){
 rownames(res$loadings) <- paste(locNames(x),alleles(x), sep=".")
 } else {
 rownames(res$loadings) <- 1:nLoc(x)
 }
 }
 if(returnDotProd){
 res$dotProd <- allProd
 rownames(res$dotProd) <- colnames(res$dotProd) <- indNames(x)
 }
 res$call <- match.call()
 class(res) <- "glPca"
 return(res)
}