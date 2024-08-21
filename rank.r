library(outForest)

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

get_rank <-function(data,quantiles=seq(from = 0.001, to = 0.999, by = 0.001),...){
    data <- as.data.frame(data)
    numeric_features <- names(data)[sapply(data,is.numeric)]
    final_result <- data.frame()
    for (v in numeric_features){
        covariables <- setdiff(numeric_features, v)
        qrf <- ranger::ranger(
            formula = stats::reformulate(covariables, response = v),
            data = data,
            quantreg = TRUE,
            ...)
        pred <- predict(qrf, data[,covariables], type = "quantiles",quantiles=quantiles)
        outMatrix <- pred$predictions
        median_outMatrix <- outMatrix[,(length(quantiles)+1)/2]

        response<- data[,v]
        diffs = response - median_outMatrix
        rmse <- sqrt(sum(diffs*diffs)/(length(diffs)-1))
        rank_value <-c()
        median_values <-c()
        for (i in 1:length(response)){
            median_values <- c(median_values,median_outMatrix[i])
            rank_<- find_max_index(outMatrix[i,],response[i])
            if (length(rank_)>1){
                diff = response[i] -median_outMatrix[i]
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
        result <- data.frame(row = row.names(data),col = v,observed = response, predicted = median_values,rank = rank_value)
        result<- result|>dplyr::filter(rank<=0.025| rank>=0.975)
        final_result <- rbind(final_result,result)
    }
    return(final_result)

}

# Example usage
iris1<-generateOutliers(iris, p = 0.1)
outMatrix <- get_rank(iris1)
print(outMatrix)
