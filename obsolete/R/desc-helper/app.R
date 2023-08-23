#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(shinydashboard)
library(DT)
library(RPostgres)

con <- dbConnect(Postgres(),
                 user = Sys.getenv("AURA_TARGET_USER"), 
                 password = Sys.getenv("AURA_TARGET_PASS"),
                 dbname = Sys.getenv("AURA_TARGET_NAME"),
                 host = Sys.getenv("AURA_TARGET_HOST"), 
                 port = "5432")


# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
  dashboardPage(dashboardHeader(disable = T),
                dashboardSidebar(disable = T),
                dashboardBody(uiOutput("MainBody"))
  )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
   
  output$MainBody = renderUI({
    
    fluidPage(
      box(width=12,
          h3(strong("Kontrola odhadovaných popisků"),align="center"),
          hr(),
          column(6,offset = 6,
                 HTML('<div class="btn-group" role="group" aria-label="Basic example">'),
                 HTML('</div>')
          ),
          
          column(12,dataTableOutput("Main_table")),
          tags$script("$(document).on('click', '#Main_table button', function () {
                    Shiny.onInputChange('lastClickId',this.id);
                    Shiny.onInputChange('lastClick', Math.random())
  });")
          
      )
    )
    })
      ##The code may seem weird but we will modify it later
  files <- system("ls data*.RData", intern = TRUE)
  print(tail(files, 1))
  data <- readRDS(tail(files, 1))
  
  output$Main_table=renderDataTable({ 
    DT = data
    DT$Actions <-
      paste0('
             <div class="btn-group" role="group" aria-label="Basic example">
             <button type="button" class="btn btn-secondary delete" id=upload_',
                1:nrow(data),'>Upload</button>
             </div>
             
             ')
    datatable(DT,
                  escape=F)
    })
 
  observeEvent(input$lastClick,
    {
      if (grepl("upload", input$lastClickId )) {
        row_to_upload = as.numeric(gsub("upload_","",input$lastClickId))
        person_id <- data[row_to_upload, ]$id
        description <- data[row_to_upload, ]$predicted_label
        sql <- glue::glue("INSERT INTO person_descriptions (person_id, description) 
        VALUES ('{person_id}', '{description}')")
        
        print(data[row_to_upload, ])
        print(sql)
        
        r <- dbSendStatement(con, sql)
        dbClearResult(r)
        #vals$Data=vals$Data[-row_to_del]
      }
    }
  )
       
}

# Run the application 
shinyApp(ui = ui, server = server)

