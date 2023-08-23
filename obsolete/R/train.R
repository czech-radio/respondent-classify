library(RPostgres)
library(dplyr)
library(quanteda)
library(caret)

#' ZAHR
#' politici vs. ne-politici

con <- dbConnect(Postgres(),
                 user = Sys.getenv("AURA_TARGET_USER"), 
                 password = Sys.getenv("AURA_TARGET_PASS"),
                 dbname = Sys.getenv("AURA_TARGET_NAME"),
                 host = Sys.getenv("AURA_TARGET_HOST"), 
                 port = "5432")

persons <- dbGetQuery(con, "select * from persons_view")
categories <- c('advokát', 'akademik', 'aktivista', 'blogger', 'byznys', 'celebrita', 'církev', 
                'europol', 'europoslanec', 'extremista', 'hejtman', 'junior', 
                'kand_obec', 'kand_kraj', 'kand_prez', 'kand_posl', 'kand_senat', 
                'komentátor', 'kontrolor', 'kultura', 'léčitel', 'lobby', 'zdravotník', 'mluvčí', 
                'ngo', 'novinář', 'odborník', 'odbory', 'ostatní', 'ombudsman', 'ozbrojenec',
                'politik', 'poslanec', 'senátor', 'social', 'soudce', 'soudce_us', 'spolek', 
                'sport', 'starosta', 'stat_byznys', 'ttank', 'umělec', 'úředník', 'ustavni_fce', 
                'vyslanec', 'zaměstnavatel', 'zast_obec', 'zast_kraj', 'zástupce', 'záchranář')

descriptions_list <- strsplit(persons$descriptions, ";") %>% 
    purrr::map(., stringr::str_trim) 

#' Počet lidí, kteří mají standardizovaný popisek
(purrr::map(descriptions_list, function(x) any(x %in% categories)) %>% unlist %>% sum -> has_desc_count)

#' Popisky patřící do jedné z definovaných kategorií
purrr::map(descriptions_list, function(x) x[x %in% categories]) -> valid_categories
#' Ostatní popisky
purrr::map(descriptions_list, function(x) x[!x %in% categories]) -> other_descriptions

descriptions_list %>% unlist -> all_descriptions
#' Počet osob s danou kategorií
data.frame(desc = all_descriptions, 
           stringsAsFactors = FALSE) %>%
    group_by(desc) %>%
    summarise(count = n()) %>%
    filter(desc %in% categories) %>%
    arrange(desc(count)) %>%
    filter(count > 40) -> categories_enough

persons %>%
    mutate(descriptions_split = strsplit(descriptions, ";") %>% 
               purrr::map(., stringr::str_trim)) %>% 
    mutate(desc_category = purrr::map(descriptions_split, 
                                      function(x) x[x %in% categories])) -> persons_train 

#' Osoby, které mají alespoň jeden z definovaných popisků
persons_w_category <- persons_train[purrr::map_lgl(persons_train$desc_category, 
                                                   function(x) length(x) > 0), ]
persons_w_category2 <- persons_w_category %>%
    mutate(descs = purrr::map_chr(descriptions_split, 
                                  function(x) paste0(x, collapse = ";"))) %>% 
    mutate(categories = purrr::map_chr(desc_category, 
                                  function(x) paste0(x, collapse = ";")))

rep(1:nrow(persons_w_category2), 
     times = purrr::map_int(persons_w_category2$desc_category, length)) -> dupl_rows
persons_d <- persons_w_category2[dupl_rows, ] %>%
    group_by(id) %>%
    mutate(desc_category = desc_category[[1]][row_number()]) %>%
    filter(!is.na(desc_category))

#' Natrénovat model
dfm1 <- dfm(corpus(persons_d$descs, docnames = persons_d$id), remove = ";")
nb_model <- textmodel_nb(dfm1, persons_d$desc_category)


#' Kontrola úspešnosti klasifikace
actual_class <- factor(persons_d$desc_category)
prediction <- predict(nb_model, dfm1)
# head(prediction$posterior.prob) # hodnoty jednotlivych labelu 
predicted_class <- prediction

confusionMatrix(predicted_class, actual_class)

saveRDS(nb_model, file = paste0("models/nb_model_", as.Date(Sys.time()), ".RData"))

persons_wo_category <- persons %>% 
    filter(!id %in% persons_d$id)

dfm2 <- dfm(corpus(persons_wo_category$descriptions, docnames = persons_wo_category$id), 
            remove = ";")
dfm_common <- dfm_select(dfm2, dfm1)

p1 <- predict(nb_model, dfm_common)

data.frame(person_id = persons_wo_category$id, 
           descriptions = persons_wo_category$descriptions, 
           predicted_label = p1, 
           stringsAsFactors = FALSE) -> predicted_labels

