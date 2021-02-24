library(dplyr)
library(ggplot2)
library(gridExtra)
library(zoo)

source("utils.R")

# Load dataset using 'coronabr', see 'utils.R'.
ministry_dataset <- WrapperGetCoronaBrMinSaude()

city_name = "Petrópolis"  # City name to filter by.

frame <- subset(ministry_dataset, municipio == city_name)
frame <- subset(frame, select=c("municipio", "data", "casosNovos", "obitosNovos"))
frame$data <- as.Date(frame$data, format = "%Y-%m-%d")

frame$rolling_cases <- round(rollmean(frame$casosNovos, k = 15, fill = NA), 2)

frame <- frame[order(frame$data),]
rownames(frame) <- NULL

p <- ggplot(frame, aes(x = data, y = rolling_cases)) + 
    geom_line(lwd=1.2) +
    theme_bw() +
    ggtitle(paste("Média Móvel de Casos em", city_name, "-", Sys.Date())) +
    xlab("Tempo") +
    ylab("Média Móvel de Casos (k=15)")

ggsave(file="images/RoolMeanCases.png", p, height=8, width=8, dpi=400)
