library(RPostgres)
library(dplyr)
library(quanteda)
library(caret)

#' ZAHR

con <- dbConnect(Postgres(),
                 user = Sys.getenv("AURA_TARGET_USER"), 
                 password = Sys.getenv("AURA_TARGET_PASS"),
                 dbname = Sys.getenv("AURA_TARGET_NAME"),
                 host = Sys.getenv("AURA_TARGET_HOST"), 
                 port = "5432")

persons <- dbGetQuery(con, "select * from persons_view 
                      where party_name in ('BEZPP', 'ZAHR')")
categories <- c('advokát', 'akademik', 'aktivista', 'blogger', 'byznys', 
                'celebrita', 'církev', 'europol', 'komentátor', 'kontrolor', 
                'kultura', 'léčitel', 'lobby', 'zdravotník', 'mluvčí', 
                'ngo', 'novinář', 'odborník', 'odbory', 'ostatní', 'ombudsman', 
                'ozbrojenec', 'politik', 'social', 'soudce', 'soudce_us', 
                'spolek', 'sport', 'starosta', 'stát_byznys', 'ttank', 
                'umělec', 'úředník', 'vyslanec', 'zaměstnavatel', 'zástupce', 
                'záchranář', 'média', 'mezinárodní')

descriptions_list <- strsplit(persons$descriptions, ";") %>% 
  purrr::map(., stringr::str_trim) 

descriptions_list %>% unlist -> all_descriptions

persons_train <- persons %>%
  mutate(descriptions_split = strsplit(descriptions, ";") %>% 
           purrr::map(., stringr::str_trim)) %>% 
  mutate(desc_category = purrr::map(descriptions_split, 
                                    function(x) x[x %in% categories]), 
         descs = purrr::map_chr(descriptions_split, 
                                   function(x) paste0(x[!x %in% categories], collapse = ";")))

#' Osoby, které mají alespoň jeden z definovaných popisků
persons_w_category <- persons_train[purrr::map_lgl(persons_train$desc_category, 
                                                   function(x) length(x) > 0), ]

dupl_rows <- rep(1:nrow(persons_w_category), 
    times = purrr::map_int(persons_w_category$desc_category, length))
persons_d <- persons_w_category[dupl_rows, ] %>%
  group_by(id) %>%
  mutate(desc_category = desc_category[[1]][row_number()]) %>%
  filter(!is.na(desc_category))

#' Natrénovat model
dfm1 <- dfm(corpus(persons_d$descs, docnames = persons_d$id), remove = ";")

set.seed(161)
train_ids <- sample(persons_d$id, size = 35000, replace = FALSE)
train_dfm <- dfm_subset(dfm1, persons_d$id %in% train_ids)
test_dfm <- dfm_subset(dfm1, !persons_d$id %in% train_ids)

nb_model_train <- textmodel_nb(train_dfm, 
                               persons_d$desc_category[persons_d$id %in% train_ids])

#' Kontrola úspešnosti klasifikace
actual_class <- persons_d$desc_category[!persons_d$id %in% train_ids]
prediction <- predict(nb_model_train, test_dfm)

confusionMatrix(prediction, factor(actual_class, levels = levels(prediction)))

saveRDS(nb_model_train, file = paste0("models/nb_model_", as.Date(Sys.time()), "not_politicians.RData"))

persons_wo_category <- persons %>% 
  filter(!id %in% persons_d$id)

dfm2 <- dfm(corpus(persons_wo_category$descriptions, docnames = persons_wo_category$id), 
            remove = ";")
dfm_common <- dfm_select(dfm2, dfm1)

p1 <- predict(nb_model_train, dfm_common) # vrací predikci class
p1_p <- predict(nb_model_train, dfm_common, type = "probability") # vrací classes s pravděpodobnostmi

purrr::map2_dbl(1:length(p1), p1, function(x, y) p1_p[x, y]) -> probs

data.frame(person_id = persons_wo_category$id, 
           descriptions = persons_wo_category$descriptions, 
           predicted_label = p1, 
           prob_label = probs, 
           stringsAsFactors = FALSE) -> predicted_labels

persons %>%
  select(id, first_name, last_name, party_name) %>%
  inner_join(., predicted_labels, by = c("id"="person_id")) -> predicted_labels2
saveRDS(predicted_labels2, file = paste0("desc-helper/data_", as.Date(Sys.time()), ".RData"))


