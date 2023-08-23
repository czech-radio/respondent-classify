# pre-classifications edits

library(RPostgres)
library(dplyr)
library(stringdist)

con <- dbConnect(Postgres(),
                 user = Sys.getenv("AURA_TARGET_USER"), 
                 password = Sys.getenv("AURA_TARGET_PASS"),
                 dbname = Sys.getenv("AURA_TARGET_NAME"),
                 host = Sys.getenv("AURA_TARGET_HOST"), 
                 port = "5432")

persons <- dbGetQuery(con, "select * from persons_view 
                      where party_name in ('BEZPP', 'ZAHR')")
person_descriptions <- dbGetQuery(con, "select * from person_descriptions")
categories <- c('advokát', 'akademik', 'aktivista', 'blogger', 'byznys', 
                'celebrita', 'církev', 'europol', 'komentátor', 'kontrolor', 
                'kultura', 'léčitel', 'lobby', 'zdravotník', 'mluvčí', 'ngo', 
                'novinář', 'odborník', 'odbory', 'ostatní', 'ombudsman', 
                'ozbrojenec', 'politik', 'social', 'soudce', 'soudce_us', 
                'spolek', 'sport', 'starosta', 'stát_byznys', 'ttank', 
                'umělec', 'úředník', 'vyslanec', 'zaměstnavatel', 'zástupce', 
                'záchranář', 'média', 'mezinárodní')


#' Najdi mluvčí nějaké instituce, kteří nemají popisek mluvčí
speakers <- persons %>%
  filter(grepl("mluvčí", descriptions))

speakers_list <- strsplit(speakers$descriptions, ";") %>% 
  purrr::map(., stringr::str_trim) 

speakers_list %>% unlist -> all_descriptions

speakers_to_update <- speakers %>%
  mutate(descriptions_split = strsplit(descriptions, ";") %>% 
           purrr::map(., stringr::str_trim)) %>% 
  mutate(desc_category = purrr::map(descriptions_split, 
                                    function(x) x[x %in% categories])) %>%
  mutate(missing = purrr::map_lgl(desc_category, function(x) length(x) == 0)) %>%
  filter(missing)

purrr::map(speakers_to_update$id, function(x) {
  sql <- glue::glue("INSERT INTO person_descriptions (person_id, description) VALUES ('{x}', 'mluvčí')")
  r <- dbSendStatement(con, sql)
  dbClearResult(r)
  })

#' Najdi, které popisky jsou pravědpoobně překlepy (mají D-Levenshtein 
#' vzdálenost od standardizovaného popisku 1)
possible_typos <- 
  purrr::map_chr(person_descriptions$description, function(x) {
    possible_cat <- categories[which(stringdist(x, categories, method = "dl") == 1)]
    ifelse(length(possible_cat > 0), possible_cat, NA_character_)
  })

possible_typos_df <- person_descriptions %>%
  mutate(possible_typos = possible_typos) %>% 
  filter(description != "starostka") %>% 
  filter(!is.na(possible_typos))

purrr::pmap(list(possible_typos_df$person_id, possible_typos_df$description, 
                 possible_typos_df$possible_typos), function(x, y, z) {
  sql <- glue::glue("UPDATE person_descriptions SET description = '{z}' WHERE person_id = '{x}' AND description = '{y}'")
  r <- dbSendStatement(con, sql)
  dbClearResult(r)
})


# check for duplicated descriptions

# check if all standardized description has category = 1
person_descriptions2 <- dbGetQuery(con, "select * from person_descriptions")
person_descriptions2 %>%
  filter(description %in% categories) %>%
  filter(category == 0) -> update_category

purrr::map2(update_category$person_id, update_category$description, function(x, y) {
  sql <- glue::glue("UPDATE person_descriptions SET category = 1 WHERE person_id = '{x}' AND description = '{y}'")
  r <- dbSendStatement(con, sql)
  dbClearResult(r)
})
