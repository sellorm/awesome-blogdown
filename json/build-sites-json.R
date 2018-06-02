#!/usr/bin/env Rscript --vanilla
library(jsonlite)
library(purrr)
files <- dir(pattern = ".json$")
output <- map_df(files, jsonlite::read_json)

output_json <- toJSON(output)
write(output_json, file = "sites.json")
