library(shiny)
library(dplyr)
library(stringr)
library(ggrain)

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
                    "排序(Sort)", "筛选(Filter)","云雨图(Raincloud)","时间戳转时间(Timestamp to Date)"
                ),
                selected = "交集(intersect)"
            ),
            radioButtons("data", "Choose data:", choices = c("data1", "data2"), inline = TRUE),
            textAreaInput("data1", "data1", rows = 15, cols = 180),
            textAreaInput("data2", "data2", rows = 15, cols = 180),
            textInput("filter", "筛选条件（正则表达式）：", ".*"),
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
            "筛选(Filter)" = data[str_detect(data, filter)],
            "云雨图(Raincloud)" = {
                dt <- read.table(text = data1, header = FALSE, sep = "\t")
                ggplot(dt, aes(1,V1)) + geom_rain()+ theme_classic()
            }
        )
        if(typeof(result) != "list"){
            paste(result, sep = "", collapse = "\n")
        }else {
            result
        }
        
    })

    output$ta<-renderText({
        if (input$operation != "云雨图(Raincloud)") {
        data<-dataInput() }
    })
    output$text <- renderText({ 
        "Count: " 
    })
    output$COUNT<-renderText({ 
        if (input$operation != "云雨图(Raincloud)") {
        data_2<-dataInput()
        sum(nzchar(str_split(data_2,"\n")[[1]])) }
    })
     output$text2 <- renderText({ 
        "Raincloud Plot: " 
    })
    output$plot <- renderPlot({
      if (input$operation == "云雨图(Raincloud)") {
            print(dataInput())
        }
    })
}

shinyApp(ui, server)