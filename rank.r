library(randomForest)
library(outForest)
library(dplyr)
find_max_index <- function(x, y) {
# 找出y在x中的位置的最大索引
    index <- which(x == y)
    if (length(index) == 1) {
# 如果x中有值等于y
        index_name <- names(x)[index]
        return(index_name)
    } else if (length(index) > 1) {
        if(median(index)<500){
            min_index <- min(index)
            min_index_name <- names(x)[min_index]
        }else{
            max_index <- max(index)
            max_index_name <- names(x)[max_index]
        }
        }
        else {
# 如果x中没有值等于y
        closest_index <- which.min(abs(x - y))
        closest_index_name <- names(x)[closest_index]
        return(closest_index_name)
    }
}

get_rank <-function(x,y,what=seq(from = 0.001, to = 0.999, by = 0.001)){
    qrf <- randomForest( x=x,y=y)
    nodesX <- attr(predict(qrf,x,nodes=TRUE),"nodes")
    rownames(nodesX) <- NULL
    nnodes <- max(nodesX)
    ntree <- ncol(nodesX)
    n <- nrow(x)
    valuesNodes  <- matrix(nrow=nnodes,ncol=ntree)

    for (tree in 1:ntree){
      shuffledNodes <- nodesX[rank(ind <- sample(1:n,n)),tree]
      useNodes <- sort(unique(as.numeric(shuffledNodes)))
      valuesNodes[useNodes,tree] <- y[ind[match(useNodes,shuffledNodes)]]
    }

    valuesPredict <- 0*nodesX
    for (tree in 1:ntree){
            valuesPredict[,tree] <- valuesNodes[nodesX[,tree],tree]  
        }

    result <- t(apply( valuesPredict,1,quantile, what,na.rm=TRUE)) 
    return(result)

}  

# Example usage
iris1<-generateOutliers(iris, p = 0.2,seed=2024)
outMatrix <- get_rank(iris1[,2:4], iris1[,1], what=seq(from = 0.001, to = 0.990, by = 0.001))

xx<-c()
median_value <-c()
for (i in 1:length(iris1[,1])){
    x<- find_max_index(outMatrix[i,],iris1[,1][i])
    median_value <- c(median_value,outMatrix[i,50])
    xx<-c(xx,x)
}
result <- data.frame(orinal_value1= iris[,1],orinal_value = iris1[,1], rank = xx, median_value = median_value)
data<- result|> filter(orinal_value1!=orinal_value |rank<0.025 |rank>0.975)
print(data)