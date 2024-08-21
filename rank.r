library(ranger)
library(outForest)
library(dplyr)

get_quantily_value <- function(name){
    str<- gsub("[^0-9.]", "", name)
    value <- as.numeric(str)
    return(value)
}

find_max_index <- function(x, y) {
    index <- which(x == y)
    if (length(index) >= 1) {
        index_name <- names(x)[index]
        value<-get_quantily_value(index_name)
        return(value)
    } 
    else {
        closest_index <- which.min(abs(x - y))
        closest_index_name <- names(x)[closest_index]
        value <- get_quantily_value(closest_index_name)
        return(value)
    }
}

get_rank <-function(x,y,quantiles=seq(from = 0.001, to = 0.999, by = 0.001)){
    qrf <- ranger(x=x,y=y,quantreg = TRUE)
    pred <- predict(qrf, x, type = "quantiles",quantiles=quantiles)
    outMatrix <- pred$predictions
    median_outMatrix <- outMatrix[,(length(quantiles)+1)/2]
    diffs = y - median_outMatrix
    rmse <- sqrt(sum(diffs*diffs)/(length(diffs)-1))

    rank_value <-c()
    median_values <-c()
    for (i in 1:length(y)){
        median_values <- c(median_values,median_outMatrix[i])
        rank_<- find_max_index(outMatrix[i,],y[i])
        if (length(rank_)>1){
            diff = y[i] -median_outMatrix[i]
            if (abs(diff)>3*rmse & diff<0 ){
                min_value <- min(rank_)
                rank_value<-c(rank_value,min_value)
            } else if (abs(diff)>3*rmse & diff>0) {
                max_value <- max(rank_)
                rank_value<-c(rank_value,max_value)
            }else {
                mean_value <- mean(rank_)
                rank_value<-c(rank_value,mean_value)
            }       
        }else {
            rank_value<-c(rank_value,rank_)
        }
    }
    result <- data.frame(orinal_value= y, median_values = median_values,rank = rank_value)
    return(result)

}

# Example usage
iris1<-generateOutliers(iris, p = 0.2,seed=2024)
outMatrix <- get_rank(iris1[,2:4], iris1[,1])
print(outMatrix)
