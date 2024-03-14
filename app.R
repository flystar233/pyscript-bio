library(shiny)
library(dplyr)
library(stringr)
library(ggrain)
library(sqldf)
library(readr)
ui <- fluidPage(
    titlePanel("Data Operation"),
    sidebarLayout(
        sidebarPanel(
            selectInput(
                inputId = "operation",
                label = "Choose an operation:",
                choices = c(
                    "交集(Intersect)", "并集(Union)",
                    "补集(Setdiff)", "去重(Unique)",
                    "排序(Sort)", "筛选(Filter by re)","筛选(Filter by sql)","云雨图(Raincloud)","时间戳转时间(Timestamp to Date)","相关性检验(Correlation)"
                ),
                selected = "交集(intersect)"
            ),
            radioButtons("data", "Choose data:", choices = c("data1", "data2"), inline = TRUE),
            textAreaInput("data1", "data1", rows = 15, cols = 180),
            textAreaInput("data2", "data2", rows = 15, cols = 180),
            textInput("filter", "筛选条件（正则表达式）：", ".*"),
            textInput("filter2", "筛选条件（SQL）：", "select * from df"),
        ),
        mainPanel(HTML('<textarea id="ta" class="form-control shiny-text-output"',
                       'style="resize:none;height:500px;" readonly></textarea>'),
                  br(),  
                  textOutput("text"),
                  verbatimTextOutput("COUNT"),
                  textOutput("text2"),
                  plotOutput("plot", width = "400px", height = "300px")
        )
    )
)

server <- function(input, output, session) {
    options(scipen=999)
    dataInput <- reactive({
        op <- input$operation
        data1 <- str_split(input$data1, "\n")[[1]]
        data2 <- str_split(input$data2, "\n")[[1]]
        filter <- input$filter
        data <- if (input$data == "data1") data1 else data2
        result<-switch(
            op,
            "交集(Intersect)" = intersect(data1, data2),
            "并集(Union)" = union(data1, data2),
            "补集(Setdiff)" = setdiff(data1, data2),
            "去重(Unique)" = unique(data),
            "排序(Sort)" = {
                if (all(str_detect(data, "^[0-9\\.]+$"))) {
                    sort(as.numeric(data))
                } else {
                    sort(data)
                }
            },
            "时间戳转时间(Timestamp to Date)" = {
                timestamp <- as.numeric(data)/1000
                beijing_time <- as.POSIXct(timestamp, origin = "1970-01-01", tz = "Asia/Shanghai")
                new_york_time <- as.POSIXct(timestamp, origin = "1970-01-01", tz = "America/New_York")
                paste0("Beijing Time:\t", format(beijing_time, "%Y-%m-%d %H:%M:%S"), "\nNew York Time:\t", format(new_york_time, "%Y-%m-%d %H:%M:%S"))
            },
            "筛选(Filter by re)" = data[str_detect(data, filter)],
            "筛选(Filter by sql)" = {
                #df <- read.table(text=data1,header = TRUE, sep = "\t")
                df <- read_table(data1)
                result<- sqldf(input$filter2)
                format_result<- paste(capture.output(print(result)), collapse = "\n")
            },
            "云雨图(Raincloud)" = {
                dt <- read.table(text = data1, header = FALSE, sep = "\t")
                ggplot(dt, aes(1,V1)) + geom_rain()+ theme_classic()
            },
            "相关性检验(Correlation)" = {
                estimate_of_pearson<-""
                p_value_of_correlation_pearson<-""
                estimate_of_spearman<-""
                p_value_of_correlation_spearman<-""

                if (length(data1) == length(data2)) {
                    t_test <- t.test(as.numeric(data1),as.numeric(data2),paired=TRUE)
                    p_value_of_t_test <- format(t_test$p.value,scientific = TRUE)

                    wilcox <- wilcox.test(as.numeric(data1),as.numeric(data2),exact = F,paired=TRUE)
                    p_value_of_wilcox <- format(wilcox$p.value,scientific = TRUE)

                    correlation_pearson <- cor.test(as.numeric(data1), as.numeric(data2),method = 'pearson')
                    estimate_of_pearson <- correlation_pearson$estimate
                    p_value_of_correlation_pearson <-format(correlation_pearson$p.value,scientific = TRUE)

                    correlation_spearman<-cor.test(as.numeric(data1), as.numeric(data2),method = 'spearman')
                    estimate_of_spearman <- correlation_spearman$estimate
                    p_value_of_correlation_spearman <-format(correlation_spearman$p.value,scientific = TRUE)

            } else {
                    t_test <- t.test(as.numeric(data1),as.numeric(data2),paired=FALSE)
                    p_value_of_t_test <- format(t_test$p.value,scientific = TRUE)
                    wilcox <- wilcox.test(as.numeric(data1),as.numeric(data2),exact = F,paired=FALSE)
                    p_value_of_wilcox <- format(wilcox$p.value,scientific = TRUE)
                }
                paste0("T 检验(p value):\t",p_value_of_t_test,
                       "\nWilcox 秩和检验(p value):\t",p_value_of_wilcox,
                       "\nPearson 相关性检验(相关系数,p value):\t",estimate_of_pearson,"\t",p_value_of_correlation_pearson,
                       "\nSpearman 相关性检验(相关系数,p value):\t",estimate_of_spearman,"\t",p_value_of_correlation_pearson
                       )
            }
        )
        if(typeof(result) != "list"){
            paste(result, sep = "", collapse = "\n")
        }else {
            result
        }
        
    })

    output$ta<-renderText({
        req(input$operation != "云雨图(Raincloud)")
        dataInput()
    })
    output$text <- renderText({ 
        "Count: " 
    })
    output$COUNT<-renderText({ 
        req(input$operation != "云雨图(Raincloud)")
        data_2<-dataInput()
        sum(nzchar(str_split(data_2,"\n")[[1]]))
    })
     output$text2 <- renderText({ 
        "Raincloud Plot: " 
    })
    output$plot <- renderPlot({
        req(input$operation == "云雨图(Raincloud)")
        print(dataInput())
    })
}

shinyApp(ui, server)
